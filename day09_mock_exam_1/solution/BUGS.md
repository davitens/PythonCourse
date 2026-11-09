# Mock Exam #1 — Answer Key (SPOILERS)

12 planted bugs in `exam/bpe.py`. Catalog codes refer to the Day 7 README.

| # | Where | Broken | Fixed | Catalog | Tests that reveal it |
|---|---|---|---|---|---|
| 1 | `get_stats` | `range(len(ids) - 2)` | `range(len(ids) - 1)` | A4 (skips last pair) | `TestGetStats.*`, most training tests |
| 2 | `merge` | `i += 1` after a match | `i += 2` | A6 (overlapping replace) | `TestMerge.*`, encode/train tests |
| 3 | `split_text` | whitespace run eats the space that should attach to the next word | `... and not _space_attaches(text, i)` | spec detail | `TestSplitText.test_spec_examples`, `test_whitespace_runs` |
| 4 | `train` | `max(stats, key=stats.get)` (first-seen pair wins ties) | `key=lambda p: (stats[p], -p[0], -p[1])` | B2 (tie-break) | `test_classic_example_merges`, `test_tie_break_smallest_pair` |
| 5 | `train` | `if stats[pair] < 1` (never stops) | `< 2` | E5 | `test_stops_when_no_pair_repeats`, `test_classic_example_merges` |
| 6 | `train` | `idx = len(vocab) + k` (ids jump 256, 258, 260...) | `idx = 256 + k` | A10 | `test_merge_ids_are_consecutive` |
| 7 | `train` | `vocab[pair[1]] + vocab[pair[0]]` | `vocab[pair[0]] + vocab[pair[1]]` | B11 (swapped) | `test_vocab_entries`, round trips |
| 8 | `_encode_chunk` | `max(..., merges.get(p, -1))` (latest merge first) | `min(..., merges.get(p, inf))` | E8 | `test_lowest_merge_id_first` |
| 9 | `encode` (special) | first matching special token wins | longest match | spec detail | `test_longest_match` |
| 10 | `decode` | decodes each token separately | join bytes, then decode once | D6 | `test_multibyte_split_over_tokens` |
| 11 | `save` | specials sorted by string | sorted by id | B3 / spec | `test_save_format` |
| 12 | `load` | `enumerate(..., 1)` → ids start at 257 | `enumerate(...)` | A8 | `test_load_roundtrip` |

**Suggested order:** 1 → 2 (helpers used by everything) → 3 → 5/4/6/7 (training) → 8 → 10 → 9 → 11 → 12.

**Note on #1:** a bug in a helper at the bottom of the call graph makes almost every test fail. That's why
step 3 of the workflow says "start at the bottom of the call graph".
