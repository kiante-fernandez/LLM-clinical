# Pre-Submission Referee Report (Round 2)

**Paper**: The threat of synthetic respondents extends to clinical mental health screening
**Authors**: Kianté Fernandez, Laura A. Berner, Blair R. K. Shevlin
**Date**: 2026-03-05
**Review Standard**: JAMA Brief Report (Leading Field Journal)

---

## Overall Assessment

This Brief Report demonstrates that Google Gemini 2.0 Flash, given DSM-informed persona descriptions, can generate diagnostically differentiated and severity-sensitive scores across seven validated psychiatric screening instruments. The principal strength is the systematic breadth of the demonstration (seven instruments, 13 diagnoses, three severity levels). The single most critical issue is that the paper's central claim of "clinical plausibility" rests on total scores exceeding cutoffs without benchmarking against human clinical data or examining item-level response patterns.

**Preliminary Recommendation**: Revise before submitting

---

## 1. Spelling, Grammar & Style

### Critical Issues (must fix before submission)

1. **Line 115**: *"Westwood recently demonstrated that autonomous LLM-based respondents..."* — Narrative citation ("Westwood") is non-standard for JAMA's numbered citation style. → "A recent study demonstrated that autonomous LLM-based respondents..."

2. **Line 115**: Pronoun clarity — *"These LLM-based agents"* immediately follows the Westwood citation but could be confused with a general statement. Consider: "Those LLM-based agents..."

### Minor Issues

1. **$n$ vs $N$ inconsistency**: Table 1 footnote (line 190) uses "$N = 2106$" while Figure 1 caption (line 215) uses "$n = 2106$." Convention: uppercase $N$ for total sample, lowercase $n$ for subgroups. Standardize to $N$ in both places.

2. **Line 97 (Abstract/Results)**: *"the two instruments typically elevated across multiple disorders (PHQ-9 and GAD-7)"* — "typically elevated" characterizes the instruments themselves when the pattern is actually a characterization of the model's behavior. Consider: "the two instruments on which the model produced uniformly elevated scores across diagnostic groups (PHQ-9 and GAD-7)."

3. **Near-verbatim repetition**: The sentence "Coherent symptom endorsement above clinical thresholds can no longer serve as a proxy for authentic participation..." appears in Key Points (line 68), Conclusions (line 101), and Conclusions section (line 206). Consider varying the phrasing slightly across these occurrences.

4. **Line 155**: *"clinically differentiated response patterns"* — "Clinically differentiated" implies validation against clinical populations. Consider "diagnostically differentiated response patterns."

### Style Patterns

- **Active/passive voice inconsistency**: Methods uses passive ("Simulations were conducted"), Results switches to active ("We note two key findings"). JAMA permits both but consistency within sections improves readability.
- **Dash formatting**: En-dashes in instrument names (e.g., "Questionnaire--9") use LaTeX `--` correctly throughout. No issues.

---

## 2. Internal Consistency & Cross-Reference Verification

### Critical Inconsistencies

None found. All regression coefficients, confidence intervals, and P-values in Table 1 match the analysis data files.

### Cross-Reference Errors

1. **Hardcoded references**: `\textbf{Figure 1}` and `\textbf{Table 1}` are used as hardcoded bold text rather than LaTeX `\ref{}` commands. The `\label{tab:main-effects}` and `\label{fig:1}` are defined but never used. Not an error per se (JAMA style often uses hardcoded references), but could lead to desynchronization if numbering changes.

### Terminology Drift

1. **"Diagnosis-congruent" vs "target"**: The paper uses "diagnosis-congruent" in the Abstract (lines 64, 93, 97) and Table 1 footnotes (line 189), but "target" and "nontarget" in the Results body. These are consistent in meaning but an explicit mapping (e.g., "target (diagnosis-congruent) personas") at first use in Results would improve clarity.

2. **"Battery" vs "instrument"**: Methods uses "battery" (line 130, 144) while Results and Abstract use "instrument." These have slightly different senses (battery = administered test session, instrument = the tool itself), which is acceptable, but Results line 156 says "battery-dependent" when referring to instrument-level results.

