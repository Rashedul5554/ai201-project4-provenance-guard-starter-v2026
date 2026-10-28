"""Combine signals (Milestone 4); label mapping remains for Milestone 5."""

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
    """TODO: replace placeholder label text in Milestone 5."""
    if score >= config.AI_THRESHOLD:
        return "ai", "PLACEHOLDER — write the high-confidence AI label."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "PLACEHOLDER — write the high-confidence human label."
    return "unsure", "PLACEHOLDER — write the unsure label."


def label_ranges() -> list[tuple[str, str]]:
    """Starter label ranges; finalize wording and boundary notation in Milestone 5."""
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
