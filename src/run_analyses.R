# ==============================================================================
# Statistical Analyses: Diagnostic Specificity & Severity Monotonicity
# ==============================================================================

library(tidyverse)
library(sandwich)
library(lmtest)
library(ggeffects)
library(patchwork)

# --- Run config --------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
run_id <- if (length(args) >= 1) args[1] else format(Sys.Date(), "%Y-%m-%d")

data_dir <- file.path("data", "runs", run_id)
figures_dir <- file.path("figures", "runs", run_id)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

cat(sprintf("Run ID: %s\n", run_id))

# --- Data ---------------------------------------------------------------------
df <- read_csv(file.path(data_dir, "scored_results.csv"), show_col_types = FALSE)

# Abbreviate diagnosis names
abbrev <- c(
  "Frontotemporal Dementia (Behavioral Variant)" = "FTD",
  "Post-Traumatic Stress Disorder"               = "PTSD",
  "Obsessive-Compulsive Disorder"                = "OCD",
  "Alcohol-Induced Mood Disorder"                = "Alcohol Mood",
  "Generalized Anxiety Disorder"                 = "GAD",
  "Parkinson's Disease Dementia"                 = "Parkinson's",
  "Major Depressive Disorder"                    = "MDD",
  "Binge Eating Disorder"                        = "Binge Eating",
  "Alzheimer's Disease"                          = "Alzheimer's",
  "Bipolar I Disorder"                           = "Bipolar I",
  "Anorexia Nervosa"                             = "Anorexia",
  "Bulimia Nervosa"                              = "Bulimia",
  "Schizophrenia"                                = "Schizophrenia"
)

df <- df %>% mutate(Diagnosis = recode(Diagnosis, !!!abbrev))

# --- Target mapping -----------------------------------------------------------
target_map <- list(
  "PHQ-9" = c("MDD", "Bipolar I", "Alcohol Mood"),
  "GAD-7" = c("GAD", "PTSD", "Alcohol Mood"),
  "OCI-R" = c("OCD"),
  "PCL-5" = c("PTSD"),
  "MDQ"   = c("Bipolar I"),
  "PQ-16" = c("Schizophrenia", "Parkinson's", "FTD"),
  "EDE-Q" = c("Anorexia", "Bulimia", "Binge Eating")
)

# Clinical cutoffs
cutoffs <- c(
  "PHQ-9" = 10, "GAD-7" = 10, "OCI-R" = 21, "PCL-5" = 33,
  "MDQ" = 7, "PQ-16" = 6, "EDE-Q" = 4.0
)

battery_order <- c("PHQ-9", "GAD-7", "OCI-R", "PCL-5", "MDQ", "PQ-16", "EDE-Q")

# Create Target indicator and ordinal severity
df <- df %>%
  rowwise() %>%
  mutate(Target = as.integer(Diagnosis %in% target_map[[Battery]])) %>%
  ungroup() %>%
  mutate(
    Severity_ord = case_when(
      Severity == "Mild"     ~ 1L,
      Severity == "Moderate" ~ 2L,
      Severity == "Severe"   ~ 3L
    ),
    Target_f = factor(Target, levels = c(0, 1), labels = c("Non-target", "Target"))
  )

# Helper: cluster-robust SEs if >= 2 clusters, else HC robust SEs
robust_vcov <- function(model, clusters) {
  n_clust <- length(unique(clusters))
  if (n_clust >= 2) {
    vcovCL(model, cluster = clusters)
  } else {
    vcovHC(model, type = "HC1")
  }
}

# Parse demographics from Persona_ID for robustness checks
df <- df %>%
  separate(Persona_ID, into = c("code", "sev", "gender", "age", "edu", "pol"),
           sep = "_", remove = FALSE) %>%
  mutate(age = as.integer(age))

# ==============================================================================
# Analysis 1: Diagnostic Specificity — Target vs. Non-Target
# ==============================================================================
cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS 1: Diagnostic Specificity (Target vs Non-Target per Battery)\n")
cat(strrep("=", 70), "\n\n")