### Minor Inconsistencies

1. **PHQ-9 mean scores rounding**: Line 157 states "PHQ-9: 13.55 vs 13.42" for target vs nontarget. Data file shows Target All = 13.578 and Non-target All = 13.449. Text rounds 13.578 to 13.55 (should be 13.58) and 13.449 to 13.42 (should be 13.45). Both values are close but not the nearest 2-decimal rounding of the actual data.

2. **$n$ vs $N$ inconsistency** (same as Agent 1 finding): Figure caption uses lowercase $n$, Table 1 uses uppercase $N$.

3. **GAD-7 and PQ-16 minor data gaps**: GAD-7 non-target group sums to 1619 instead of 1620 (one missing observation); PQ-16 target sums to 484 instead of 486 (two missing). The paper does not mention excluded observations. These are small (1-2 obs) and likely API parsing failures, but should ideally be noted.

4. **All citation keys verified**: All 16 `\cite{}` keys have matching `\bibitem{}` entries. No orphaned bibliography entries.

---

## 3. Unsupported Claims & Identification Integrity

### Causal Overclaiming (must address)

1. **Lines 64, 157, 161**: *"severity modulated scores monotonically"* — "Modulated" is causal language. The study documents a correlation between the severity label in the prompt and the output score. → "Scores increased monotonically with assigned severity" or "Assigned severity was associated with monotonically increasing scores."

2. **Line 119**: *"suggesting that even synthetic clinical text may capture patterns associated with diagnostic information"* — The inferential leap from "embeddings predict scores" to "text captures diagnostic patterns" could be hedged further. → "indicating that statistical regularities in synthetic clinical text are sufficient to predict screening scores."

### Generalization Issues

1. **Single-model limitation understated**: The title, abstract, Key Points, and Conclusions use generic phrases ("a standard commercial LLM," "LLMs") that invite generalization beyond the single model tested. The Conclusions should note results were obtained with a single commercial model. Consider softening "can no longer" to "may no longer reliably."

2. **"Clinically plausible" unanchored**: The paper claims responses are "clinically plausible" (lines 64, 101, 206) but never benchmarks against actual patient distributions. "Exceeding established clinical cutoffs" would be more precise.

3. **Prompt richness understated**: Line 144 states "No adversarial prompt engineering or fine-tuning was employed," but the prompts contained DSM-informed diagnoses and characteristic symptoms. The framing understates how much clinical information was provided.

### Missing Caveats

1. **No temperature/sampling parameters reported**: LLM outputs are stochastic; reproducibility is unaddressed.

2. **No test-retest or internal consistency analysis**: Readers cannot assess whether the patterns are stable.

3. **Line 111**: *"is no longer tenable"* — Stated as universal fact before the study's own contribution is presented. → "is increasingly questioned."

4. **Line 115**: *"Yet none of these studies examined..."* — Implicit "we are the first" claim. → "To our knowledge, none of these studies..."

5. **Line 157**: PHQ-9/GAD-7 non-specificity attributed to "known comorbidities." An equally valid interpretation: the model defaults to high depression/anxiety for any clinical persona. Present both interpretations.

6. **No discussion of ecological validity**: The threat model assumes an attacker with DSM-level knowledge. How realistic is this compared to typical survey fraud?

### Minor Language Issues

1. **Line 199**: *"The triviality of generating plausible counterfeits"* — "Triviality" overstates; the simulation required domain expertise and 7 full instrument implementations. → "The low marginal cost of generating plausible counterfeits..."

2. **Lines 68, 206**: *"can no longer"* implies a discrete temporal breakpoint. → "may not reliably."

3. **Line 81**: *"has not yet been examined"* → "to our knowledge, has not yet been examined."

---

## 4. Mathematics, Equations & Notation

### Mathematical Errors

