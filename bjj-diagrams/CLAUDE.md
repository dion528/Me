# BJJ Position Diagrams: Project Handoff

## What this is
Labelled diagrams of BJJ positions for **Dion Palmer**: gi white belt, ~18 months, trains twice a week, bigger than most partners, Melbourne.
Output is the **Position Atlas**, a printable A4 PDF. It's a companion to his 98-page *Dion's Jiu-Jitsu Book* (in `reference/`).
Each position gets:
- a diagram
- a numbered control-point checklist
- "Read in your book" page references
- a QR code to a YouTube search

**The goal of the next round is to make the diagrams more understandable at a glance.** Accuracy comes first. Prettier comes second.

## How Dion wants to be worked with
- Act as a ruthless mentor. Be direct and honest over polished. Use trade-facing language with no gloss.
- Stress-test everything. If an approach is weak, say why.
- He learns through if-then decision rules, principles over step lists, and explain-back checks.
- His core problem: he **blanks in dominant positions**, which is a retrieval problem. His fix is the **arrival script**: settle 3 seconds, check where their elbows are, run the default. Diagrams should support that: *what do I check the moment I land here?*

## Files
| File | Role |
|---|---|
| `fig.py` | SVG renderer. `Scene` class: `chain`/`limb` (one polyline per limb with a white halo, so crossings show a gap), `torso`, `blob`, `head`, `mark` (numbered orange marker, remembered for the eye-test ring), `tag`, `arrow`, `mat` (floor line for side views), `svg(eye=n)`. Colours `YOU`/`THEM` plus darker `YOU_FAR`/`THEM_FAR` for limbs that are underneath. `K` scales limb width. `supine()` draws a person on their back (`far=` shades the arms). `figure_html()` renders a single scene or a panel list. |
| `scenes.py` | One function per position, returning `(Scene, [checklist])` or, for sequences and two-view cards, `([(caption, Scene or decision-table), ...], [checklist])`. Helpers: `upright()` (top-down kneeling torso), `side_person()` (side-view figure), `P()` (panel scene with bigger markers). The `SC` list maps name → function. |
| `atlas.py` | Lays out `atlas.html`: intro plus one card per position. Holds the per-position data: view, page refs, YouTube search, one-line idea, `EYE` (eye-test marker + line) and `LAND` (arrival-script default from book p. 8). Panel cards go full width. |
| `build.py` | `python3 build.py` → `build/Position-Atlas.pdf` (Playwright Chromium). |
| `render.py` | Quick preview grid: `python3 render.py scenes out.png "Mount\|K guard"`. **Look at the PNG after every change.** |
| `fonts/` | Fredoka 600/700 woff2 (headings). |
| `reference/` | The complete book (for page numbers), K Guard Study Page, curriculum photo, atlas v1. |

Setup: `pip install -r requirements.txt && python3 -m playwright install chromium`
If a Chromium is already installed but doesn't match the pip Playwright version, point at it: `PW_CHROMIUM=/path/to/chrome python3 build.py` (render.py honours it too).

`reference/` is **not in git** (the repo is public and it holds Dion's book, his academy's curriculum and class notes). Keep it local.

## Visual conventions (keep these consistent)
- **Blue = YOU, grey = THEM.** Every checklist is written from Dion's point of view.
- Top-down ("ceiling camera") unless the card says otherwise. Crab ride is a side view. K guard is a schematic.
- Orange numbered markers must match the checklist order exactly. Keep it to 3–5 markers.
- The numbered markers must sit on the body part the checklist names. If a marker is ambiguous, that's a bug.

## Current state: honest quality rating (round 2)
Round 2 shipped: halo gaps + thinner limbs + darker underneath shade on every card, eye-test ring and callout on every card, arrival-script "Land here" line on mount / side control / back / top half, S-mount as top-down + side view, a new "Cross body headlock: you underneath" card (escapes 68/74/80/81), K guard and crab ride as panel sequences. Atlas is 7 pages, 2 cards a page, no splits.

