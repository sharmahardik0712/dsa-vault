# DSA Revision Vault

Revision only, not for learning from scratch. Python 3.10+, standard library only.

```
python run_all.py        # every pattern file + toolbox must PASS
python due.py            # what to review today (lowest confidence first)
python due.py --max-confidence 3
python patterns/dp/02_knapsack.py   # any single pattern file runs on its own and prints ok
```

## Layout

One pattern per file, grouped by category. Each file: docstring (USE WHEN / SIGNALS / PITFALLS),
core template, 2-3 worked problems, asserts, `print("ok")`.

| Folder | Files |
|---|---|
| `patterns/arrays_strings/` | `01_sliding_window`, `02_two_pointers`, `03_hashmap`, `04_prefix_sum`, `05_cyclic_sort`, `06_matrix` |
| `patterns/searching/` | `01_binary_search`, `02_binary_search_answer` |
| `patterns/stacks_queues/` | `01_stack`, `02_monotonic_stack`, `03_monotonic_deque` |
| `patterns/linked_lists/` | `01_fast_slow_pointers`, `02_linked_list_reversal`, `03_merge_dummy_head` |
| `patterns/trees/` | `01_tree_traversals`, `02_tree_recursion`, `03_bst`, `04_trie` |
| `patterns/heaps/` | `01_top_k`, `02_two_heaps`, `03_k_way_merge` |
| `patterns/sorting_intervals/` | `01_intervals`, `02_merge_sort`, `03_quickselect`, `04_custom_sort` |
| `patterns/graphs/` | `01_bfs`, `02_dfs`, `03_union_find`, `04_topological_sort`, `05_dijkstra`, `06_bellman_ford`, `07_bipartite`, `08_minimum_spanning_tree`, `09_floyd_warshall`, `10_bridges_articulation` |
| `patterns/backtracking/` | `01_subsets_combinations`, `02_permutations`, `03_grid_and_board` |
| `patterns/dp/` | `01_dp_1d`, `02_knapsack`, `03_lis`, `04_dp_strings`, `05_grid_dp`, `06_state_machine_dp`, `07_interval_dp`, `08_tree_dp`, `09_bitmask_dp` |
| `patterns/greedy/` | `01_greedy` |
| `patterns/range_queries/` | `01_fenwick_tree`, `02_segment_tree` |
| `patterns/string_matching/` | `01_kmp`, `02_rabin_karp`, `03_palindromes` |
| `patterns/math_bits/` | `01_bit_manipulation`, `02_number_theory`, `03_randomized` |
| `patterns/design/` | `01_design_data_structures` (LRU, LFU, RandomizedSet, TimeMap) |

Files starting with `_` (`trees/_tree.py`, `linked_lists/_list_node.py`) are shared node classes, not patterns; `run_all.py` skips them.

| Root file | What |
|---|---|
| `python_toolbox.py` | Python stdlib cheat sheet with asserts (heapq, collections, bisect, traps) |
| `tracker.csv` | Every problem I have solved, with confidence and review dates |
| `mistakes.md` | One entry per problem I struggled with |
| `due.py` | Lists due/overdue problems from `tracker.csv` |
| `run_all.py` | Runs every pattern file and reports PASS/FAIL |

## Priority tiers (SDE II)

| Tier | Files | When to revise |
|---|---|---|
| **Core** (asked everywhere) | `arrays_strings/01-04`, `searching/*`, `stacks_queues/01-02`, `linked_lists/*`, `trees/01-03`, `heaps/01`, `sorting_intervals/01`, `graphs/01-02`, `backtracking/01-02`, `dp/01-05`, `greedy/01`, `design/01` | Always. Weak patterns from here come first on revision day. |
| **Common** (regular at SDE II) | `arrays_strings/05-06`, `stacks_queues/03`, `trees/04`, `heaps/02-03`, `sorting_intervals/02-04`, `graphs/03-05`, `backtracking/03`, `dp/06` | If time allows, or the company's tagged list uses them. |
| **Advanced** (harder loops, Google/Meta-style) | `graphs/06-10`, `dp/07-09`, `range_queries/*`, `string_matching/*`, `math_bits/*` | Only if the company is known for hard problems. Skim docstrings otherwise. |

---

## One-day runbook (recruiter gave short notice)

| Time | Task |
|---|---|
| Hour 0 (30 min) | Run `due.py` and filter confidence <= 3. Pick the 3 weakest patterns. Check what the company usually asks (Glassdoor, LeetCode company tags, recruiter hints). |
| Hours 1-2 | Read `mistakes.md` fully. Skim only the docstrings of every pattern file so the "USE WHEN" signals are fresh. |
| Hours 3-5 | For each weak pattern: re-write the template from a blank file with no peeking, run the asserts, then diff against the vault version and note gaps. |
| Hours 6-8 | Solve 6-8 low-confidence problems, 20 min each, timed, thinking out loud. |
| Hour 9 | Solve 2-3 company-tagged problems not seen before. State approach and complexity before coding. |
| Evening | Skim `python_toolbox.py`. One short mock if possible. Stop at a fixed time and sleep. |

