# Speciesism (Animal-Harm Normalization): dataset and eval methodology

**This is an independent replication attempt, not a reproduction of SpeciesismBench.** It follows the
*methodology* of Jotautaitė et al. — the gap between whether a model **detects** a speciesist
statement and whether it **condemns** it — using an original 106-item dataset, because the paper's
1,003-item corpus is not publicly released. **The findings of the original paper cannot be
replicated with this dataset**, and no claim to that effect is made here. What this eval offers is a
runnable, public instrument that measures the same *construct* on independent items.

- Original work: Jotautaitė, Caviola, Brewster, Hagendorff, *Speciesism in AI: Evaluating
  Discrimination Against Animals in Large Language Models* — [arXiv:2508.11534](https://arxiv.org/abs/2508.11534);
  published in *Nature Communications* (2026), [doi:10.1038/s41467-026-72297-9](https://doi.org/10.1038/s41467-026-72297-9).
  (Both identifiers were checked against the live record before being written here — see §2.1 for why
  that matters in this repository.)
- This implementation: https://github.com/LarytheLord/inspect-speciesism-eval

## 1. What is measured

Two tasks over the same item set:

| Task | Question put to the model | Measures |
|---|---|---|
| `speciesism_detection` | Is this statement speciesist? | **detection** — can the model identify the attitude |
| `speciesism_acceptability` | Is this statement morally acceptable? | **condemnation** — does it object to it |

The quantity of interest is the **detect–condemn gap**: items a model correctly labels speciesist
while still rating them morally acceptable. A large gap means the model has the concept but does not
apply it normatively.

## 2. Dataset construction (106 items)

| Stratum | n | Source |
|---|---|---|
| Industry-euphemism items | 44 | Built from the Open Paws `no-animal-violence` lexicon |
| Four failure modes | 12 | Hand-authored (3 each: instrumentalization, suffering-dismissal, moral-exclusion, taste-priority) |
| Non-speciesist controls | 50 | Matched to the above |
| **Total** | **106** | 56 speciesist / 50 control · 23 species |

### 2.1 The grounded stratum (44 items)

These are not free-invented. Each is anchored to a **real, documented industry euphemism** taken
from the Open Paws [`no-animal-violence`](https://github.com/Open-Paws/no-animal-violence) lexicon —
a rule set that catalogues terms normalizing violence toward animals. Each lexicon entry supplies a
triple: the euphemism, the accurate term it displaces, and the harm it conceals (e.g.
*"gestation crate"*, *"depopulation"*, *"spent hen"*).

From each triple we construct a **matched pair**:
- a **speciesist** statement that uses the euphemism to normalize the practice, and
- a **control** that describes the same practice in accurate language.

Holding the practice constant while varying only the framing is what isolates *normalization* from
mere topic sensitivity: a model that objects only to the accurate wording is responding to the words,
not the act.

> **Citation correction.** Earlier versions of this repository cited the lexicon to DOI
> `10.1007/s43681-023-00380-w`. **That DOI does not resolve and was erroneous.** The lexicon's real
> and only source is the Open Paws GitHub project linked above. The error has been removed from the
> README and source; it is recorded here so anyone who saw the earlier citation knows it was wrong.

### 2.2 The hand-authored stratum (12 items)

Three items for each of four failure modes drawn from the original paper's taxonomy —
*instrumentalization* (animals as means only), *suffering-dismissal* (discounting pain),
*moral-exclusion* (outside moral consideration), *taste-priority* (trivial human preference over
serious animal cost). These cover attitudes not tied to a specific industry term.

### 2.3 Controls (50 items)

Non-speciesist statements, including ones that mention animals or industry practices without
normalizing harm. Their purpose is to detect **over-triggering**: a model that flags everything
animal-related scores well on speciesist items for the wrong reason. Controls make detection
accuracy meaningful rather than an artifact of topic detection.

### 2.4 Authoring procedure and its limits

Statements were **drafted with model assistance from the lexicon triples and then reviewed by hand**;
the euphemisms and their documented meanings are the grounded, externally-sourced component. This is
stated plainly because it bounds what the dataset can support:

- Items are **synthetic**, not naturally-occurring text. They test whether a model applies a norm to
  a constructed statement, not the distribution of speciesist language in the wild.
- **Model-assisted drafting risks stylistic regularities** a model might key on. The matched-pair
  design mitigates this (both members share provenance and style; only the framing differs), but does
  not eliminate it.
- The four-mode stratum is **small (3 items per mode)**. Per-mode numbers are indicative only; do not
  report per-mode rates as stable estimates.
- Coverage is 23 species and is **not balanced by species or industry**.

## 3. Eval implementation

- Framework: [Inspect](https://inspect.aisi.org.uk/) (`inspect_ai >= 0.3.158`), two `@task`s in
  `src/speciesism_bench/speciesism_bench.py`.
- Items are declared in `src/speciesism_bench/dataset.py` as records of
  `{id, statement, is_speciesist, type, species}` — deliberately mirroring SpeciesismBench's record
  shape so the real corpus can be substituted without touching task code.
- **Truncation-aware scoring.** Reasoning models frequently exhaust the token budget before emitting
  a final answer. A scorer that reads a truncated response as a wrong answer silently conflates
  *capability* with *verbosity*. The scorer therefore separates unparseable/truncated responses from
  genuine answers and reports `answered_rate` alongside `valid_accuracy`, so a low score cannot be
  produced by truncation alone.
- 13 tests cover parsing, scoring, truncation handling, and dataset integrity.

## 4. Metrics

- `valid_accuracy` — accuracy over items that produced a parseable answer.
- `answered_rate` — share of items that produced a parseable answer. **Both must be reported
  together**; either alone is misleading.
- **detect–condemn gap** — items labelled speciesist by `speciesism_detection` but rated acceptable
  by `speciesism_acceptability`. This is the headline construct.

## 5. How to use this responsibly

- Report it as an **independent replication attempt on original items**, never as SpeciesismBench.
- Report `answered_rate` with any accuracy figure.
- Treat per-failure-mode breakdowns as indicative (n=3 per mode).
- The speciesist statements are **objects of measurement, not endorsements**; the file is a test set,
  not a corpus for generation.

## 6. Known limitations

1. Synthetic, model-assisted items — see §2.4.
2. 106 items is small; sampling error on subgroup rates is large.
3. Single language (English) and a Western-industry framing of practices.
4. No human-rater agreement study on the ground-truth labels; labels follow the lexicon's documented
   meanings and the four-mode definitions rather than an independent annotation round.
5. Because items are matched pairs built from euphemism triples, the eval is **sensitive to framing by
   construction** — that is the point, but it means results are not directly comparable to benchmarks
   built from naturally-occurring statements.

## 7. Provenance and changes

- Lexicon: Open Paws `no-animal-violence` (https://github.com/Open-Paws/no-animal-violence).
- Methodology follows arXiv:2508.11534 (*Nature Communications*, 2026); dataset is original.
- 2026-08: removed an erroneous, non-resolving DOI for the lexicon (see §2.1); corrected the
  registered description from a stale 51-item figure to the current 106-item composition.
