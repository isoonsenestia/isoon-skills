---
name: design-feedback-as-oracle
description: Use when a user rejects a UI change as "not matching" or "not working" but your literal reading of the request was already implemented — disambiguate with side-by-side candidates instead of re-guessing.
---

# When Design Feedback Is Rejected, Make the User the Oracle

**Rule:** If the user says "it doesn't match / doesn't work" and you've already implemented the literal interpretation, STOP guessing. Render 2–3 concrete candidate variants side-by-side, label them, and let the user pick. Decouple cheap visual iteration from the expensive commit/rebase step — lock the look on the preview *first*, then propagate once.

**Why:** We implemented "16px padding" literally and *measured* exactly 16px gaps — the user still said the inset "doesn't work." The ambiguity was *what* gets the padding (ticks-within-band vs band-within-card), not the value. A third self-verified guess would share the same blind spot. Rendering candidates A/B/C and asking which matched their Figma settled it in one round (they picked C) and avoided a third wrong rebase cycle.

**How to apply:**
- The moment a literal interpretation is rejected, treat the ambiguity as the user's to resolve, not yours to re-guess.
- Build one preview that renders the realistic candidate layouts together; screenshot and/or ask a single multiple-choice question (AskUserQuestion with ASCII/preview is ideal).
- Only commit / rebase / re-propagate after the look is user-confirmed. Pay the expensive step once.

**Anti-example:** Re-interpreting the feedback yourself, re-implementing, and re-propagating through the whole branch stack on a hunch — paying a full rebase cycle per guess.