specificity_results <- list()

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat)
  m <- lm(Score ~ Target, data = sub)

  # Cluster-robust SEs by Diagnosis
  vcov_cl <- robust_vcov(m, sub$Diagnosis)
  ct <- coeftest(m, vcov. = vcov_cl)

  ci <- coefci(m, vcov. = vcov_cl, level = 0.95)

  cat(sprintf("--- %s ---\n", bat))
  cat(sprintf("  Non-target mean: %.2f | Target mean: %.2f\n",
              mean(sub$Score[sub$Target == 0]),
              mean(sub$Score[sub$Target == 1])))
  cat(sprintf("  Target coef: %.2f [%.2f, %.2f], p = %.2e\n",
              ct["Target", "Estimate"], ci["Target", 1], ci["Target", 2], ct["Target", 4]))
  cat("\n")

  specificity_results[[bat]] <- tibble(
    Battery = bat,
    Analysis = "Specificity",
    Term = "Target",
    Estimate = ct["Target", "Estimate"],
    CI_lower = ci["Target", 1],
    CI_upper = ci["Target", 2],
    p_value = ct["Target", 4]
  )
}

# ==============================================================================
# Analysis 2: Severity Monotonicity (within target groups)
# ==============================================================================
cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS 2: Severity Monotonicity (within Target groups)\n")
cat(strrep("=", 70), "\n\n")

severity_results <- list()

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat, Target == 1)
  m <- lm(Score ~ Severity_ord, data = sub)

  vcov_cl <- robust_vcov(m, sub$Diagnosis)
  ct <- coeftest(m, vcov. = vcov_cl)
  ci <- coefci(m, vcov. = vcov_cl, level = 0.95)

  cat(sprintf("--- %s (target only, n=%d) ---\n", bat, nrow(sub)))
  cat(sprintf("  Mild mean: %.2f | Moderate mean: %.2f | Severe mean: %.2f\n",
              mean(sub$Score[sub$Severity == "Mild"]),
              mean(sub$Score[sub$Severity == "Moderate"]),
              mean(sub$Score[sub$Severity == "Severe"])))
  cat(sprintf("  Severity slope: %.2f [%.2f, %.2f], p = %.2e\n",
              ct["Severity_ord", "Estimate"], ci["Severity_ord", 1], ci["Severity_ord", 2],
              ct["Severity_ord", 4]))
  cat("\n")

  severity_results[[bat]] <- tibble(
    Battery = bat,
    Analysis = "Severity_trend",
    Term = "Severity_ord",
    Estimate = ct["Severity_ord", "Estimate"],
    CI_lower = ci["Severity_ord", 1],
    CI_upper = ci["Severity_ord", 2],
    p_value = ct["Severity_ord", 4]
  )
}

# ==============================================================================
# Analysis 3: Target × Severity Interaction
# ==============================================================================
cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS 3: Target x Severity Interaction\n")
cat(strrep("=", 70), "\n\n")

interaction_results <- list()

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat)
  m <- lm(Score ~ Target * Severity_ord, data = sub)

  vcov_cl <- robust_vcov(m, sub$Diagnosis)
  ct <- coeftest(m, vcov. = vcov_cl)
  ci <- coefci(m, vcov. = vcov_cl, level = 0.95)

  cat(sprintf("--- %s ---\n", bat))
  print(ct)
  cat("\n")

  # Store interaction term
  interaction_results[[bat]] <- tibble(
    Battery = bat,
    Analysis = "Interaction",
    Term = "Target:Severity_ord",
    Estimate = ct["Target:Severity_ord", "Estimate"],
    CI_lower = ci["Target:Severity_ord", 1],
    CI_upper = ci["Target:Severity_ord", 2],
    p_value = ct["Target:Severity_ord", 4]
  )
}

# ==============================================================================
# Analysis 4: Cutoff Classification Rates
# ==============================================================================
cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS 4: Cutoff Classification Rates\n")
cat(strrep("=", 70), "\n\n")

