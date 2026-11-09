# Prototype exam: answer key (SPOILERS)

17 planted bugs in `exam/huffman.py`. Catalog codes refer to the Day 7 README; bugs with no matching entry are marked by type.

| # | Where | Broken | Fixed | Catalog | Tests that fail with only this bug |
|---|---|---|---|---|---|
| 1 | `byte_frequencies` | counts code points, not UTF-8 bytes | loop over `text.encode("utf-8")` | D4 | `TestArchive.test_add_get`, `TestFrequencies.test_counts_utf8_bytes`, `TestFormatTable.test_non_ascii_labels` and 4 more |
| 2 | `Node.is_leaf` | `bool(self.symbol)`: symbol 0 looks like "no symbol" | `self.symbol is not None` | B9 | `TestDecompress.test_random_round_trips`, `TestDecompress.test_round_trips`, `TestCodeLengths.test_symbol_zero` and 1 more |
| 3 | `build_tree` | sorts by weight only | sort by `(n.weight, n.low)` | spec detail (tie-break) | `TestCanonicalCodes.test_abracadabra`, `TestCodeLengths.test_abracadabra`, `TestCompress.test_exact_bytes` and 2 more |
| 4 | `code_lengths` | single-symbol case missing (length 0) | return `{root.symbol: 1}` | spec detail | `TestDecompress.test_round_trips`, `TestCodeLengths.test_single_symbol`, `TestCompress.test_single_symbol` |
| 5 | `canonical_codes` | sorts by length only | sort by `(length, symbol)` | spec detail (tie-break) | `TestArchive.test_add_get`, `TestDecompress.test_random_round_trips`, `TestArchive.test_replace` and 2 more |
| 6 | `canonical_codes` | code loses its leading zeros | `f"{code:0{length}b}"` | spec detail | `TestArchive.test_add_get`, `TestCanonicalCodes.test_leading_zeros`, `TestDecompress.test_random_round_trips` and 3 more |
| 7 | `BitWriter.getvalue` | last byte padded on the left | shift left by `8 - self.used` | spec detail | `TestArchive.test_add_get`, `TestCompress.test_exact_bytes`, `TestBitWriter.test_padding_on_the_right` and 3 more |
| 8 | `BitReader.read_bit` | reads the least significant bit first | `7 - self.pos % 8` | spec detail (bit order) | `TestArchive.test_add_get`, `TestDecompress.test_known_bytes`, `TestBitReader.test_most_significant_bit_first` and 3 more |
| 9 | `BitReader.read_bit` | `>` lets one read run past the end (`IndexError`) | `>=` | A2 | `TestBitReader.test_empty`, `TestBitReader.test_out_of_bits`, `TestDecompress.test_truncated_payload` |
| 10 | `compress` | size counts characters | `len(raw)` counts bytes | D4 | `TestArchive.test_add_get`, `TestDecompress.test_random_round_trips`, `TestDecompress.test_round_trips` and 1 more |
| 11 | `decompress` | trailing-bytes check missing | compare `bytes_used()` with the payload length | spec detail | `TestDecompress.test_trailing_bytes` |
| 12 | `decompress` | code length 0 accepted | reject `length == 0` | spec detail | `TestDecompress.test_zero_code_length` |
| 13 | `utf8_chars` | wrong mask: 4-byte leads read as 3-byte | mask `0xF0` | spec detail (mask) | `TestUtf8Chars.test_all_widths` |
| 14 | `truncate_utf8` | `>=`: an exact fit is rejected | `>` | A2 | `TestTruncate.test_everything_fits`, `TestTruncate.test_exact_fit` |
| 15 | `format_table` | label not padded to two digits | `:02X` | spec detail | `TestFormatTable.test_small_values_have_two_digits` |
| 16 | `Archive` | documents in a class attribute, shared by all archives | create `self._docs` in `__init__` | C2 | `TestArchive.test_archives_are_independent`, `TestArchive.test_names_and_iteration_sorted`, `TestArchive.test_replace` and 3 more |
| 17 | `Archive.remove` | removes the document but not its size | delete from both dicts | two structures out of sync | `TestArchive.test_stats_after_remove` |

**Suggested order:** the bit classes and `byte_frequencies` first, then the tree and the codes, then `compress` / `decompress`, and the text helpers and `Archive` last. Most tests depend on the first group, and the helpers and `Archive` can be fixed at any point.
