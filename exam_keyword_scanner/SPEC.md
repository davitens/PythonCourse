# Keyword Scanner: Specification

## 1. What the program is for

Suppose you run a website and want to check every comment against a list of 10,000 banned words. The obvious way is to search for
the first word, then search again for the second, and so on. That means reading the comment 10,000 times, which is far too slow
when you have millions of comments.

This program reads the text only **once**, however many keywords you're looking for. It does this with a well-known method called
the **Aho-Corasick algorithm**, named after the two people who published it in 1975. Tools that scan for viruses or search logs for
known patterns use the same idea.

The next three sections explain how it works. You don't have to know the algorithm already. Section 5 onward gives the exact rules
each function must follow.

## 2. Step one: a tree of keywords

First, all the keywords go into a single tree called a **trie**. Each node in the tree stands for some text that the keywords start
with, and keywords that start the same way share the same path.

Take the keywords `he`, `she`, `his` and `hers`:

```text
root ─ h ─ e* ─ r ─ s*        "he" ends at e, "hers" ends at the last s
       │
       └─ i ─ s*              "his"

root ─ s ─ h ─ e*             "she"
```

The stars mark nodes where a keyword ends. Notice that `he`, `his` and `hers` all begin by going through the same `h` node. That
sharing is why a large list of keywords stays manageable.

To search, you start at the root and follow the path one letter at a time as you read the text. If you get to a starred node, you've
just found a keyword.

The question is what to do when the path runs out.

## 3. Step two: fallback links

Suppose you've read `she` and the next letter is `r`. The `she` node has no `r` below it. A simple program would go back to the root
and start again from the next letter of the text, but that means reading letters a second time, and that's what we're trying to avoid.

Look at what you've actually read: `she`. Its last two letters are `he`, and `he` is also a path in the tree! The text you've read could
already be part way through `hers`. So instead of starting over, you can jump straight to the `he` node and carry on from there. The
`r` is there, so you've lost nothing.

That jump is called a **fallback link**. Every node has one, and it points to:

> the node for the **longest ending** of this node's text that is also a path in the tree.

If no ending fits, it points to the root. Here are the links for our example:

| Node | Its text | Endings to try, longest first | Links to |
|---|---|---|---|
| `sh` | sh | `h`: yes | `h` |
| `she` | she | `he`: yes | `he` |
| `hi` | hi | `i`: no | root |
| `his` | his | `is`: no; `s`: yes | `s` |
| `her` | her | `er`: no; `r`: no | root |
| `hers` | hers | `ers`: no; `rs`: no; `s`: yes | `s` |

So when the next letter isn't available, you follow the fallback link and try again. If it's not available there either, you follow
the next link, and so on until you find it or reach the root. It can take **several** jumps. At the root, if there's still no path, you
stay at the root and move on to the next letter of the text.

### Building the links in the right order

A node's link is worked out from its parent's link. To find the link for child `c` reached by letter `x`:

1. Start at the node that the parent's link points to.
2. If that node has a child for `x`, then that child is the link.
3. If not, follow that node's own link and go back to step 2.
4. If you reach the root and it has no child for `x`, the link is the root.

Since a link always points to a **shallower** node, all the shallow links have to exist before the deep ones are worked out. So the nodes
must be processed level by level: first everything at depth 1, then depth 2, and so on. This is called **breadth-first** order, and it's
done with a queue, where you add at the back and take from the front. Nodes at depth 1 always link to the root.

## 4. Step three: keywords hiding inside other keywords

There's one more catch. When you arrive at the `she` node you've found `she`, but you've also found `he`, because `he` is the end of
`she`. The `she` node's star only tells you about `she`.

The fallback link solves this as well, because it points to exactly the ending you need to check. So each node gets a list called its
**outputs**: every keyword that ends at this point.

> A node's outputs are its own keyword, if it has one, followed by the outputs of the node its fallback link points to.

For `she`, that's `["she"]` plus the outputs of `he`, which gives `["she", "he"]`. Since links point to shallower nodes, outputs come out
**longest first**, and the rules below rely on that.

### A full example

Let's search for those four keywords in `ushers`:

| Read | What happens | Now at | Keywords found |
|---|---|---|---|
| `u` | The root has no `u`, so stay at the root | root | |
| `s` | Follow the path | `s` | |
| `h` | Follow the path | `sh` | |
| `e` | Follow the path | `she` | `she`, `he` |
| `r` | `she` has no `r`. Follow the link to `he`, which has one | `her` | |
| `s` | Follow the path | `hers` | `hers` |

Each letter was read once, and all three keywords were found.

## 5. Characters and bytes

The search works on **UTF-8 bytes**, not characters. In UTF-8, a character takes between 1 and 4 bytes, depending on the first byte (the
**lead byte**):

| Lead byte in binary | Bytes in this character | Example |
|---|---|---|
| `0xxxxxxx` | 1 | `a` is `61` |
| `110xxxxx` | 2 | `é` is `C3 A9` |
| `1110xxxx` | 3 | `€` is `E2 82 AC` |
| `11110xxx` | 4 | `😀` is `F0 9F 98 80` |

The bytes after the lead byte always look like `10xxxxxx`. To test a pattern with `x`s in it, use `&` to keep only the fixed bits. For
example, `lead & 0xE0 == 0xC0` keeps the top three bits and checks that they're `110`.

Working with bytes means the tree can stay small, since no node has more than 256 children. It also means that a character can be cut
in half when text arrives in pieces, as section 9 describes.