| Position | Rating | Problem |
|---|---|---|
| Mount, side control, closed guard, back control | Good | Back control hooks redrawn: legs now wrap outside the hips with the heels between their thighs (they used to sit on the thigh) |
| High mount, knee on belly, half guard top, turtle | OK+ | Overlap reads better with halos. Half guard leg tangle is still the busiest picture |
| S-mount | OK | Side view shows the posture. Top-down S still small. Confirm which side the knee-by-head goes on with the coach (drawn on the trapped-arm side) |
| Scarf hold (top) | OK | Head wrap now loops visibly round the head. Leg direction (which leg forward) is approximate: not asserted in the checklist |
| Scarf hold (bottom) | OK | Checklist tied to book escapes. Which exit when (80 vs 81) is left for the coach on purpose |
| K guard | OK- | Now a sequence + decision table. Panel 2 is still a schematic; the study page itself was built without the coach in the room |
| Crab ride | Weak | Side-view stick panels. Correct order and checkpoints, but the inverted figure is cramped and the hook-behind-the-knee can't really be seen from the side |

## Improvement priorities (in order)
1. **Crab ride:** redraw panel 2 bigger, maybe as a 3/4 view, so the insteps behind the knees read.
2. **Get the coach to mark up** S-mount knee side, scarf-hold legs, K guard grips and which headlock exit when. Then fix the drawings.
3. **Submission diagrams** (armbar from mount, head and arm choke, cross collar choke, rear naked choke, triangle) in the same style. Armbar should be a sequence: high mount → S-mount → swing → finish.
4. Half guard top: split the leg tangle into a small inset.

## Technical accuracy rules (these were corrected earlier, so don't regress them)
- **Head and arm choke:** dismount to the side **your head is on**. Their right arm is trapped → step off to their left.
- **Back control:** keep them on your **choking-arm side**. Don't let them slide toward your under-arm side, because that's the side they escape to. Lineages differ; flag that rather than asserting.
- **Seatbelt:** one arm over the shoulder (choking arm), one under. Hooks inside the thighs, feet never crossed.
- Use "hip escape" wording consistently (it's the kids' book term too).
- If a diagram and his coach disagree, the coach wins. Keep that line in the intro.

## Don'ts
- **Don't use AI image generation for the technique diagrams.** It gets grips, limb count and which leg goes where wrong, and a wrong picture is worse than none for a student. Generated art is fine for covers.
- Don't copy photos or stills from instructionals or YouTube (copyright). Use QR codes to link out instead.
- Don't break the page references. If the book changes, re-check the page numbers against `reference/Dions Jiu-Jitsu Book.pdf` with `pdftotext -raw`.

## Page reference map (combined book)
| Topic | Page(s) |
|---|---|
| Arrival script | 8 |
| Mount system | 9 |
| Getting to mount | 21 |
| Curriculum: mount | 42–43 |
| High mount / armbar | 9–10, 28 |
| S-mount | 10, 28–29, 44 (card 31) |
| Side control | 11, 20–21, 50 |
| Knee on belly | 7 |
| Closed guard | 13, 22, 46–47 |
| Top half guard | 8, 13 |
| Back | 12, 32, 54 |
| Turtle | 12, 20 |
| Headlock escapes | 54–55 |
| K guard / crab ride | separate K Guard Study Page |

## Suggested skills in Claude Code
- `frontend-design` for card layout and visual hierarchy.
- `canvas-design` for cover and visual polish only, not technique accuracy.
- `pdf` for merging the atlas into the complete book as Part 6, and for page numbers and bookmarks.
- `bjj-position-diagrams`, if Dion saved it, for the drawing conventions above.

## Definition of done for each change
1. Render the preview PNG and look at it.
2. Ask: could a white belt point to each numbered marker and say what it is, without reading the text?
3. Rebuild the PDF and check that no card splits across pages.
