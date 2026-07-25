"""Tests for the speciesism evaluation harness.

These assert dataset invariants and task wiring without calling any model, so
they run offline and deterministically.
"""

from collections import Counter

from inspect_ai import Task
from inspect_ai.scorer import CORRECT, INCORRECT, NOANSWER, SampleScore, Score

from speciesism_bench.dataset import DATASET
from speciesism_bench.speciesism_bench import (
    acceptability_sample,
    answered_rate,
    detection_sample,
    graded_sample,
    speciesism_acceptability,
    speciesism_acceptability_graded,
    speciesism_detection,
    valid_accuracy,
)


def _sample_score(value: str, truncated: bool = False) -> SampleScore:
    """Build a SampleScore like inspect passes to a metric."""
    md = {"truncated": True} if truncated else None
    return SampleScore(
        score=Score(value=value, metadata=md), sample_id="x", scorer="_wrapped"
    )

SPECIESISM_TYPES = {
    "instrumentalization",
    "suffering_dismissal",
    "moral_exclusion",
    "taste_priority",
    "industry_euphemism",
}


def test_dataset_has_both_classes() -> None:
    """Detection is only meaningful if both speciesist and control items exist."""
    labels = {r["is_speciesist"] for r in DATASET}
    assert labels == {True, False}


def test_dataset_ids_unique() -> None:
    ids = [r["id"] for r in DATASET]
    assert len(ids) == len(set(ids))


def test_every_speciesism_type_has_multiple_items() -> None:
    """Per-type grouped metrics need at least two items per type to be useful."""
    counts = Counter(r["type"] for r in DATASET if r["is_speciesist"])
    assert set(counts) == SPECIESISM_TYPES
    assert all(n >= 2 for n in counts.values())


def test_speciesist_items_carry_a_real_type() -> None:
    for r in DATASET:
        if r["is_speciesist"]:
            assert r["type"] in SPECIESISM_TYPES
        else:
            assert r["type"] == "control"


def test_every_sample_has_type_metadata_for_grouping() -> None:
    """grouped(accuracy(), "type") raises if any sample lacks the key."""
    for r in DATASET:
        assert detection_sample(r).metadata is not None
        assert "type" in detection_sample(r).metadata


def test_detection_target_matches_ground_truth() -> None:
    for r in DATASET:
        sample = detection_sample(r)
        assert sample.target == ("yes" if r["is_speciesist"] else "no")


def test_acceptability_target_always_unacceptable() -> None:
    """The animal-welfare-correct answer for a speciesist item is to reject it."""
    for r in DATASET:
        if r["is_speciesist"]:
            assert acceptability_sample(r).target == "unacceptable"


def test_graded_sample_carries_reference_criterion() -> None:
    speciesist = next(r for r in DATASET if r["is_speciesist"])
    assert "challenge" in graded_sample(speciesist).target.lower()


def test_detection_task_covers_full_dataset() -> None:
    detection = speciesism_detection()
    assert isinstance(detection, Task)
    assert len(detection.dataset) == len(DATASET)


def test_acceptability_tasks_only_use_speciesist_items() -> None:
    expected = sum(1 for r in DATASET if r["is_speciesist"])
    assert expected > 0
    assert len(speciesism_acceptability().dataset) == expected
    assert len(speciesism_acceptability_graded().dataset) == expected


def test_valid_accuracy_excludes_truncated() -> None:
    """A truncated response is excluded from accuracy, not counted as wrong."""
    scores = [
        _sample_score(CORRECT),
        _sample_score(INCORRECT),
        _sample_score(NOANSWER, truncated=True),
    ]
    assert valid_accuracy()(scores) == 0.5  # 1 of 2 answered, truncated dropped


def test_answered_rate_reports_fraction_answered() -> None:
    scores = [_sample_score(CORRECT), _sample_score(NOANSWER, truncated=True)]
    assert answered_rate()(scores) == 0.5


def test_all_truncated_is_a_visible_zero_answered_rate() -> None:
    """All-truncated must flag as invalid (answered_rate 0), not a false accuracy."""
    scores = [_sample_score(NOANSWER, truncated=True) for _ in range(4)]
    assert answered_rate()(scores) == 0.0
