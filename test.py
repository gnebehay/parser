import compute
import parser


def test_computation(inputstring, expected_output):
    ast = parser.parse(inputstring)
    actual_result = compute.compute(ast)
    print('{} should evaluate to {}, actual result is {}'.format(inputstring, expected_output, actual_result))
    assert actual_result == expected_output


test_computation('1+1', 2)
test_computation('1-1', 0)
test_computation('3-2+1', 2)
test_computation('8/4/2', 1)
test_computation('1*2', 2)
test_computation('(1+7)*(9+2)', 88)
test_computation('(2+7)/4', 2.25)
test_computation('7/4', 1.75)
test_computation('2*3+4', 10)
test_computation('2*(3+4)', 14)
test_computation('2+3*4', 14)
test_computation('2+(3*4)', 14)
test_computation('2-(3*4+1)', -11)
test_computation('2*(3*4+1)', 26)
test_computation('8/((1+3)*2)', 1)

try:
    test_computation('1+1)', 1)
    raised = False
except Exception:
    raised = True
assert raised

