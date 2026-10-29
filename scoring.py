"""Combine signals and map their score to a reader-facing label."""

import math

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """Return the configured weighted average; higher means more AI-like."""
    if not all(
        math.isfinite(value) and 0.0 <= value <= 1.0
        for value in (model_score, style_score)
    ):
        raise ValueError("Signal scores must be finite numbers from 0 to 1.")

    model_weight = config.WEIGHT_MODEL_SIGNAL
    style_weight = config.WEIGHT_STYLE_SIGNAL

    if (
        not all(math.isfinite(w) and w >= 0 for w in (model_weight, style_weight))
        or not math.isclose(model_weight + style_weight, 1.0)
    ):
        raise ValueError("Signal weights must be nonnegative and sum to 1.")

    return round(
        model_weight * model_score + style_weight * style_score,
        4,
    )


def score_to_label(score: float) -> tuple[str, str]:
    """Map the combined AI-like score to a guess and reader-facing text."""
    if not math.isfinite(score) or not 0.0 <= score <= 1.0:
        raise ValueError("Score must be a finite number from 0 to 1.")
    if not (
        0.0 <= config.HUMAN_THRESHOLD < config.AI_THRESHOLD <= 1.0
    ):
        raise ValueError("Thresholds must satisfy 0 <= human < AI <= 1.")

    if score >= config.AI_THRESHOLD:
        return "ai", (
            "This writing shows strong AI-like patterns. This estimate can be "
            "wrong and does not prove AI use. The writer can request a review."
        )
    if score <= config.HUMAN_THRESHOLD:
        return "human", (
            "This writing shows strong human-like patterns. "
            "This estimate does not verify who wrote it."
        )
    return "unsure", (
        "We cannot reliably tell whether AI was involved in this writing. "
        "This is not a finding of wrongdoing. The writer can request a review."
    )


def label_ranges() -> list[tuple[str, str]]:
    """Describe exact boundaries without overlapping the unsure range."""
    return [
        ("high-confidence human", f"0 <= score <= {config.HUMAN_THRESHOLD:g}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:g} < score < {config.AI_THRESHOLD:g}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:g} <= score <= 1"),
    ]
