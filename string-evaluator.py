'''
NAME: FUNCTIONS FOR STRING CALCULATOR
MIKHAIL BUSHKOV SUMMER 2023
The purpose of this program is to take an expression (in the form of a string), then to output the evaluated result.
'''

# PART 1: INTRO [INPUT STRING --> TOKENIZED LIST]-----


def get_input():  # Basically just the input function.
    input_str = input('Enter an expression: ')
    return input_str


def identify_tokens(input_str):  # Takes a string, converts it into a token format.
    token_list = []
    number, symbol = '', ''  # * These will help keep track of the items going into the list.
    for character in input_str:
        if not character == ' ':  # * Just skips spaces.
            if character in '1234567890.':
                if symbol == '':
                    number += character
            else:
                if not number == '':
                    token_list.append(number)
                    number = ''

                symbol += character
                token_list.append(symbol)
                symbol = ''
    if not number == '':
        token_list.append(number)
    if not symbol == '':
        token_list.append(symbol)

    return token_list


def process_tokens(token_list):  # takes [identify_token], then returns the same list but with float types for the numbers.
    processed_token_list = []
    for token in token_list:
        try:
            token = float(token)  # Tries to convert token (ex. '1') into a float; if it is a number, this will be possible.
        except:
            pass  # If not, it will just return the symbol in string form (ex. '+').
        processed_token_list.append(token)
    return processed_token_list


# FUNCTIONALITY [HELP CALCULATION BE SMOOTHER]-----

# General-based


def is_number(entered):  # This function takes a character, and determines whether it is a number or not.
    if type(entered) == float:
        return True
    else:
        return False


def split_expression(symbol, token_list):  # Takes token list, and splits in accordance with given symbol.
    before, inside, after = [], [], []
    symbol_appears = False
    for token in token_list:
        if token == symbol and not symbol_appears:
            symbol_appears = True
        elif not symbol_appears:
            before.append(token)
        elif symbol_appears:
            after.append(token)

    inside.append(before[-1])
    before.pop(-1)

    inside.append(symbol)

    inside.append(after[0])
    after.pop(0)

    return before, inside, after  # '1 + 2 * 3' --> [1 +], [2 * 3], []


# Bracket-based

def brackets_are_valid(token_list):  # This function makes sure that the brackets are legitimately placed.
    token_str = str(token_list)
    overall_count = 0
    is_possible = True
    for character in token_str:
        if character == '(':
            overall_count += 1
        elif character == ')':
            if (overall_count - 1) < 0:
                is_possible = False
                break
            else:
                overall_count -= 1
        else:
            pass

    return is_possible and overall_count == 0


def split_brackets(token_list):  # Same idea as split_expression, but just for brackets.
    if brackets_are_valid(token_list):
        before, inside, after = [], [], []
        bracket = 0
        opened = False
        for token in token_list:
            if bracket > 0:
                if token == ')':
                    bracket -= 1
                    if bracket > 0:
                        inside.append(token)
                else:
                    if token == '(':
                        bracket += 1
                    inside.append(token)
            else:
                if token == '(' and not opened:
                    bracket += 1
                    opened = True
                else:
                    if len(inside) > 0:
                        after.append(token)
                    else:
                        before.append(token)
        return before, inside, after
    else:
        return [], [], []


# PART 2: CALCULATION [TOKENIZED EXPRESSION --> RESULT]-----


def calculate(token_list):  # Calculates the value of a string given its "token list" form [DOES NOT FOLLOW BEDMAS].
    result = 0
    last_operation = '+'  # Work-around solution: '2 * 3' = '(0 + 2) * 3' <-- addition is first.

    for token in token_list:
        # Checks if the item is a symbol.
        if token == '+':
            last_operation = '+'

        elif token == '-':
            last_operation = '-'

        elif token == '*':
            last_operation = '*'

        elif token == '/':
            last_operation = '/'

        elif token == '^':
            last_operation = '^'

        elif is_number(token):  # Now checks if it is a number, then applies the operation.
            if last_operation == '+':
                result += token
            elif last_operation == '-':
                result -= token
            elif last_operation == '*':
                result *= token
            elif last_operation == '^':
                result **= token
            elif last_operation == '/':
                result /= token

    return result


# BEDMAS OPERATIONS.


def b_calculation(token_list):  # BEDMAS: This function will help prioritize BRACKETS in the calculation process.
    is_valid = brackets_are_valid(token_list)
    if not is_valid:
        return (0 / 0)

    before, inside, after = split_brackets(token_list)

    if '(' not in token_list:
        return token_list
    else:
        result = bedmas_calculation(inside)
        new_expression = before + [result] + after
        return b_calculation(new_expression)  # This is a recursive function, meaning it will call on itself until no more brackets are found.


def e_calculation(token_list):  # BEDMAS: This function will help prioritize EXPONENTS in the calculation process.
    if '^' not in token_list:
        return token_list  # Would just skip this function if no exponents.
    else:
        for symbol in token_list:
            if symbol == '^':
                before, inside, after = split_expression('^', token_list)
                result = calculate(inside)
                token_list = before + [result] + after
            else:
                pass

    return token_list


def dm_calculation(token_list):  # BEDMAS: This function will help prioritize DIVISION & MULTIPLICATION (in sequence) in the calculation process.
    if '*' not in token_list and '/' not in token_list:
        return token_list
    else:
        for symbol in token_list:
            if symbol == '/':
                before, inside, after = split_expression('/', token_list)
                result = calculate(inside)
                token_list = before + [result] + after
            elif symbol == '*':  # elif allows for sequency in multiplication and division.
                before, inside, after = split_expression('*', token_list)

                result = calculate(inside)
                token_list = before + [result] + after
            else:
                pass

        return token_list


def as_calculation(token_list):  # Labelled this as a function in the name of code organization.
    return calculate(token_list)  # Should work since it goes in order anyway.


def bedmas_calculation(token_list):  # This is just the entire calculation section summed up into one function.
    if '(' in token_list:
        token_list = b_calculation(token_list)

    token_list = e_calculation(token_list)
    token_list = dm_calculation(token_list)
    result_number = as_calculation(token_list)

    return result_number


# CONCLUSION-----

def complete_program(input_str):  # The whole program in one function.
    try:
        token_list = process_tokens(identify_tokens(input_str))  # PART 1.
        result = bedmas_calculation(token_list)  # PART 2.

        # A small fix for float outputs (1.0 would become 1).
        if int(result) == result:
            result = int(result)
        else:
             pass

        print('The evaluated result is:', result)
    except:
        print('There has been an error.')      


# MAIN SEQUENCE-----
while (True):
    complete_program(get_input())
    print()