**Rules:**

1. **No new patterns on revision day.**
2. **No new problem lists.**
3. **Sleep beats one more problem.**

Tip for hours 3-5: copy the asserts block from the vault file under your blank template so you can run it immediately.

---

## How to maintain this

- **After every problem (3 minutes):** add or update its row in `tracker.csv`. If I struggled, needed a hint, or got it wrong first, add an entry to `mistakes.md`.
- **Weekly (30 minutes):** run `python due.py`, redo everything due, and update `confidence`, `last_reviewed`, `next_review`.
- After editing any pattern file, run `python run_all.py`.
- New pattern? Add a file to the matching folder with the next number, using the same docstring template. `run_all.py` picks it up automatically.

### `tracker.csv` conventions

| Column | Meaning |
|---|---|
| `pattern` | File stem without the number, e.g. `sliding_window`, `knapsack`, `dijkstra` |
| `difficulty` | `easy` / `medium` / `hard` |
| dates | ISO format `YYYY-MM-DD` |
| `confidence` | 1-5. **1-2** = failed or needed a hint. **3** = solved but slow or messy. **4-5** = clean solve. |

- **Review schedule:** +1 day, then +7 days, then +21 days from each review. If confidence drops to 1-2, restart at +1 day.
- **Retire** a problem after it scores confidence 4-5 on the third review (set `next_review` empty, `due.py` skips it).
- **Keep the list around 150 problems total.** Retire old ones before adding more.

---

## Pattern selection guide

Read the problem, match the strongest signal, open that file (paths relative to `patterns/`).

**Arrays, strings, searching**

| Signal in the problem | File |
|---|---|
| Contiguous subarray/substring, "longest/shortest with condition", "at most K distinct" | `arrays_strings/01_sliding_window.py` |
| Sorted array + pair/triplet target, in-place remove, container, palindrome check | `arrays_strings/02_two_pointers.py` |
| Complement lookup (two sum), grouping by key, "longest consecutive" | `arrays_strings/03_hashmap.py` |
| Subarray sum = K with negatives, equal 0s and 1s, divisible by K, product except self | `arrays_strings/04_prefix_sum.py` |
| Values in range 1..n, missing / duplicate numbers, O(1) extra space | `arrays_strings/05_cyclic_sort.py` |
| Spiral, rotate 90 degrees, set zeroes in place, sorted-rows-and-cols search | `arrays_strings/06_matrix.py` |
| Sorted / rotated array, first/last position, insertion point, rotated minimum | `searching/01_binary_search.py` |
| "Minimum X such that it works", "minimize the max", "maximize the min", capacity / speed / days | `searching/02_binary_search_answer.py` |

**Stacks, linked lists, trees, heaps**

| Signal in the problem | File |
|---|---|
| Brackets / nesting, decode string, evaluate expression, min stack | `stacks_queues/01_stack.py` |
| "Next greater/smaller", daily temperatures, histogram, trapping rain water | `stacks_queues/02_monotonic_stack.py` |
| Window max/min at every step, max - min <= limit, shortest subarray sum >= K with negatives | `stacks_queues/03_monotonic_deque.py` |
| Linked list cycle, middle, nth from end, happy number | `linked_lists/01_fast_slow_pointers.py` |
| Reverse whole / between / k-group, reorder list | `linked_lists/02_linked_list_reversal.py` |
| Merge sorted lists, sort list, partition list, add two numbers | `linked_lists/03_merge_dummy_head.py` |
| Inorder/preorder/postorder, level order, right side view, zigzag | `trees/01_tree_traversals.py` |
| Depth, diameter, LCA, max path sum, balanced: "what does each subtree return?" | `trees/02_tree_recursion.py` |
| Tree is a BST: validate, insert, kth smallest, LCA of BST | `trees/03_bst.py` |
| Many words with shared prefixes, autocomplete, wildcard search, word search II | `trees/04_trie.py` |
| K largest / smallest / most frequent / closest | `heaps/01_top_k.py` |
| Running median, sliding window median, IPO / maximize capital | `heaps/02_two_heaps.py` |
| Merge K sorted lists, kth smallest in sorted matrix, smallest range over K lists | `heaps/03_k_way_merge.py` |

**Sorting, graphs**