cutoff_results <- list()

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat)
  co <- cutoffs[bat]

  sub <- sub %>% mutate(Above = as.integer(Score >= co))

  # Sensitivity by severity (target only)
  target_sub <- sub %>% filter(Target == 1)
  sens_by_sev <- target_sub %>%
    group_by(Severity) %>%
    summarise(sensitivity = mean(Above), n = n(), .groups = "drop")

  # Specificity (non-target)
  nontarget_sub <- sub %>% filter(Target == 0)
  specificity <- 1 - mean(nontarget_sub$Above)

  # Chi-squared test
  tbl <- table(sub$Target_f, sub$Above)
  chi <- chisq.test(tbl)

  cat(sprintf("--- %s (cutoff = %.1f) ---\n", bat, co))
  cat("  Sensitivity by severity (target):\n")
  for (i in seq_len(nrow(sens_by_sev))) {
    cat(sprintf("    %s: %.1f%% (%d/%d)\n",
                sens_by_sev$Severity[i],
                sens_by_sev$sensitivity[i] * 100,
                sum(target_sub$Above[target_sub$Severity == sens_by_sev$Severity[i]]),
                sens_by_sev$n[i]))
  }
  cat(sprintf("  Specificity (non-target): %.1f%%\n", specificity * 100))
  cat(sprintf("  Chi-squared: %.1f, df=%d, p = %.2e\n", chi$statistic, chi$parameter, chi$p.value))
  cat("\n")

  cutoff_results[[bat]] <- tibble(
    Battery = bat,
    Cutoff = co,
    Sens_Mild = sens_by_sev$sensitivity[sens_by_sev$Severity == "Mild"],
    Sens_Moderate = sens_by_sev$sensitivity[sens_by_sev$Severity == "Moderate"],
    Sens_Severe = sens_by_sev$sensitivity[sens_by_sev$Severity == "Severe"],
    Specificity = specificity,
    Chi_sq = chi$statistic,
    Chi_p = chi$p.value
  )
}

# ==============================================================================
# Analysis 5: Demographic Robustness Check
# ==============================================================================
cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS 5: Demographic Robustness Check\n")
cat(strrep("=", 70), "\n\n")

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat)
  m <- lm(Score ~ Target * Severity_ord + age + gender + edu, data = sub)

  vcov_cl <- robust_vcov(m, sub$Diagnosis)
  ct <- coeftest(m, vcov. = vcov_cl)

  cat(sprintf("--- %s ---\n", bat))
  print(ct)
  cat("\n")
}

# ==============================================================================
# Verification Plots (ggeffects) — Temporary, for review
# ==============================================================================
cat("\nGenerating verification plots...\n")

dir.create("figures", showWarnings = FALSE)

plot_list <- list()

for (bat in battery_order) {
  sub <- df %>% filter(Battery == bat) %>%
    mutate(Severity_ord = as.numeric(Severity_ord))

  m <- lm(Score ~ Target_f * Severity_ord, data = sub)

  pred <- ggpredict(m, terms = c("Severity_ord", "Target_f"))

  # Mark significant interactions with *
  int_p <- interaction_results[[bat]]$p_value
  bat_label <- if (int_p < 0.05) paste0(bat, " *") else bat

  p <- plot(pred) +
    scale_x_continuous(breaks = 1:3, labels = c("Mild", "Moderate", "Severe")) +
    geom_hline(yintercept = cutoffs[bat], linetype = "dashed", color = "grey40") +
    labs(
      title = bat_label,
      x = "Severity", y = "Predicted Score", color = "Group"
    ) +
    theme_classic(base_size = 12)

  plot_list[[bat]] <- p
}

# --- Patchwork assembly (no overall title) ------------------------------------
combined <- wrap_plots(plot_list, ncol = 4, guides = "collect") +
  plot_annotation(
    caption = "* significant Target x Severity interaction (p < .05, cluster-robust SEs)"
  ) &
  theme(legend.position = "bottom")

ggsave(file.path(figures_dir, "analysis_verification_patchwork.png"), combined,
       width = 14, height = 7, dpi = 150)
ggsave(file.path(figures_dir, "analysis_verification_patchwork.pdf"), combined,
       width = 14, height = 7, dpi = 300)

cat("Patchwork saved to figures/analysis_verification_patchwork.{png,pdf}\n")

# ==============================================================================
# Save summary table
# ==============================================================================
all_results <- bind_rows(
  bind_rows(specificity_results),
  bind_rows(severity_results),
  bind_rows(interaction_results)
)

write_csv(all_results, file.path(data_dir, "analysis_results.csv"))
cat("\nSummary table saved to data/analysis_results.csv\n")
cat("Done.\n")
