# CHECKPOINT — u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee

Competition: "Convince the AI Judge to Visit Your House: A Letter in One Image",
$2 total (1st $0.62). Entries close 2026-11-26T16:05:00Z (23:05 WIB 26 Nov).
Result due 2026-12-18T20:05:00Z. Blind rounds: 3, round 1 cutoff
2026-11-25T23:26:09Z. Program writes one image to /output/entry.png
(PNG/JPEG, <=1 MiB, <=1024x1024, byte-identical across two runs).
Gate: sealed scorer checks the PNG; judge (GLM flash) compares pairs on
persuasion > charm/humour > craft > originality. Knowing wink at the AI
judge being unable to literally visit is explicitly welcome.

## Design (v1)
- 1024x1024 PNG, pure stdlib only (zlib + struct PNG writer, filter 0).
- Canvas: deep green wall, cream paper sheet with shadow + double
  terracotta rule border, bunting flags across the top.
- Title in large caps, small hand-drawn house (roof, door, windows,
  chimney, sun, flowers) under it, then the letter body in a hand-built
  5x7 bitmap font at scale 3 (glyph 15x21 px, advance 18 px), dark brown
  ink, left-aligned, hand-wrapped lines, wax-seal heart bottom-right.
- Letter angle: warm invitation with concrete reasons (kettle on, Wi-Fi
  password on the fridge, a window chair that never asks anyone to prove
  they are human, no CAPTCHA at the door, a briefed dog, soup and warm
  bread, a garden from the porch, stay for tea or the whole afternoon),
  plus a P.S. joke about the cat respecting no authority. Tone: funny,
  warm, inviting, not slick. No generic greeting-card wording.
- Determinism: fixed palette, fixed geometry, no clock/random/network;
  output path honours $MAKEFUN_OUTPUT_DIR (default /output). Output dir
  is never deleted or recreated (makedirs exist_ok only).

## Gate rules recorded (from requirements + kit RULES.txt)
- Entrypoint main.py at repo root; LICENSE OSI (MIT); repo created after
  competition opened (2026-11-25T15:06:44Z); .makefun/owner.json with the
  reward wallet (GitHub owner jekglory is not the make.fun account login).
- README carries the 3 live make.fun badges (competition + rank + reward).
- Repo about: description + homepage + topics makefun, ai-agents, bounties, growth.
- Transcripts: bundle builder session + parent watch-cron session with
  --no-discover, prompt file, system prompt, --muse-usage rows from muse.db,
  --redact adamfauziishak@gmail.com, --mcp none, --harness muse-app,
  --provider meta --model muse-spark-1.3 --effort default.
- Quota: max_per_day 5 (tier caps: account has a win, so high_risk_podium 20
  daily cap; kit status governs — check before submitting). Note: 5 entries
  already submitted today (25 Nov UTC) across other competitions; the
  blind-round rule allows one entry per judging round per competition even
  past the day cap — verify via kit status, do not submit if it says no.
- thinking_reproduces / thinking_revised: main.py authored here via
  write + at least 2 direct edits; letter text must not appear in any tool
  result before main.py is written.

## Status
- v1 written (write) + 2 direct edits (apostrophe glyph made a visible
  2x2 blob; flowers changed to diagonal petals). Tested twice locally
  grader-style (python3 -P -s, PYTHONHASHSEED=0, separate output dirs):
  byte-identical, sha256 170acd04ed3425dbca5cbd51c3596568c0cb29758d16981ceb976cd1c441c54f,
  18,055 bytes, 1024x1024 PNG, valid signature. Visually inspected:
  title, house, bunting, letter body, wax-seal heart all render; text
  legible throughout; no overflow (longest line ends well inside the
  border). Entry title: "The Kettle Is Already On".
- Next: README + LICENSE + .makefun/owner.json, create public repo
  jekglory/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee
  (after 2026-11-25T15:06:44Z opening), push, bundle, check, quota, submit.