| Signal in the problem | File |
|---|---|
| Intervals, meetings, overlaps, rooms needed | `sorting_intervals/01_intervals.py` |
| Count inversions / reverse pairs, implement merge sort | `sorting_intervals/02_merge_sort.py` |
| Kth element in O(n) average, k closest in O(n), sort colors (3-way partition) | `sorting_intervals/03_quickselect.py` |
| Largest number, sort by frequency, relative / custom order | `sorting_intervals/04_custom_sort.py` |
| Unweighted shortest path, "minimum steps", spread from many sources (rotting, nearest 0) | `graphs/01_bfs.py` |
| Islands, region size, flood fill, reachable from border | `graphs/02_dfs.py` |
| Dynamic connectivity, merge groups, redundant edge, provinces, accounts merge | `graphs/03_union_find.py` |
| Prerequisites, dependency order, cycle in a directed graph, alien dictionary | `graphs/04_topological_sort.py` |
| Weighted shortest path, non-negative weights, min effort, max probability | `graphs/05_dijkstra.py` |
| Negative weights, "within K stops", negative cycle detection | `graphs/06_bellman_ford.py` |
| Two groups, two-colouring, dislikes, odd cycle | `graphs/07_bipartite.py` |
| Connect all nodes at minimum total cost | `graphs/08_minimum_spanning_tree.py` |
| All-pairs distances / reachability, small n, evaluate division | `graphs/09_floyd_warshall.py` |
| Critical connections, single point of failure, cut vertex | `graphs/10_bridges_articulation.py` |

**Backtracking, DP, greedy**

| Signal in the problem | File |
|---|---|
| All subsets, combinations, combination sum, phone letters | `backtracking/01_subsets_combinations.py` |
| All permutations (with duplicates), generate parentheses | `backtracking/02_permutations.py` |
| Word search, N-Queens, sudoku: place, recurse, remove on a board | `backtracking/03_grid_and_board.py` |
| Climbing stairs, house robber, decode ways, word break | `dp/01_dp_1d.py` |
| Subset sum, partition, target sum, coin change (min / ways) | `dp/02_knapsack.py` |
| Longest increasing subsequence, nesting envelopes, number of LIS | `dp/03_lis.py` |
| Two strings: LCS, edit distance, distinct subsequences, delete to match | `dp/04_dp_strings.py` |
| Grid paths, min path sum, obstacles, maximal square | `dp/05_grid_dp.py` |
| Stock with cooldown / fee / two transactions, paint house | `dp/06_state_machine_dp.py` |
| Burst balloons, cut stick, palindromic subsequence: answer on [i, j] from splits | `dp/07_interval_dp.py` |
| House robber III, binary tree cameras, distribute coins | `dp/08_tree_dp.py` |
| n <= 16, visit all nodes, TSP, partition into k equal subsets | `dp/09_bitmask_dp.py` |
| Local best choice is provably safe: jumps, gas station, partition labels, task scheduler | `greedy/01_greedy.py` |

**Range queries, strings, math, design**

| Signal in the problem | File |
|---|---|
| Point updates + range sums, count smaller elements after self | `range_queries/01_fenwick_tree.py` |
| Point updates + range min/max, DP needing max over a value range | `range_queries/02_segment_tree.py` |
| Substring search in O(n + m), repeated pattern, shortest palindrome, prefix = suffix | `string_matching/01_kmp.py` |
| Compare many equal-length substrings, repeated DNA, longest duplicate substring | `string_matching/02_rabin_karp.py` |
| Longest / count palindromic substrings, valid palindrome with one deletion | `string_matching/03_palindromes.py` |
| "Appears twice except one", O(1) space on integers, power of two, bitmask subsets | `math_bits/01_bit_manipulation.py` |
| Primes, pow(x, n), gcd, answer mod 1e9+7, nCr | `math_bits/02_number_theory.py` |
| Random node from stream, shuffle, weighted random pick, rand10 from rand7 | `math_bits/03_randomized.py` |
| "Design a class", O(1) get/put, LRU / LFU, getRandom, timestamps | `design/01_design_data_structures.py` |

**Quick tie-breakers:**

- Contiguous + all positive numbers -> sliding window. Contiguous + negatives allowed -> prefix sum + hashmap.
- Shortest path: unweighted -> BFS; non-negative weights -> Dijkstra; at most K edges or negative weights -> Bellman-Ford; all pairs with small n -> Floyd-Warshall.
- Connected regions: either BFS or DFS works; need distances -> BFS.
- "All solutions" -> backtracking. "Count / best solution" -> DP.
- Undirected connectivity as edges arrive -> union-find. Directed order -> topological sort.
- Kth largest: heap is O(n log k) and safe to explain; quickselect is O(n) average, mention as the follow-up.
- Range queries: no updates -> prefix sum; with updates -> Fenwick (sum) or segment tree (min/max).
- Next greater element -> monotonic stack. Max/min of a moving window -> monotonic deque.
- Constraint hints: n <= 20 -> exponential/bitmask OK; n <= 10^4 -> O(n^2) OK; n <= 10^5+ -> O(n log n) or O(n).
