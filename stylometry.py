"""
Signal two: writing style.

Measures sentence-length variation, vocabulary variety, and punctuation.
Returns a score from 0 to 1; higher means more AI-like characteristics.

These are experimental heuristics, not proof of authorship.
"""

import re
import statistics
import unicodedata


def sentences(text: str) -> list[str]:
    """Split text using sentence-ending punctuation."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part for part in parts if part.strip()]


def words(text: str) -> list[str]:
    """Extract lowercase words using the starter's tokenizer."""
    return re.findall(r"[a-z0-9']+", text.lower())


def sentence_length_spread(text: str) -> float:
    """Sentence-length standard deviation divided by mean length."""
    lengths = [
        len(words(sentence))
        for sentence in sentences(text)
        if words(sentence)
    ]

    if len(lengths) < 2:
        return 0.0

    return statistics.pstdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """Unique words divided by total words."""
    tokens = words(text)

    if not tokens:
        return 0.0

    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """Punctuation characters divided by non-whitespace characters."""
    characters = [character for character in text if not character.isspace()]

    if not characters:
        return 0.0

    punctuation_count = sum(
        unicodedata.category(character).startswith("P")
        for character in characters
    )

    return punctuation_count / len(characters)


def style_signal(text: str) -> float:
    """
    Combine three normalized style measures.

    Experimental assumptions:
    - Lower sentence-length variation increases the AI-like score.
    - Lower vocabulary variety increases the AI-like score.
    - Lower punctuation density increases the AI-like score.

    A short sample returns a neutral 0.5 because it supplies too little
    evidence for these measurements.
    """
    tokens = words(text)
    usable_sentences = [
        sentence for sentence in sentences(text) if words(sentence)
    ]

    if len(tokens) < 20 or len(usable_sentences) < 2:
        return 0.5

    spread = sentence_length_spread(text)
    variety = type_token_ratio(text)
    density = punctuation_density(text)

    # Normalize every component to the same 0-to-1 direction.
    spread_score = 1.0 - min(spread, 1.0)
    vocabulary_score = 1.0 - variety
    punctuation_score = 1.0 - min(density / 0.10, 1.0)

    score = (
        0.50 * spread_score
        + 0.30 * vocabulary_score
        + 0.20 * punctuation_score
    )

    return round(max(0.0, min(score, 1.0)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and "
        "provides good results. Users generally find it easy to use "
        "and understand."
    )

    print(f"Sentences: {len(sentences(text))}")
    print(f"Words: {len(words(text))}")
    print(f"Sentence-length spread: {sentence_length_spread(text):.4f}")
    print(f"Vocabulary variety: {type_token_ratio(text):.4f}")
    print(f"Punctuation density: {punctuation_density(text):.4f}")
    print(f"Style score: {style_signal(text):.4f}")
    print("Higher scores indicate more AI-like style characteristics.")