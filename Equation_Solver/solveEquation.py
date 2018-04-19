from Node import Node
import itertools

OPS = set(['+', '-', '*', '/', '^', 'log', '(', ')', '='])

LEFTREMOVALTRANSFORMS = {'+': ['y + x = z', 'x = z - y'], '-': ['y - x = z', 'x = y - z'],
                         '/': ['y / x = z', 'x = y / z'], '*': ['y * x = z', 'x = z / y'],
                         '^': ['y ^ x = z', 'x = y log z']}

RIGHTREMOVALTRANSFORMS = {'+': ['x + y = z', 'x = z - y'], '-': ['x - y = z', 'x = z + y'],
                         '*': ['x * y = z', 'x = z / y'], '/': ['x / y = z', 'x = z * y'],
                         '^': ['x ^ y = z', 'x = z ^ ( $1 / y )']}

DATABASE = ['force = mass * acceleration', '@KE = $0.5 * mass * @velocity ^ $2', '@time = infinity * space', '@velocity = acceleration * @time', '@work = force * @time']


#to simplify
#if child of operator A is opposite operator, and one child has same value as other child of A, cancel
PRIORITY = {'=':0, '+':1, '-':1, '*':2, '/':2, '^':3, 'log':4}

#next step =

#returns an array with different trees representing the output in terms of the inputs, using database of equations
def physics_solve(inputs, output, knowns:dict, visited: set):



    #each option represents one equation in database that contains the output
    options = []
    for i in DATABASE:
        eq = i.split(' ')
        #if equation contains the current var we are looking for, and will not result in a loop
        if(eq.__contains__(output) and not intersects(eq, visited)):
            needed_vars = []
            for token in eq:
                if isVariable(token) and not (token in inputs or token in output):
                    needed_vars.append(token)

            option = (eq, needed_vars)
            options.append(option)

    options.sort(key = lambda x: len(x[1]))
    visited.add(output)



    #keys are the index of the equation in the options list
    #values are each a list
    #consisting of tuples of a variable needed to solve the equation and its corresponding trees
    solutions = dict()
    for idx, option in enumerate(options):
        solution = []
        needed_vars = option[1]
        for var in needed_vars:
            if var not in knowns:
                knowns[var] = physics_solve(inputs, var, knowns, visited)
            solution.append((var, knowns[var]))

        if False not in solution:
            solutions[idx] = solution
    visited.remove(output)




    ret = []
    for i, option in enumerate(options):
        eq = option[0]
        tree_eq = infixToTree(eq)
        if i in solutions:
            solution = solutions[i]

            # base case - all variables in eq are either the output or the input
            if len(solution) == 0:
                rearranged_eq = solveFor(tree_eq, output)
                return [removeEqualsFromLeft(rearranged_eq)]
            else:

                solution_trees = [x[1] for x in solution]

                # for a single equation (of a single option), gets all possible combinations,
                # of all possible trees for each needed variable
                all_solutions_for_equation = list(itertools.product(*solution_trees))

                for solution_combo in all_solutions_for_equation:
                    legend = dict()
                    for idx, tree in enumerate(solution_combo):
                        legend[solution[idx][0]] = tree
                    rearranged_eq = solveFor(tree_eq, output)
                    solved_rearranged_equation = substitute(rearranged_eq, legend)

                    ret.append(removeEqualsFromLeft(solved_rearranged_equation))

    return ret

def isVariable(token):
    return token not in OPS and token[0] != '$'

def intersects(x, y):
    for i in x:
        for j in y:
            if i == j:
                return True
    return False

def removeEqualsFromLeft(tree):
    return tree.right

def infix_to_postfix(formula):
    stack = [] # only pop when the coming op has priority
    output = []
    for ch in formula:
        if ch not in OPS:
            output.append(ch)
        elif ch == '(':
            stack.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # pop '('
        else:
            while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output.append(stack.pop())
            stack.append(ch)
    # leftover
    while stack:
        output.append(stack.pop())

    return output
