"""
PATTERN: Trie (Prefix Tree)
USE WHEN: Many strings share prefixes and you need fast prefix lookup, autocomplete, or to search
          a grid/stream for many words at once.
SIGNALS: "prefix", "starts with", "autocomplete", "dictionary of words", "word search II",
         "replace words", "longest common prefix", "wildcard '.' search"
TIME: O(L) per insert/search (L = word length)   SPACE: O(total characters)
PITFALLS: - Forgetting the end-of-word flag: "app" is a prefix of "apple" but not a word unless marked.
          - search() vs starts_with() differ only in checking that flag.
          - Word Search II: prune found words (set word = None) to avoid duplicates and speed up.
          - Dict children are simpler than [None]*26 arrays in Python; use them.
PROBLEMS: 208 Implement Trie, 211 Design Add and Search Words, 212 Word Search II,
          648 Replace Words, 14 Longest Common Prefix
"""


# ---------- Core template ----------
class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.word: str | None = None          # full word stored at its end node


class Trie:
    # LC 208.
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.word = word

    def _walk(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.word is not None

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None


# ---------- Worked problems ----------
def wildcard_search(root: TrieNode, word: str) -> bool:
    # LC 211. On '.', branch into every child (DFS).
    def dfs(node: TrieNode, i: int) -> bool:
        if i == len(word):
            return node.word is not None
        ch = word[i]
        if ch == ".":
            return any(dfs(child, i + 1) for child in node.children.values())
        return ch in node.children and dfs(node.children[ch], i + 1)

    return dfs(root, 0)


def replace_words(roots: list[str], sentence: str) -> str:
    # LC 648. Walk each word through the trie; stop at the first complete root.
    trie = Trie()
    for r in roots:
        trie.insert(r)
    out = []
    for word in sentence.split():
        node = trie.root
        replacement = word
        for ch in word:
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.word is not None:
                replacement = node.word
                break
        out.append(replacement)
    return " ".join(out)


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    # LC 212. DFS the board while walking the trie: prunes all words at once.
    trie = Trie()
    for w in words:
        trie.insert(w)
    rows, cols = len(board), len(board[0]) if board else 0
    found: list[str] = []

    def dfs(r: int, c: int, node: TrieNode) -> None:
        ch = board[r][c]
        if ch not in node.children:
            return
        nxt = node.children[ch]
        if nxt.word is not None:
            found.append(nxt.word)
            nxt.word = None                   # report once
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                dfs(nr, nc, nxt)
        board[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root)
    return found


if __name__ == "__main__":
    t = Trie()
    t.insert("apple")
    assert t.search("apple")
    assert not t.search("app")
    assert t.starts_with("app")
    t.insert("app")
    assert t.search("app")
    assert not t.starts_with("b")
    assert t.starts_with("")                  # empty prefix matches everything
    assert not t.search("")

    w = Trie()
    for word in ["bad", "dad", "mad"]:
        w.insert(word)
    assert not wildcard_search(w.root, "pad")
    assert wildcard_search(w.root, ".ad")
    assert wildcard_search(w.root, "b..")
    assert not wildcard_search(w.root, "b...")

    assert replace_words(["cat", "bat", "rat"], "the cattle was rattled by the battery") == \
        "the cat was rat by the bat"
    assert replace_words(["a", "aa"], "aaa bbb") == "a bbb"
    assert replace_words([], "hello") == "hello"

    board = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
    assert sorted(find_words(board, ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
    assert find_words([["a"]], ["a", "a"]) == ["a"]
    assert find_words([], ["a"]) == []
    print("ok")
