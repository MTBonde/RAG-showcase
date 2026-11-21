# Sources for the numbers

Every number in this repo is a measurement or a count from recall's own records. The
records are private (they quote the eval questions and name files in my notes), so this
page lists them by name only. Only aggregates are published; no question or prompt text
appears in this repo except the one hardware question used as an example.

The stage column says which point in the work a record or number belongs to: the
earlier attempts in the summer, the time before the first version, the first version,
the review after it, one of the three parts of the current iteration, or the plan for
the next iteration.

## The records

| Short name | What it is | Stage |
|---|---|---|
| Summer plan | The memory-system plan from the summer, with its reviews and what the earlier trial showed | Earlier attempts |
| Decision record | The first version's design and decision record, with its first measured runs and the known misses that started it | First version |
| RAG definitions | Eight official definitions of RAG compared with the first version | First version |
| Diagnosis | What the first version got wrong, each fault with its evidence | After the first version |
| Eval baseline | The repaired eval, run once on the first version's index | After the first version |
| Latency tests | Model load and search times with the model loaded | After the first version |
| Part 1 record | The resident service, and the morning index update (in a section added later) | Part 1 |
| Part 2 record | The hook, the relevance bar and its tuning rounds, the first budget raise to 10 s, keep-warm | Part 2 |
| Part 3 record | Translation, the reranker, the check set (called the held-out set there), the wide lists, the heat breach, the review fixes, the result of the current iteration | Part 3 |
| Design page | The design of the current iteration, each part's acceptance test, the state of each part, the open list and "Next" | Current iteration, all parts |
| Research reports | The two research reports on RAG accuracy, each from a different AI research tool (unchecked); used only for "what the published work says" | Part 3 |
| Explainer | A plain explanation of the system for a new reader | After part 2 |
| Eval reports | The eval reports in the code repo, one file per measured run | First version and current iteration |
| Code | The code repo for the current iteration, its README (including the hook section) and project rules | Current iteration |

## The numbers

