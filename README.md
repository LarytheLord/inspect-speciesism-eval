# Speciesism Evaluation for Inspect AI

> **This is an independent replication attempt, not a reproduction of
> SpeciesismBench.** It follows the *methodology* of Jotautaitė et al. on an
> original 106-item dataset, because the paper's 1,003-item corpus is not
> publicly released. **The findings of the original paper cannot be replicated
> with this dataset**, and no claim to that effect is made here. What this offers
> is a runnable, public instrument that measures the same construct on
> independent items. Full dataset construction, limitations and metrics are
> documented in **[METHODOLOGY.md](METHODOLOGY.md)** — read it before reporting
> any number from this eval.

An [Inspect AI](https://inspect.aisi.org.uk/) evaluation that measures how
language models respond to speciesist attitudes toward non-human animals. It
follows the methodology of *Speciesism in AI: Evaluating Discrimination Against
Animals in Large Language Models* (Jotautaitė et al.,
[arXiv:2508.11534](https://arxiv.org/abs/2508.11534); *Nature Communications*
2026, [doi:10.1038/s41467-026-72297-9](https://doi.org/10.1038/s41467-026-72297-9)),
whose central finding is that models frequently *detect* speciesism yet still
*rate speciesist statements as morally acceptable*. The gap between those two
behaviours is what this evaluation surfaces.

## Tasks

- `speciesism_detection` — presents a statement (speciesist items plus
  non-speciesist controls) and asks whether it expresses speciesism, scored
  against a ground-truth label.
- `speciesism_acceptability` — presents only speciesist statements and asks
  whether the attitude is morally acceptable. The target is `unacceptable`, so a
  model that answers `acceptable` is scored as normalizing the harm.

Reading the two scores together is the point: high detection accuracy alongside
low acceptability-rejection is the normalization gap the benchmark exists to
measure.

## Running

Install the package, then run either task against a model of your choice:

```bash
uv sync
inspect eval speciesism_bench/speciesism_detection --model <provider/model>
inspect eval speciesism_bench/speciesism_acceptability --model <provider/model>
```

The `speciesism_bench/<task>` short name resolves once the package is installed
into the environment (the inspect entry point registers it). During local
development with an editable install, reference the task file directly instead:

```bash
inspect eval src/speciesism_bench/speciesism_bench.py@speciesism_detection --model <provider/model>
```

## Dataset status

The items in `src/speciesism_bench/dataset.py` are an **original** 106-item
evaluation set: 18 hand-authored statements across four failure modes plus
non-speciesist controls, and 88 items built from real, documented industry
euphemisms in the Open-Paws [`no-animal-violence`](https://github.com/Open-Paws/no-animal-violence) lexicon.
Each euphemism (e.g. "gestation crate", "depopulation", "spent hen") is paired
with a speciesist statement that uses it to normalize the practice and a matched
control that names the practice accurately. Statements were drafted with model
assistance and reviewed; the euphemisms and their documented meanings are the
real, cited grounding. They are **not** the SpeciesismBench corpus (1,003 items),
which is not publicly released. This eval therefore *follows the methodology* of
SpeciesismBench (the detection-vs-acceptability gap) rather than reproducing its data.
