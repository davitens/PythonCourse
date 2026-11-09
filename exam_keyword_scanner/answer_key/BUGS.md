# Answer key

16 bugs were planted in `scanner.py`. A corrected copy is in this folder.

| # | Where | What was wrong | The fix | Tests that fail with only this bug |
|---|---|---|---|---|
| 1 | `_char_width` | Mask `0xE0` also matches 4-byte lead bytes, so they are read as 3 bytes wide | Use mask `0xF0` | `TestFindAll.test_emoji`, `TestUtf8Offsets.test_four_byte` |
| 2 | `Match` | `__hash__` is missing. Defining `__eq__` alone makes objects unhashable | Hash the same three fields that `__eq__` compares | `TestMatch.test_hashable` |
| 3 | `KeywordScanner.add` | Duplicates are not ignored | Return early when the key was already seen | `TestAdd.test_duplicates_ignored`, `TestAdd.test_duplicates_ignored_when_folded` |
| 4 | `KeywordScanner.add` | The keyword is not case-folded, so only the text is | Fold the keyword too | `TestAdd.test_duplicates_ignored_when_folded`, `TestIgnoreCase.test_keyword_case` |
| 5 | `KeywordScanner.add` | Adding a keyword does not mark the links as out of date | Set `self._built = False` | `TestAdd.test_add_after_searching`, `TestStream.test_uses_keywords_added_before_streaming` |
| 6 | `KeywordScanner.build` | Takes from the back of the queue, so it walks depth-first and uses links that are not ready | `queue.pop(0)` (breadth-first) | `TestFindAll.test_against_brute_force`, `TestFindAll.test_classic_example`, `TestContainsAny.test_keyword_ending_inside_a_longer_path` and 1 more |
| 7 | `KeywordScanner.build` | Outputs are not inherited through the fallback link, so keywords ending inside others are missed | `child.own + child.fail.outputs` | `TestFindAll.test_against_brute_force`, `TestFindAll.test_classic_example`, `TestContainsAny.test_keyword_ending_inside_a_longer_path` and 2 more |
| 8 | `KeywordScanner._step` | Follows only one fallback link | Use `while` | `TestFindAll.test_against_brute_force`, `TestCount.test_counts_overlaps_and_zeros`, `TestFindAll.test_deep_fallback_links` and 1 more |
| 9 | `KeywordScanner.find_all` | Subtracts the length in characters from a byte offset | Use the length in bytes | `TestFindAll.test_against_brute_force`, `TestFindAll.test_non_ascii_offsets_are_characters` |
| 10 | `KeywordScanner.contains_any` | Only looks at keywords ending exactly at this node | Check `node.outputs` | `TestContainsAny.test_keyword_ending_inside_a_longer_path` |
| 11 | `KeywordScanner.find_non_overlapping` | No "longest first" among matches with the same start | Sort by `(m.start, -m.length)` | `TestNonOverlapping.test_longest_wins_at_same_start` |
| 12 | `KeywordScanner.find_non_overlapping` | Rejects a match that starts exactly where the previous one ended, and any match at position 0 | Use `>=` | `TestNonOverlapping.test_adjacent_matches_are_kept`, `TestRewriting.test_highlight_keeps_original_case`, `TestNonOverlapping.test_leftmost_wins` and 2 more |
| 13 | `KeywordScanner.replace` | The text after the last replacement is dropped | Append `text[pos:]` | `TestRewriting.test_replace`, `TestRewriting.test_replace_keeps_the_tail`, `TestRewriting.test_replace_non_ascii` and 1 more |
| 14 | `KeywordScanner.summary` | Ties are left in insertion order | Sort by `(-count, keyword)` | `TestRewriting.test_summary` |
| 15 | `StreamScanner.feed` | The state is reset at every chunk, so matches across chunks are lost | Keep `self._node` between calls | `TestStream.test_character_split_across_chunks`, `TestStream.test_match_split_across_chunks`, `TestStream.test_streams_are_independent` |
| 16 | `StreamScanner.reset` | `reset` keeps the current state, so a partial match survives | Reset `self._node` as well | `TestStream.test_reset` |

A good order is `utf8_offsets`, then `add` and `build`, then `_step`, then the search functions, and the rewriting functions and the stream last. Nearly everything depends on the first group.
