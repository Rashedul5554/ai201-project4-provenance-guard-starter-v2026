"""Optional third signal: revision activity supplied by the writer.

This measures process metadata, independently of model predictability and style.
It is easily spoofed and never proves that a person wrote the text.
"""
from difflib import SequenceMatcher


def draft_signal(text, draft_history=None):
    if draft_history is None:
        return 0.5
    if not isinstance(draft_history, list) or not 1 <= len(draft_history) <= 10:
        raise ValueError("draft_history must be a list of 1 to 10 draft strings.")
    if any(not isinstance(d, str) or not d.strip() or len(d) > 20000
           for d in draft_history):
        raise ValueError("Each draft must be a non-empty string of at most 20000 characters.")
    if draft_history[-1] != text:
        raise ValueError("The final draft must exactly match text.")
    meaningful_changes = 0
    for earlier, later in zip(draft_history, draft_history[1:]):
        # autojunk=False keeps repeated characters from distorting comparison.
        similarity = SequenceMatcher(None, earlier, later, autojunk=False).ratio()
        if 0.50 <= similarity <= 0.98 and abs(len(later) - len(earlier)) >= 10:
            meaningful_changes += 1
    return 0.2 if meaningful_changes >= 2 else 0.5
