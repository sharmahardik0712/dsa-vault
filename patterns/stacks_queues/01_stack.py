"""
PATTERN: Stack (matching, nesting, evaluation)
USE WHEN: The most recent unfinished thing must be handled first: matching brackets, nested
          structures, undo, expression evaluation, or tracking a running state per level.
SIGNALS: "valid parentheses", "balanced", "nested", "decode string", "evaluate expression",
         "reverse polish notation", "simplify path", "min stack", "backspace"
TIME: O(n)   SPACE: O(n)
PITFALLS: - Popping from an empty stack: always check `stack` before `stack.pop()` / `stack[-1]`.
          - Return `not stack` at the end: leftovers mean unmatched openers.
          - Integer division in RPN truncates toward zero: use int(a / b), not a // b.
          - Nested decode: push (string_so_far, repeat_count) on '[' and restore on ']'.
PROBLEMS: 20 Valid Parentheses, 155 Min Stack, 150 Evaluate Reverse Polish Notation,
          394 Decode String, 71 Simplify Path
"""


# ---------- Core template: push openers, match on closers ----------
def is_valid_parentheses(s: str) -> bool:
    # LC 20.
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack


# ---------- Worked problems ----------
class MinStack:
    # LC 155. Store (value, min_so_far) so min is O(1) after pops.
    def __init__(self) -> None:
        self.items: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = min(val, self.items[-1][1]) if self.items else val
        self.items.append((val, current_min))

    def pop(self) -> None:
        self.items.pop()

    def top(self) -> int:
        return self.items[-1][0]

    def get_min(self) -> int:
        return self.items[-1][1]


def eval_rpn(tokens: list[str]) -> int:
    # LC 150. Operands pushed; an operator pops two (order matters for - and /).
    stack: list[int] = []
    for tok in tokens:
        if tok in "+-*/" and len(tok) == 1:
            b, a = stack.pop(), stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(tok))
    return stack[-1]


def decode_string(s: str) -> str:
    # LC 394. On '[' save context; on ']' current = saved + current * k.
    stack: list[tuple[str, int]] = []
    current = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((current, num))
            current, num = "", 0
        elif ch == "]":
            prev, k = stack.pop()
            current = prev + current * k
        else:
            current += ch
    return current


if __name__ == "__main__":
    assert is_valid_parentheses("()[]{}")
    assert not is_valid_parentheses("(]")
    assert not is_valid_parentheses("([)]")
    assert is_valid_parentheses("")
    assert not is_valid_parentheses("(") and not is_valid_parentheses(")")

    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0 and ms.get_min() == -2

    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert eval_rpn(["-7", "2", "/"]) == -3                 # truncates toward zero
    assert eval_rpn(["5"]) == 5

    assert decode_string("3[a]2[bc]") == "aaabcbc"
    assert decode_string("3[a2[c]]") == "accaccacc"
    assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decode_string("10[a]") == "a" * 10
    assert decode_string("") == ""
    print("ok")
