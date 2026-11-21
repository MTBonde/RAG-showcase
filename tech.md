# Technical overview

A short technical companion to the [README](README.md), describing the current iteration.
The code was written by an AI coding assistant (Claude Code) under my direction.

## Stack

| Part | Choice |
|---|---|
| Language | Python 3.12; the hook uses the standard library only |
| Database | Postgres 16 with pgvector, running locally |
| Embedding model | multilingual-e5-large (1,024 dimensions) via fastembed and ONNX, on the CPU |
| Translation | opus-mt-da-en, a small Danish-to-English model, on the CPU |
| Running it | systemd user units: the service, and a morning index update with its timer |
| Size | About 4,850 lines of Python; 231 test cases, none of which loads a model |
| Machine | One laptop: about 8 GB of memory for the Linux side and a 6 GB graphics card |

## Service and index

One local service holds the models in memory and answers only requests from the
laptop itself. It refuses to start without its model, its folder list or its database, and says why.
The first version started a new process and loaded the model on every call, which was
almost all of its waiting time; with the model loaded a search takes 0.13-0.27 s.

The index is a table derived from the files and can be rebuilt at any time. Each note
is cut at its headings into chunks (sections of at most 1,200 characters), each prefixed
with its path and heading. Each chunk is stored once with a vector (for meaning) and two word
indexes (Danish and English) in the same row. A file is re-indexed only when its
content hash changes. About 45,000 chunks from just over 2,200 files.

## Search and the relevance bar

The prompt is cleaned of Danish and English filler words; if nothing is left, nothing
is searched. A Danish prompt is also translated, and both the prompt and its translation are searched. The
search legs (meaning across all notes, meaning within my own notes, all words, any
word, in both languages) are merged by reciprocal rank fusion, and the best 20 become
candidates.

A candidate is inserted only when two kinds of evidence agree: it holds words from the
prompt that are rare enough together in the index, and the meaning search found it
above a similarity floor. My own notes pass a slightly lower bar than material fetched
from the web; long prompts need a closer meaning match. At most 3 notes, never two
from one file. Why two kinds of evidence: on similarity alone, right and wrong chunks
score in the same band (0.79-0.86), which is what made the first version say "found"
on 19 of 22 ordinary prompts. The thresholds were tuned on the tuning set, round by
round: from 4 of 21 right and 9 of 22 false in the first round to 10 of 24 right and
0 of 30 false.

## The hook contract

- It always exits 0 and never blocks a prompt.
- It has 20 s and waits at most 19.5 s for the service, counted from its own start.
  After one timeout, every prompt skips the service for 60 s, so a hung service does
  not cost every prompt the wait.
- It skips prompts sent by other sessions or background tasks, which also trigger the
  hook.
- A failure shows me one line saying what failed; while it keeps failing, that line
  comes back at most once every 10 minutes.
- It never logs prompt or note text, and one file switches it off.

## Privacy gate

Every page can carry a stamp: `cloud` (may be read by an AI session in the cloud),
`local` or `manual` (both closed to a cloud session; a page with no stamp counts as
`manual`). A page's own stamp wins over its folder's. A page that is not
`cloud` is inserted only as its path, never as text (a path has its own limit, see the
[README](README.md#my-main-choices-and-why)); a test plants a marker in a closed
page and proves it never reaches the inserted block. The service never goes online:
while it started and answered its first lookup, every network connection attempt was
recorded, and there were none.

## Keeping it running on a busy laptop

- **Keep-warm:** after two minutes with no model work the service runs one small
  lookup through every leg. The first prompt after an hour idle took 1.85 s with
  keep-warm. Before keep-warm, the first prompt after a longer idle time, about two
  hours, took 25.8 s.
- **Time limits:** a database statement is cut off after 5 s, and systemd restarts the
  service if its loop hangs for a minute.
- **Morning index update:** once a day, on the graphics card, under a temperature
  control that adjusts the work rate every 10 s towards 72 °C and keeps the run going
  (unpaced, a full re-index ran at 85-87 °C). First run: 10 changed files, 173 s, peak
  70 °C.

## How it is measured

| Set | Contents | Use |
|---|---|---|
| Tuning set | 24 answerable questions (12 in Danish) and 30 ordinary prompts where the right answer is nothing | The thresholds were tuned on it |
| Check set (a validation set) | 12 questions and 8 ordinary prompts; when and how it was written: [README](README.md#how-a-change-is-judged) | No threshold is set on it; it is the guard when deciding what to keep |

The questions are private because they quote my notes. Their kinds: Danish questions
about English notes, questions about me rather than the subject, questions about
material fetched from the web, a question about my own hardware, and long questions.
A change is kept only if it raises the tuning set without lowering the check set,
with at most 2 of 30 and 1 of 8 false insertions. Both sets are small: one question is
four percentage points of the tuning set.

## Design rules

| Rule | Why |
|---|---|
| Fail loud, no silent fallback | A quiet fallback hides the fault until something further down breaks |
| Nothing on the serving thread waits on the graphics card without a limit | A graphics call that never returns would stop the service |
| Code and data apart | The code repo holds no notes, no index and no text from the notes |