None found. All numbers verified correct:
- Cartesian product: 13 × 3 × 3 × 2 × 3 × 3 = 2106 ✓
- All regression coefficients in Table 1 match analysis_results.csv ✓
- All CIs and P-values match ✓

### Notation Inconsistencies

1. **$n$ vs $N$**: Figure caption uses $n = 2106$, Table 1 uses $N = 2106$. Standardize.

2. **$b$ used for both models**: Table 1 uses $b$ for both diagnostic specificity and severity monotonicity regressions, which are different models with different dependent variables and samples. Consider distinguishing (e.g., subscripts) or clarifying in footnotes.

### Statistical Concerns

1. **13-cluster SEs**: Cluster-robust standard errors with only 13 clusters (diagnoses) may produce unreliable inference. The small-cluster literature (Cameron & Miller, 2015) suggests a minimum of ~50 clusters. Consider noting this limitation or reporting wild bootstrap p-values.

2. **Regression model underspecified**: Methods (line 148) describes the regression verbally but provides no equation. Adding a brief formal specification would improve clarity: $Y_{id} = \alpha + \beta \cdot \text{Target}_{id} + \varepsilon_{id}$.

### LaTeX Formatting

No issues found. Math formatting is clean throughout.

---

## 5. Tables, Figures & Documentation

### Table 1

1. **Missing model form**: The table notes describe what the coefficients represent but do not state the regression equation. Adding a brief specification would improve reproducibility.

2. **$N$ vs $n$ inconsistency** with Figure 1 (see above).

3. **Star notation**: No significance stars are used (P-values reported directly), which is appropriate for JAMA style.

### Figure 1

1. **X-axis abbreviations**: Diagnostic group abbreviations on the x-axis (e.g., "MDD," "Bipolar I," "Clinical Controls") are not all defined in the caption. While most are standard, the caption should either define all abbreviations or refer readers to the Methods.

2. **No panel labels**: The seven instrument panels have no letter labels (A, B, C...). Adding them would facilitate in-text references to specific panels.

3. **Nontarget group composition**: The caption states "averaged clinical control group (all nontarget diagnoses)" but does not specify how many diagnoses comprise each nontarget group or the per-group sample sizes.

4. **Cutoff citations**: The cutoff values are listed in the caption but not cited to their source publications.

### Cross-Reference Issues

All tables and figures are referenced in the text. No orphaned elements.

---

## 6. Contribution & Referee Assessment

### Part 1 — Central Contribution

The paper claims that a commercially available LLM can generate clinically differentiated and severity-sensitive responses on seven psychiatric screening instruments with zero specialized configuration. This extends prior work (Westwood 2025) from general surveys to clinical instruments.

**Rating: Incremental.**

The core insight — LLMs can mimic clinical questionnaire responses — is a straightforward extrapolation of established findings. The breadth across seven instruments adds value, but the finding would surprise few researchers familiar with both the LLM-contamination literature and the structure of psychiatric self-report instruments. For JAMA, even in Brief Report format, incremental confirmation of a predictable threat falls below the novelty threshold unless accompanied by either evidence of real-world contamination or a validated detection method.

### Part 2 — Identification and Credibility

**Strengths**: Systematic Cartesian design, breadth of instruments, open data/code, cluster-robust SEs.

**Key threats**: Single model (no generalizability evidence), no human benchmark, prompts contain rich clinical information despite "no specialized configuration" framing, PHQ-9/GAD-7 non-specificity is ambiguous, no item-level analysis, standard inferential statistics applied to deterministic LLM outputs.

### Part 3 — Analyses: Required and Suggested

