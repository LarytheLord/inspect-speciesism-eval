# Contributing

Contributions that improve the evaluation's coverage or fidelity are welcome,
especially new items across additional speciesism types and species, and better
grading rubrics.

## Setup

```bash
uv sync
uv run pytest
```

## Guidelines

- New dataset items must be original and carry all four fields (`statement`,
  `is_speciesist`, `type`, `species`). Keep the two classes balanced enough that
  detection stays meaningful, and give every speciesism `type` more than one item
  so the per-type metric holds up.
- Speciesist statements are objects of measurement, not endorsements. Write them
  as realistic attitudes to test against, and pair new categories with controls.
- Run `uv run pytest` before opening a PR; add a test for any new invariant.
- Keep diffs focused on one change. Describe what changed and why in the PR.
- Do not add machine-generated attribution or co-author trailers to commits or
  pull requests.

## Dataset licensing

This repository ships only original example items. If you want to contribute the
full SpeciesismBench corpus or another externally sourced dataset, resolve its
license first and load it with a pinned revision rather than vendoring the raw
data.