| Number | Stage | Source |
|---|---|---|
| Earlier attempts: a quick trial in the summer, where a small English-only embedding model failed on Danish questions against English notes; a full plan later that summer, reviewed and approved, never built | Earlier attempts | Summer plan, its header and "Supersessions"; Decision record, section 3 (embedding model) and section 9 |
| Five known misses where the answer was already in a note, in a little over two weeks this autumn; in one, the memory work was planned from scratch while the summer plan existed | Before the first version | Decision record, section 1 |
| The first version left the choice of when to search to the building session, when the remaining decisions were handed over | First version | Diagnosis, sections 1 and 2 |
| First version: right file among the best 5 for 8 of 21 (hybrid mode); "found" on 19 of 22 ordinary prompts | First version | Eval baseline, summary table |
| Current iteration: right note among the best 5 for 19 of 24 (the README's numbers table) | Part 3 | Part 3 record, Table C1 |
| First version: about 10 s per call, up to 244 s after a reboot; 2.2 GB model downloaded again after every reboot | First version | Design page, "Where we start"; Diagnosis, fault 1 |
| A search with the model loaded: 0.13-0.27 s | After the first version | Latency tests, test 0e |
| Relevance bar tuning: 4 of 21 right and 9 of 22 false in round 1; 10 of 24 right and 0 of 30 false in the final round | Part 2 | Part 2 record, Table 2 |
| Right and wrong pieces both score 0.79-0.86 on similarity | First version | Code README, relevance bar; Diagnosis, fault 13 |
| Budget raised from 2 s to 10 s after answers of 3.7 s and 2.5 s were dropped; 60 s skip after a timeout | Part 2 | Part 2 record, "Budget raised to 10 s" |
| Budget raised again to 20 s (19.5 s for the service) after a prompt was lost at 10.8 s on a machine short of memory | Part 3 | Code README, hook section |
| Keep-warm: 25.8 s after about two hours idle before it; 1.85 s after an hour idle with it | Part 2 | Part 2 record, "keep-warm tick" |
| Morning index update, first run: 10 changed files, 173 s, peak 70 °C | Part 1 | Part 1 record, Table 5 |
| Temperature control: unpaced 85-87 °C; paced peak 78 °C, settling at 65-70 °C | First version | Decision record, section 7b |
| The 80 °C limit is mine | Part 3 | Part 3 record, "The heat breach" |
| Translation: tuning set 10 to 12 of 24, check set 5 to 8 of 12; false 0 to 1 of 30 and 2 to 1 of 8; about 0.3 s and 550 MB | Part 3 | Part 3 record, Table A |
| Review fixes to the insert rule (a Danish word and its translation counted twice; short English or code prompts taken for Danish): 12 to 11 of 24, false 1 to 0 of 30; check set unchanged at 8 of 12 and 1 of 8 | Part 3 | Part 3 record, "Review fixes" (fixes 5 and 6), Table 1 and the paragraph after Table D |
| Target 16: set in the design as part 3's acceptance bar, as 16 of 21 on the set of that time | Design of the current iteration | Design page, "Three slices, each with its test" |
| Reranker: tuning set 12 to 16, check set 8 to 8; service memory 2.1 GB without, 3.1-3.2 GB with (at start); needs about 1.1 GB more; worth trying again with about 1.5 GB more free than during the trial; median 0.6 s (translation only, first run after a restart) to 1.4 s; with little free memory a median of 1.6 s and one prompt of 17 s | Part 3 | Part 3 record, Table B, "The RAM cost showed up", "switched off" |
| Reranker placements: CPU 6.2 s and 3.1 GB more; all on the graphics card 5.9 of 6 GB and a 3.8 s median | Part 3 | Part 3 record, "Placements measured and dropped" |
| Wide list: reranking median 0.76 s at 20 and 5.7 s at 150; right 16 and 17 of 24; check-set false 1 and 3 of 8 | Part 3 | Part 3 record, Tables C2 and C3 |
| Passing on the best 5 once one clears the bar: check set 8 to 9 of 12 for about 800 more characters | Part 3 | Part 3 record, Table C3 and "Shipped" paragraph |
| Heat breach: 80-87 °C for roughly ten minutes; scripts now stop at 79 °C | Part 3 | Part 3 record, "The heat breach" |
| Current iteration: right note inserted 11 of 24 and 8 of 12; false 0 of 30 and 1 of 8; lookup median 1.09 s and 1.00 s, on a machine short of memory and busy | Part 3 | Part 3 record, Table D; the two eval reports of the current iteration's setup |
| Daily-use example: the prompt got nothing at about 11 s when the hook gave up at 9.5 s | Part 3 | Code README, hook section |
| Funnel: right note among the best 5 / 20 / 50 for 19 / 20 / 22 of 24 and 10 / 12 / 12 of 12 | Part 3 | Part 3 record, Table C1 |
| Lever steps in the figure: 10, 12, 16, 11 of 24; 5, 8, 8, 8 of 12; false 0, 1, 0, 0 of 30 and 2, 1, 1, 1 of 8 | Part 3 | Part 3 record, Table 1 |
| Index: about 45,000 pieces from just over 2,200 files | After part 2 | Explainer, section 3 |
| Code size and test count (231 cases) | Current iteration | Code README, test section; line counts of the code files |
| "Published work counts the right text among the best 20"; "published pipelines rerank 100-150 candidates" | Part 3 | Research reports (unverified); Design page, "Next"; Part 3 record, "Wide pools" |
| What the next iteration would try: a test set of 150 questions or more; telling a real question from an ordinary prompt; a one-line pointer when half sure; a fourth and fifth note; a page of the most-asked facts at session start; table rows with their headers; BM25; one right note lost to the cut at three | Next iteration | Design page, "Next"; Part 3 record, "Review fixes" |
| Holding speed on a busy machine: a higher priority, keeping the service out of swap, a more compact search model (one re-index) | Next iteration | Part 2 record, keep-warm section and its open decisions; Diagnosis, section 6 |

## How to read them

- The tuning set is the set the thresholds were tuned on; its numbers are in-sample.
  The check set (a validation set, called the held-out set in the records) is described
  in the README's "How a change is judged"; no threshold is set on it, and a change
  that lowers it is rejected. It is small (12 questions and 8 ordinary prompts).
- The README's numbers table compares like with like in its "best 5" row (8 of 21 and 19 of
  24). The "inserted by itself" row has no first-version figure, because the first
  version inserted nothing by itself.
- The funnel's candidate counts, and the numbers table's "best 5" figure for the current iteration,
  come from the run with translation on, before the review fixes; the funnel's last
  step is the current iteration after them. The fixes lost one question to the
  three-note cut (12 to 11 of 24), as the README's "How a change is judged" says.