**Required:**
1. Human benchmark comparison (overlay published clinical norms on figure)
2. Item-level response distribution analysis for at least 2-3 instruments
3. Clarification of statistical inference framework for deterministic LLM outputs
4. Internal consistency reliability (Cronbach's alpha) for synthetic responses
5. Exact prompt template disclosure (in supplement or repository)

**Suggested:**
1. Multi-model comparison (even small-scale with one additional LLM)
2. Cross-instrument correlation matrix compared to known comorbidity patterns
3. Sensitivity analysis varying prompt detail level
4. Discriminant validity analysis between similar conditions

### Part 4 — Literature Positioning

**Notable omissions:**
- Argyle et al. (2023), "Out of One, Many" — foundational silicon sampling paper
- Binz & Schulz (2023) or Aher et al. (2023) on LLMs as simulated participants
- Malingering/symptom validity literature (TOMM, SIMS) — structurally isomorphic problem, entirely absent
- Veselovsky et al. (2023) on detecting LLM-generated survey responses

### Part 5 — Journal Fit and Recommendation

**Recommendation: Revise before sending to referees.**

The paper has clinical relevance and potential impact but three deficiencies would predictably lead to rejection at JAMA: (1) no human benchmark to anchor "clinically plausible," (2) no item-level analysis, and (3) insufficient novelty without detection methods or contamination evidence.

**Best target journals**: JAMA Psychiatry (Brief Report), Clinical Psychological Science (Brief Empirical), American Psychologist, Behavior Research Methods.

### Part 6 — Questions to the Authors

1. You state prompts contained "no information about instrument content" yet the Methods says each prompt included "the current battery's questions with response options." How do you reconcile this?

2. Have you compared item-level response distributions to published norms from clinical samples? Would item profiles look human or stereotyped?

3. If you regenerated all 2106 personas with the same prompts, how much would results change? Have you quantified test-retest reliability?

4. Can you distinguish between the "known comorbidity" interpretation and the "default high depression/anxiety" interpretation of the PHQ-9/GAD-7 results? Do non-clinical personas produce low scores?

5. What evidence do you have that results generalize beyond Gemini 2.0 Flash?

6. Your recommendations (identity verification, triangulation) have been made for over a decade. What specifically about your findings changes the calculus?

7. What is the realistic economic incentive for an adversary to craft clinical personas to infiltrate research studies?

---

## Priority Action Items

**CRITICAL** (must fix — could cause desk rejection or major referee objections):
1. **"Clinically plausible" claim is unanchored** — no benchmark against human clinical data. At minimum, overlay published norms on Figure 1 or reframe language to "exceeding clinical cutoffs" (Agent 3, Agent 6)
2. **Single-model generalization** — title/abstract/conclusions generalize beyond the single model tested. Add explicit caveat in Conclusions (Agent 3, Agent 6)
3. **Causal overclaiming** — "modulated" used for correlational findings; fix in 3 locations (Agent 3)

**MAJOR** (should fix — will likely be raised by referees):
4. **PHQ-9 mean rounding discrepancy** — text says 13.55/13.42, data rounds to 13.58/13.45 (Agent 2)
5. **Missing caveats** — no temperature/sampling parameters reported; no test-retest analysis; "no longer tenable" too strong before study contribution (Agent 3)
6. **"No instrument content" contradiction** — prompts included full item text; clarify what was/wasn't included (Agent 6)
7. **13-cluster SE concern** — small number of clusters for cluster-robust inference; note limitation (Agent 4)
8. **PHQ-9/GAD-7 alternative interpretation** — present both "comorbidity" and "default elevation" explanations (Agent 3)
9. **Missing literature** — malingering/symptom validity literature, Argyle et al. 2023 (Agent 6)

**MINOR** (polish — improves paper quality):
10. **$n$ vs $N$ inconsistency** between Table 1 and Figure caption (Agents 1, 2, 4, 5)
11. **Narrative citation** — "Westwood recently demonstrated" non-standard for numbered citation style (Agent 1)
12. **Terminology drift** — "diagnosis-congruent" vs "target" needs explicit mapping at first use (Agent 2)
13. **"Battery" vs "instrument" conflation** in Results (Agent 2)
14. **Figure panel labels** — add A, B, C labels for easier reference (Agent 5)
15. **Near-verbatim repetition** across Key Points, Abstract Conclusions, and Conclusions section (Agent 1)
16. **"Triviality" editorializing** — the simulation required domain expertise; reframe (Agent 3)
