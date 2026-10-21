from stack import Stack


_MATCH = {')': '(', ']': '[', '}': '{'}
_OPEN = set(_MATCH.values())
_CLOSE = set(_MATCH.keys())


def validate_expression(expression: str) -> bool:
    bracket_stack = Stack(label="ExprChecker")

    for i, ch in enumerate(expression):
        if ch in _OPEN:
            bracket_stack.push(ch)

        elif ch in _CLOSE:
            if bracket_stack.is_empty():
                print(f"    [!] Unmatched closing '{ch}' at position {i}")
                return False
            top = bracket_stack.pop()
            if top != _MATCH[ch]:
                print(f"    [!] Mismatch: opened with '{top}' but closed by '{ch}' at pos {i}")
                return False

    if not bracket_stack.is_empty():
        print(f"    [!] {bracket_stack.get_size()} unclosed bracket(s) remaining")
        return False

    return True


def run_expression_demo() -> None:
    test_cases = [
        ("(TeacherA AND (RoomB OR RoomC))", True),
        ("(TeacherA AND (RoomB OR RoomC)", False),
        ("TeacherA AND RoomB)", False),
        ("{[TeacherB] AND (SlotMon OR SlotTue)}", True),
        ("{[TeacherB] AND (SlotMon OR SlotTue})", False),
        ("((CourseCS101 AND NOT Holiday))", True),
        ("", True),
    ]

    print("\n  Stack-Based Constraint Expression Validator")
    print("  " + "-" * 55)
    print(f"  {'Expression':<45} {'Result'}")
    print("  " + "-" * 55)

    for expr, expected in test_cases:
        result = validate_expression(expr)
        status = "[VALID]" if result else "[INVALID]"
        correct = "OK" if result == expected else "UNEXPECTED"
        display = expr if expr else "(empty string)"
        print(f"  {display:<45} {status}  {correct}")

    print("  " + "-" * 55)
