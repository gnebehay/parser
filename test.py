import compute
import parser


def test_computation(inputstring, expected_output):
    ast = parser.parse(inputstring)
    actual_result = compute.compute(ast)
    print(actual_result)
    assert actual_result == expected_output


test_computation('1+1', 2)
test_computation('1-1', 0)
test_computation('1*2', 2)
test_computation('(1+7)*(9+2)', 88)
test_computation('(2+7)/4', 2.25)
test_computation('7/4', 1.75)

try:
    test_computation('1+1)', 1)
    raised = False
except Exception:
    raised = True
assert raised