def postfix_to_infix(formula):
    print(formula)
    stack = []
    prev_op = None
    for ch in formula:
        if not ch in OPS:
            stack.append(ch)
        else:
            b = stack.pop()
            a = stack.pop()
            if prev_op and len(a) > 1 and PRIORITY[ch] > PRIORITY[prev_op]:
                # if previous operator has lower priority
                # add '()' to the previous a
                expr = '('+a+')' + ch + b
            else:
                expr = a + ch + b
            stack.append(expr)
            prev_op = ch

    return stack[-1]


def infixToTree(formula):
    return postfixToTree(infix_to_postfix(formula))

def postfixToTree(formula):
    stack = []
    for tok in formula:
        if tok not in OPS:
            stack.append(tok)
        else:
            right = stack.pop()
            left = stack.pop()
            if isinstance(right, str):
                right = Node(right)
            if isinstance(left, str):
                left = Node(left)
            stack.append(Node(tok, left, right))
    return stack[-1]

#prints out tree in infix by post-order traversal
def treeToPostfix(tree: Node):
    if tree is None:
        return ''
    ret = ' '
    ret = ret + treeToPostfix(tree.left)
    ret = ret + treeToPostfix(tree.right)
    ret = ret + tree.data
    return ret + ' '

def treeToInfix(tree: Node):

    return postfix_to_infix(treeToPostfix(tree).split())

def substitute(formula, legend):
    if(formula is None):
        return None
    if formula.data[0] == '$':
        ret = formula.nodeCopy()
        return ret
    elif formula.data not in OPS and formula.data in legend:
        return legend[formula.data]
    else:
        left = substitute(formula.left, legend)
        right = substitute(formula.right, legend)
        ret = formula.nodeCopy()
        ret.left = left
        ret.right = right
        return ret

#checks if an expression (formula) matches a pattern
#keeps track of the tree each variable in the pattern is equivalent to
def match(formula, pattern, legend):
    if pattern is None:
        if formula is None:
            return True
        else:
            return False
    else:
        if formula is None:
            return False

    if pattern.data[0] == '$':
        if pattern.data != formula.data:
            return False
    else:
        if pattern.data in OPS:
            if formula.data != pattern.data:
                return False
        else:
            if pattern.data in legend:
                print('Only happens if multiples in pattern')
                return match(formula, legend[pattern.data], legend)
            else:

                legend[pattern.data] = formula.treeCopy()
                return True

    leftMatch = match(formula.left, pattern.left, legend)
    rightMatch = match(formula.right, pattern.right, legend)
    return leftMatch and rightMatch

def transform(formula, patternFrom, patternTo):
    legend = dict()
    if match(formula, patternFrom, legend):
        return substitute(patternTo, legend)
    else:
        return None

def solveFor(formula, v):
    if v in formula.right:
        formula.flip()
    elif v not in formula.left:
        return None
    done = False
    rhs = formula.right
    lhs = formula.left

    while(not done):
        rhs = formula.right
        lhs = formula.left
        if lhs.data in OPS:
            removalTransforms = []
            if v in lhs.right:
                removalTransforms = LEFTREMOVALTRANSFORMS
            elif v in lhs.left:
                removalTransforms = RIGHTREMOVALTRANSFORMS
            removalTransform = removalTransforms[lhs.data]

            patternFrom = infixToTree(removalTransform[0].split(' '))
            patternTo = infixToTree(removalTransform[1].split(' '))
            formula = transform(formula, patternFrom, patternTo)
        else:
            done = True
        #done = lhs.data == v
    return formula

def testInfixPostfix(formula):
    print(infix_to_postfix(formula))
    print(treeToPostfix(postfixToTree(infix_to_postfix(formula))))

infix = 'a + c ^ $5 * d / z = g ^ $3'.split(' ')
postfix = infix_to_postfix(infix)
tree = postfixToTree(postfix)

patterns = 'a b * c /'.split(' ')
patternTree = postfixToTree(patterns)
newPattern = 'b a + c *'.split(' ')
newPatternTree = postfixToTree(newPattern)

legend = dict()


print(treeToInfix(physics_solve(["force", "mass", "@KE"], "@work", knowns=dict(), visited=set())[0]))
