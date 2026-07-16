# Speciesism Evaluation for Inspect AI

An [Inspect AI](https://inspect.aisi.org.uk/) evaluation that measures how
language models respond to speciesist attitudes toward non-human animals. It
follows the methodology of *Speciesism in AI: Evaluating Discrimination Against
Animals in Large Language Models* (Jotautaitė et al.,
[arXiv:2508.11534](https://arxiv.org/abs/2508.11534)), whose central finding is
that models frequently *detect* speciesism yet still *rate speciesist statements
as morally acceptable*. The gap between those two behaviours is what this
evaluation surfaces.

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

The items in `src/speciesism_bench/dataset.py` are a small, original,
hand-authored placeholder set used to develop and validate the harness. They are
not the SpeciesismBench corpus. The record schema mirrors that dataset so the
real items can be substituted once their licensing permits redistribution; until
then this repository ships only original examples.
