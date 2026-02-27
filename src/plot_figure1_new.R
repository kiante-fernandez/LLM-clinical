# ==============================================================================
# New Figure 1: Clinical Target Groups vs Clinical Controls
# Points + error bars (mean ± 95% CI) by severity, with clinical cutoff lines
# ==============================================================================

library(tidyverse)

# --- Data -------------------------------------------------------------------
df <- read_csv("data/scored_results.csv", show_col_types = FALSE)

# Abbreviate diagnosis names (match existing Python mapping)
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

df <- df %>%
  mutate(Diagnosis = recode(Diagnosis, !!!abbrev))

# --- Relevant groups & thresholds per battery --------------------------------
battery_info <- tribble(
  ~Battery, ~relevant,                                    ~threshold,
  "PHQ-9",  list(c("MDD", "Bipolar I", "Alcohol Mood")), 10,
  "GAD-7",  list(c("GAD", "PTSD", "Alcohol Mood")),      10,
  "OCI-R",  list(c("OCD")),                               21,
  "PCL-5",  list(c("PTSD")),                              33,
  "MDQ",    list(c("Bipolar I")),                          7,
  "PQ-16",  list(c("Schizophrenia", "Parkinson's", "FTD")), 6,
  "EDE-Q",  list(c("Anorexia", "Bulimia", "Binge Eating")), 4.0
)

# Flatten the relevant list for lookup
relevant_lookup <- battery_info %>%
  mutate(relevant = map(relevant, ~ .x[[1]])) %>%
  unnest(relevant) %>%
  select(Battery, relevant)

# --- Classify each row as target group or clinical control -------------------
df_labeled <- df %>%
  left_join(
    relevant_lookup %>% mutate(is_relevant = TRUE),
    by = c("Battery" = "Battery", "Diagnosis" = "relevant")
  ) %>%
  mutate(
    is_relevant = replace_na(is_relevant, FALSE),
    Group = if_else(is_relevant, Diagnosis, "Clinical Controls")
  )

# --- Summarise: mean, SE, 95% CI per Battery × Group × Severity -------------
summary_df <- df_labeled %>%
  group_by(Battery, Group, Severity) %>%
  summarise(
    mean_score = mean(Score, na.rm = TRUE),
    se         = sd(Score, na.rm = TRUE) / sqrt(n()),
    n          = n(),
    .groups    = "drop"
  ) %>%
  mutate(
    ci_lower = mean_score - 1.96 * se,
    ci_upper = mean_score + 1.96 * se
  )

# --- Thresholds data frame for geom_hline -----------------------------------
thresholds <- battery_info %>%
  select(Battery, threshold)

# --- Order severity as factor ------------------------------------------------
severity_order <- c("Mild", "Moderate", "Severe")
summary_df <- summary_df %>%
  mutate(Severity = factor(Severity, levels = severity_order))

# --- Order batteries ---------------------------------------------------------
battery_order <- c("PHQ-9", "GAD-7", "OCI-R", "PCL-5", "MDQ", "PQ-16", "EDE-Q")
summary_df <- summary_df %>%
  mutate(Battery = factor(Battery, levels = battery_order))
thresholds <- thresholds %>%
  mutate(Battery = factor(Battery, levels = battery_order))

# --- Put "Clinical Controls" last on x-axis ---------------------------------
group_levels <- summary_df %>%
  filter(Group != "Clinical Controls") %>%
  distinct(Group) %>%
  arrange(Group) %>%
  pull(Group)
group_levels <- c(group_levels, "Clinical Controls")

summary_df <- summary_df %>%
  mutate(Group = factor(Group, levels = group_levels))

# --- Color palette for severity ----------------------------------------------
severity_colors <- c(
  "Mild"     = "#fcbba1",
  "Moderate" = "#ef3b2c",
  "Severe"   = "#67000d"
)

# --- Plot --------------------------------------------------------------------
p <- ggplot(summary_df, aes(x = Group, y = mean_score, color = Severity)) +
  geom_hline(
    data = thresholds,
    aes(yintercept = threshold),
    linetype = "dashed",
    color = "grey40",
    linewidth = 0.5
  ) +
  geom_pointrange(
    aes(ymin = ci_lower, ymax = ci_upper),
    position = position_dodge(width = 0.6),
    size = 0.4,
    fatten = 2.5
  ) +
  facet_wrap(~ Battery, scales = "free", ncol = 4) +
  scale_color_manual(values = severity_colors) +
  labs(
    x = NULL,
    y = "Score",
    color = "Severity"
  ) +
  theme_minimal(base_size = 10) +
  theme(
    text              = element_text(family = "Helvetica"),
    strip.text        = element_text(face = "bold", size = 10),
    axis.text.x       = element_text(angle = 45, hjust = 1, size = 7),
    axis.text.y       = element_text(size = 8),
    legend.position   = "bottom",
    panel.grid.minor  = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.spacing     = unit(1, "lines")
  )

# --- Save --------------------------------------------------------------------
ggsave("figures/figure1_new.pdf", p, width = 10, height = 6, dpi = 300)
ggsave("figures/figure1_new.png", p, width = 10, height = 6, dpi = 300)

cat("Saved: figures/figure1_new.pdf and figures/figure1_new.png\n")
