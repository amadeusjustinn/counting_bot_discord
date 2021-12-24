def eval_helper(exp):
    """
    Checks if a mathematical expression can be evaluated by eval().

    Parameters
    ==========
    - exp

        Expression to be verified

    Returns
    =======
    [

        - number: Evaluation result of expression (if valid), 0 otherwise,
        - boolean value: whether the expression can be evaluated by eval()

    ]
    """

    # Return false if there are letters in expression
    if any(char.isalpha() for char in exp):
        return [0, False]

    # Replace exponentiation, multiplication and division signs with Pythonic equivalents
    temp = exp.replace("^", "**").replace("×", "*").replace("÷", "/")

    # Perform the check
    try:
        result = eval(temp)
    except:
        return [0, False]
    return [result, True]


def evaluate(exp, curr_count):
    """
    Safely evaluates the mathematical expression in the message.

    Parameters
    ==========
    - exp

        Expression to be verified

    - curr_count

        The current count

    Returns
    =======
   [

        - number: Evaluation result of expression (if valid), 0 otherwise,
        - boolean value: whether the expression is current_count + 1

    ]
    """

    result = eval_helper(exp)

    # Return False if expression cannot be evaluated
    if not result[1]:
        return [0, False]

    # Check if current expression evaluates to 1 more than curr_count
    return [result[0], result[0] == curr_count + 1]


print(evaluate("2*5-", 9))
