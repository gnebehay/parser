import sys
import operator
import parser


operations = {
    parser.TokenType.T_PLUS: operator.add,
    parser.TokenType.T_MINUS: operator.sub,
    parser.TokenType.T_MULT: operator.mul,
    parser.TokenType.T_DIV: operator.truediv
}


def compute(node):
    if node.token_type == parser.TokenType.T_NUM:
        return node.value
    left_result = compute(node.children[0])
    right_result = compute(node.children[1])
    operation = operations[node.token_type]
    return operation(left_result, right_result)


if __name__ == '__main__':
    ast = parser.parse(sys.argv[1])
    result = compute(ast)
    print(result)