**However, every position the program reports to the caller counts characters**, unless a function says otherwise. In the text `a€b`,
the `b` is character 2, but it's byte 4. Mixing these two up is an easy mistake, so watch out for it.

### `utf8_offsets(data)`

This function converts byte positions into character positions. Given `bytes`, it returns a list with `len(data) + 1` entries, where
entry `i` is the index of the character that byte `i` belongs to. The extra last entry is the total number of characters, which is what
you need when a match ends at the very end of the text.

```text
utf8_offsets("aé".encode())   ->  [0, 1, 1, 2]
```

`a` is byte 0 and character 0. `é` is bytes 1 and 2, and both belong to character 1. The final 2 is the total.

It raises `ValueError` if a lead byte doesn't fit the table above, or if a character is cut off by the end of the data. It doesn't check
the bytes after the lead byte.

## 6. `Match`

A `Match` describes one keyword found in a text. `Match(keyword, start, end)` has these attributes:

- `keyword`: the keyword as it was originally added
- `start`, `end`: **character** positions, with `end` being one past the last character, so `text[start:end]` is the matching text
- `length`: a read-only property equal to `end - start`

Two `Match` objects are equal when all three values are equal. A `Match` is never equal to something of another type, and it can be put
in a set or used as a dict key. `repr(Match("he", 2, 4))` is `Match('he', 2, 4)`.

## 7. `KeywordScanner`: building

`KeywordScanner(keywords=(), ignore_case=False)` creates a scanner and adds each of the given keywords.

**`add(keyword)`** adds one keyword to the tree:

- If it isn't a `str`, it raises `TypeError`. If it's empty, it raises `ValueError`.
- If the keyword has already been added, nothing happens.
- A scanner can be used, then given more keywords, then used again. New keywords must be found in later searches.

**`keywords()`** returns a new list of the keywords, in the order they were added. Changing that list must not affect the scanner.

**`build()`** works out the fallback links and outputs, as in sections 3 and 4. Callers don't need to call it. Every search must make
sure it has been done, and must not repeat it when nothing has changed.

**`ignore_case=True`** makes the search ignore the difference between upper and lower case, for **ASCII letters only**: `É` and `é` remain
different. Both the keywords and the text are folded. (In Python, `lower()` on a `bytes` object does exactly this, and it never changes
the length.) So `He` and `he` count as the same keyword when `ignore_case` is on, and only the first one is kept. A `Match` still reports
the keyword with the spelling it was added with.

## 8. `KeywordScanner`: searching and rewriting

**`find_all(text)`** returns a list of **every** occurrence of every keyword, as `Match` objects, including ones that overlap. They're
ordered by where they **end**, earliest first. When several end at the same place, the longest comes first. For the example above:

```text
[Match('she', 1, 4), Match('he', 2, 4), Match('hers', 2, 6)]
```

**`contains_any(text)`** returns `True` if any keyword occurs in the text, and `False` otherwise. It should stop as soon as it knows.

**`find_non_overlapping(text)`** returns a list of matches that don't overlap, chosen like this: sort all the matches by start position,
and for matches with the same start, put the longest first. Then go through them in that order, keeping each match that begins at or after
the end of the last one you kept. So two matches can sit right next to each other: `ab` and `cd` in `abcd` are both kept.

**`first(text)`** returns the first match that `find_non_overlapping` would choose, or `None` if there isn't one.

**`count(text)`** returns a dict from each keyword to the number of times it occurs, counting overlaps as `find_all` does. Every keyword is
included, even with a count of 0, in the order the keywords were added.

**`replace(text, replacements)`** returns a new string, with the matches from `find_non_overlapping` replaced. `replacements` is a dict from
keyword to replacement text. A match whose keyword isn't in the dict is left as it is. All the other text is kept unchanged.

**`highlight(text, before="[", after="]")`** returns a new string with `before` and `after` placed around each match from
`find_non_overlapping`. The matched text keeps its original spelling, even when `ignore_case` is on.

**`summary(text)`** returns one line per keyword that was found, written as `keyword: count`. Lines are ordered by count from highest to
lowest, and alphabetically when counts are equal. They're joined with `"\n"`, with no newline at the end. If nothing was found, it returns
`""`.

## 9. `StreamScanner`: text that arrives in pieces

Sometimes text arrives a piece at a time, as with a file too big for memory or data coming over a network. A keyword can be split between
two pieces. So can a single character: the three bytes of `€` might not arrive together. That's one more reason the search works on bytes,
because a scanner just keeps walking the tree from wherever it stopped.

**`scanner.stream()`** returns a new `StreamScanner`. Streams from the same scanner don't affect each other. A stream uses the keywords that
were added before it was created.

**`feed(chunk)`** takes a `bytes` object and returns a list of the matches that **end** inside this chunk, as tuples of
`(keyword, start, end)`. The order within a chunk is the same as in `find_all`. Here, `start` and `end` count **bytes** from the very
beginning of the stream, and not characters, since the stream may be part way through a character.

**`position`** is the total number of bytes fed in so far.

**`reset()`** starts over, as if nothing had been fed in, so a partly read keyword is forgotten and `position` goes back to 0.

```text
>>> st = KeywordScanner(["cat"]).stream()
>>> st.feed(b"a c")
[]
>>> st.feed(b"at")
[('cat', 2, 5)]
>>> st.position
5
```
