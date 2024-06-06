from sympy.parsing.sympy_parser import parse_expr
from sympy import simplify, latex, Matrix, Symbol, Integer, Add, pi, posify, prod
import sys, re

try:
    from .static_unit_conversion_arrays import convert_short_forms, convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_units_and_dimensions, convert_alternative_names_to_standard
    from .expression_utilities import preprocess_expression, parse_expression, create_sympy_parsing_params, substitute
    from .preview import preview_function
except ImportError:
    from static_unit_conversion_arrays import convert_short_forms, convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_units_and_dimensions, convert_alternative_names_to_standard
    from expression_utilities import preprocess_expression, parse_expression, create_sympy_parsing_params, substitute
    from preview import preview_function

parsing_feedback_responses = {
    "PARSE_ERROR_WARNING": lambda x: f"`{x}` could not be parsed as a valid mathematical expression. Ensure that correct notation is used, that the expression is unambiguous and that all parentheses are closed.",
    "PER_FOR_DIVISION": "Note that 'per' was interpreted as '/'. This can cause ambiguities. It is recommended to use parentheses to make your entry unambiguous.",
    "STRICT_SYNTAX_EXPONENTIATION": "Note that `^` cannot be used to denote exponentiation, use `**` instead.",
    "QUANTITIES_NOT_WRITTEN_CORRECTLY": "List of quantities not written correctly.",
    "SUBSTITUTIONS_NOT_WRITTEN_CORRECTLY": "List of substitutions not written correctly.",
}

def feedback_not_dimensionless(groups):
    groups = list(groups)
    if len(groups) == 1:
        return f"The group {convert_to_latex(groups[0])} is not dimensionless."
    else:
        return "The groups "+", ".join([convert_to_latex(g) for g in groups[0:-1]])+" and "+convert_to_latex(groups[-1])+" are not dimensionless."

def convert_to_latex(expr):
    if isinstance(expr, str):
        return expr
    else:
        return "$"+latex(expr)+"$"

buckingham_pi_feedback_responses = {
    "VALID_CANDIDATE_SET": "",
    "NOT_DIMENSIONLESS": feedback_not_dimensionless,
    "MORE_GROUPS_THAN_REFERENCE_SET": "Response has more groups than necessary.",
    "CANDIDATE_GROUPS_NOT_INDEPENDENT": lambda r, n: f"Groups in response are not independent. It has {r} independent group(s) and contains {n} groups.",
    "TOO_FEW_INDEPENDENT_GROUPS": lambda name, r, n: f"{name} contains too few independent groups. It has {r} independent group(s) and needs at least {n} independent groups.",
    "UNKNOWN_SYMBOL": lambda symbols: "Unknown symbol(s): "+", ".join([convert_to_latex(s) for s in symbols])+".",
    "SUM_WITH_INDEPENDENT_TERMS": lambda s: f"Sum in {convert_to_latex(s)} contains more independent terms that there are groups in total. Group expressions should ideally be written as a comma-separated list where each item is an entry of the form `q_1**c_1*q_2**c_2*...*q_n**c_n`."
}

feedback_responses_list = [parsing_feedback_responses, buckingham_pi_feedback_responses]


def get_exponent_matrix(expressions, symbols):
    exponents_list = []
    for expression in expressions:
        exponents = []
        for symbol in symbols:
            exponent = expression.as_coeff_exponent(symbol)[1]
            if exponent == 0:
                exponent = -expression.subs(symbol, 1/symbol).as_coeff_exponent(symbol)[1]
            exponents.append(exponent)
        exponents_list.append(exponents)
    return Matrix(exponents_list)


def string_to_expressions(string):
    beta = Symbol("beta")
    gamma = Symbol("gamma")
    zeta = Symbol("zeta")
    # e = E
    E = Symbol("E")
    I = Symbol("I")
    O = Symbol("O")
    N = Symbol("N")
    Q = Symbol("Q")
    S = Symbol("S")
    symbol_dict = {
        "beta": beta,
        "gamma": gamma,
        "zeta": zeta,
        "I": I,
        "N": N,
        "O": O,
        "Q": Q,
        "S": S,
        "E": E
    }
    expressions = [parse_expr(expr, local_dict=symbol_dict).expand(power_base=True, force=True) for expr in string.split(',')]
    symbols = set()
    for expression in expressions:
        expr = expression.simplify()
        expr = expr.expand(power_base=True, force=True)
        symbols = symbols.union(expression.free_symbols)
    return expressions, symbols


def create_power_product(exponents, symbols):
    return prod([s**i for (s, i) in zip(symbols, exponents)])


def determine_validity(reference_set, reference_symbols, reference_original_number_of_groups, candidate_set, candidate_symbols, candidate_original_number_of_groups):
    '''
    Analyses if the given candidate set satisfies the Buckingham Pi theorem assuming that the given reference set does.
    '''
    symbols = set(reference_symbols).union(set(candidate_symbols))
    R = get_exponent_matrix(reference_set, symbols)
    C = get_exponent_matrix(candidate_set, symbols)
    D = R.col_join(C)
    feedback = []
    more_groups_than_reference_set = reference_original_number_of_groups < candidate_original_number_of_groups
    candidate_groups_independent = C.rank() == candidate_original_number_of_groups
    rank_R_equal_to_rank_D = R.rank() == D.rank()
    rank_C_equal_to_rank_D = C.rank() == D.rank()
    if candidate_symbols.issubset(reference_symbols):
        valid = not more_groups_than_reference_set
        if more_groups_than_reference_set:
            feedback.append(buckingham_pi_feedback_responses["MORE_GROUPS_THAN_REFERENCE_SET"])
        valid = valid and candidate_groups_independent
        if not candidate_groups_independent:
            feedback.append(buckingham_pi_feedback_responses["CANDIDATE_GROUPS_NOT_INDEPENDENT"](C.rank(), len(candidate_set)))
        if rank_R_equal_to_rank_D:
            if rank_C_equal_to_rank_D:
                feedback.append(buckingham_pi_feedback_responses["VALID_CANDIDATE_SET"])
            else:
                valid = False
                feedback.append(buckingham_pi_feedback_responses["TOO_FEW_INDEPENDENT_GROUPS"]("Response", C.rank(), D.rank()))
        else:
            valid = False
            if len(candidate_set) == 1:
                dimensionless_groups = candidate_set
            else:
                dimensionless_groups = set()
                for i in range(len(candidate_set)):
                    exponents = C.row(i)
                    Di = R.col_join(exponents)
                    if R.rank() != Di.rank():
                        dimensionless_groups.add(create_power_product(exponents, symbols))
            feedback.append(buckingham_pi_feedback_responses["NOT_DIMENSIONLESS"](dimensionless_groups))
    else:
        feedback.append(buckingham_pi_feedback_responses["UNKNOWN_SYMBOL"](candidate_symbols.difference(reference_symbols)))
        valid = False
    feedback = [elem.strip() for elem in feedback if len(elem.strip()) > 0]
    return valid, "<br>".join(feedback)


def evaluation_function(response, answer, params) -> dict:
    """
    Function that provides some basic dimensional analysis functionality.
    """

    # Utility function that wraps a string in a function that takes an
    # arbitrary number of arguments
    def wrap_feedback_function(output):
        def wrapped_function(*args):
            return output
        return wrapped_function

    # Take custom feedback string given by task author and
    # replace the corresponding entries in the feedback response
    # dictionaries, wrapping pure stings in a function that takes
    # an arbitrary number of arguments when necessary
    custom_feedback = params.get("custom_feedback", None)
    if custom_feedback is not None:
        for feedback_responses in feedback_responses_list:
            for key in custom_feedback.keys():
                if key in feedback_responses.keys():
                    if isinstance(feedback_responses[key], str):
                        feedback_responses[key] = custom_feedback[key]
                    elif callable(feedback_responses[key]):
                        feedback_responses[key] = wrap_feedback_function(custom_feedback[key])
                    else:
                        raise Exception("Cannot handle given costum feedback for "+key)

    # Uses the preview function to translate latex input to  a
    # sympy compatible representation
    if params.get("is_latex", False):
        response = preview_function(response, params)["preview"]["sympy"]

    feedback = {}
    default_rtol = 1e-12

    # If substitutions are set, default unit and dimension names are
    # deactivated
    if "substitutions" in params.keys():
        unsplittable_symbols = tuple()
    else:
        unsplittable_symbols = names_of_prefixes_units_and_dimensions

    # Set default parameters if not already set
    parameters = {"comparison": "expression", "strict_syntax": True}
    parameters.update(params)

    # Check if `per` is ised for division and add relevant remark to
    # feedback if so
    remark = ""
    if "per" not in sum([[x[0]]+x[1] for x in parameters.get("input_symbols", [])], []):
        if (" per " in response):
            remark += parsing_feedback_responses["PER_FOR_DIVISION"]
        if (" per " in answer):
            raise Exception(parsing_feedback_responses["PER_FOR_DIVISION"])
        answer = substitute(answer+" ", convert_alternative_names_to_standard+[(" per ", "/")])[0:-1]
        response = substitute(response+" ", convert_alternative_names_to_standard+[(" per ", "/")])[0:-1]

    # Raise exceptions when answer or response is missing from input
    if not isinstance(answer, str):
        raise Exception("No answer was given.")
    if not isinstance(response, str):
        return {"is_correct": False, "feedback": "No response submitted."}

    answer = answer.strip()
    response = response.strip()
    if len(answer) == 0:
        raise Exception("No answer was given.")
    if len(response) == 0:
        return {"is_correct": False, "feedback": "No response submitted."}

    # Preprocess answer and response to prepare for parsing by sympy
    answer, response = preprocess_expression([answer, response], parameters)
    parsing_params = create_sympy_parsing_params(parameters, unsplittable_symbols=unsplittable_symbols)

    # Remark on syntax if necessary
    if parameters["strict_syntax"]:
        if "^" in response:
            separator = "" if len(remark) == 0 else "\n"
            remark += separator+parsing_feedback_responses["STRICT_SYNTAX_EXPONENTIATION"]
        if "^" in answer:
            raise Exception(parsing_feedback_responses["STRICT_SYNTAX_EXPONENTIATION"])

    # Perform buckinghamPi comparison
    if parameters["comparison"] == "buckinghamPi":
        # Parse expressions for groups in response and answer
        response_strings = response.split(',')
        response_number_of_groups = len(response_strings)
        response_original_number_of_groups = len(response_strings)
        response_groups = []
        separator = "" if len(remark) == 0 else "\n"
        for res in response_strings:
            try:
                expr = parse_expression(res, parsing_params).simplify()
                expr = expr.expand(power_base=True, force=True)
            except Exception:
                separator = "" if len(remark) == 0 else "\n"
                return {"is_correct": False, "feedback": parsing_feedback_responses["PARSE_ERROR_WARNING"](response)+separator+remark}
            if isinstance(expr, Add):
                response_groups += list(expr.args)
                response_number_of_groups += len(list(expr.args))
            else:
                response_groups.append(expr)
                response_number_of_groups += 1
        response_latex = [latex(expr) for expr in response_groups]

        interp = {"response_latex": ", ".join(response_latex)}

        if answer == "-":
            answer_strings = []
        else:
            answer_strings = answer.split(',')
        answer_groups = []
        answer_number_of_groups = 0
        answer_original_number_of_groups = 0
        for ans in answer_strings:
            try:
                expr = parse_expression(ans, parsing_params).simplify()
                expr = expr.expand(power_base=True, force=True)
            except Exception as e:
                raise Exception(parsing_feedback_responses["PARSE_ERROR_WARNING"]("The answer")) from e
            if isinstance(expr, Add):
                answer_groups += list(expr.args)
                answer_number_of_groups += len(list(expr.args))
            else:
                answer_groups.append(expr)
                answer_number_of_groups += 1
            answer_original_number_of_groups += 1

        remark = ""

        # Find what different symbols for quantities there are
        if "quantities" in parameters.keys():
            quantities_strings = parameters["quantities"]
            quantities = []
            index = quantities_strings.find("(")
            while index > -1:
                index_match = find_matching_parenthesis(quantities_strings, index)
                try:
                    quantity_strings = eval(quantities_strings[index+1:index_match])
                    quantity = tuple(map(lambda x: parse_expression(x, parsing_params), quantity_strings))
                    quantities.append(quantity)
                except Exception:
                    raise Exception(parsing_feedback_responses["QUANTITIES_NOT_WRITTEN_CORRECTLY"])
                index = quantities_strings.find('(', index_match+1)
            response_symbols = list(map(lambda x: x[0], quantities))
            answer_symbols = response_symbols

            # Check how many dimensionless groups are needed
            dimension_symbols = set()
            for quantity in quantities:
                dimension_symbols = dimension_symbols.union(quantity[1].free_symbols)
            quantity_matrix = get_exponent_matrix([q[1] for q in quantities], dimension_symbols)
            number_of_groups = len(quantities)-quantity_matrix.rank()

            # If answer groups are not given, generate a valid set of groups to use as answer
            if answer_groups == []:
                # Compute answer groups from defined quantities
                nullspace_basis = quantity_matrix.T.nullspace()
                for basis_vector in nullspace_basis:
                    multiplier = 1
                    for i in range(0, basis_vector.rows):
                        if not isinstance(basis_vector[i, 0], Integer):
                            multiplier *= 1/basis_vector[i, 0]
                    if multiplier != 1:
                        for i in range(0, basis_vector.rows):
                            basis_vector[i, 0] = round(basis_vector[i, 0]*multiplier)
                answer_groups = [1]*number_of_groups
                for i in range(0, len(answer_groups)):
                    for j in range(0, len(quantities)):
                        answer_groups[i] *= quantities[j][0]**nullspace_basis[i][j]

            if answer == "-":
                answer_number_of_groups = number_of_groups
                answer_original_number_of_groups = number_of_groups

            # Analyse dimensions of answers and responses
            answer_dimensions = []
            for group in answer_groups:
                dimension = group
                for quantity in quantities:
                    dimension = dimension.subs(quantity[0], quantity[1])
                answer_dimensions.append(posify(dimension)[0].simplify())

            # Check that answers are dimensionless
            for k, dimension in enumerate(answer_dimensions):
                if not dimension.is_constant():
                    raise Exception(buckingham_pi_feedback_responses["NOT_DIMENSIONLESS"](answer_groups[k]))

            # Check that there is a sufficient number of independent groups in the answer
            answer_matrix = get_exponent_matrix(answer_groups, answer_symbols)
            if answer_matrix.rank() < number_of_groups:
                raise Exception(buckingham_pi_feedback_responses["TOO_FEW_INDEPENDENT_GROUPS"]("Answer", answer_matrix.rank(), number_of_groups))

        # Compare symbols used in answer and response
        response_symbols = set()
        for res in response_groups:
            response_symbols = response_symbols.union(res.free_symbols)
        answer_symbols = set()
        for ans in answer_groups:
            answer_symbols = answer_symbols.union(ans.free_symbols)
        if not response_symbols.issubset(answer_symbols):
            feedback.update({"feedback": buckingham_pi_feedback_responses["UNKNOWN_SYMBOL"](response_symbols.difference(answer_symbols))})
            return {"is_correct": False, **feedback, **interp}
        answer_symbols = list(answer_symbols)

        # Check ing the given response is a valid set of groups
        reference_set = set(answer_groups)
        reference_symbols = set(answer_symbols)
        candidate_set = set(response_groups)
        candidate_symbols = set(response_symbols)
        valid, feedback_string = determine_validity(reference_set, reference_symbols, answer_original_number_of_groups, candidate_set, candidate_symbols, response_original_number_of_groups)
        feedback.update({"feedback": feedback_string})

        # Check the special case where one groups expression contains several power products
        separator = "" if len(remark) == 0 else "\n"
        answer_matrix = get_exponent_matrix(answer_groups, answer_symbols)
        if answer_matrix.rank() > answer_number_of_groups:
            raise Exception(buckingham_pi_feedback_responses["SUM_WITH_INDEPENDENT_TERMS"]("answer"))
        response_matrix = get_exponent_matrix(response_groups, answer_symbols)
        if response_matrix.rank() > response_original_number_of_groups:
            return {"is_correct": False, "feedback": buckingham_pi_feedback_responses["SUM_WITH_INDEPENDENT_TERMS"]("response")+separator+remark, **interp}

        return {"is_correct": valid, "feedback": feedback.get("feedback", "")+separator+remark, **interp}

    list_of_substitutions_strings = parameters.get("substitutions", [])
    if isinstance(list_of_substitutions_strings, str):
        list_of_substitutions_strings = [list_of_substitutions_strings]

    if "quantities" in parameters.keys():
        list_of_substitutions_strings = [parameters["quantities"]]+list_of_substitutions_strings

    if not (isinstance(list_of_substitutions_strings, list) and all(isinstance(element, str) for element in list_of_substitutions_strings)):
        raise Exception(parsing_feedback_responses["SUBSTITUTIONS_NOT_WRITTEN_CORRECTLY"])

    try:
        interp = {"response_latex": expression_to_latex(response, parameters, parsing_params, remark)}
    except Exception:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parsing_feedback_responses["PARSE_ERROR_WARNING"](response)+separator+remark}

    # Perform substitutions
    substitutions = []
    for subs_strings in list_of_substitutions_strings:
        # Parsing list of substitutions
        sub_substitutions = []
        index = subs_strings.find('(')
        while index > -1:
            index_match = find_matching_parenthesis(subs_strings, index)
            try:
                sub_substitutions.append(eval(subs_strings[index:index_match+1]))
            except Exception:
                raise Exception(parsing_feedback_responses["SUBSTITUTIONS_NOT_WRITTEN_CORRECTLY"])
            index = subs_strings.find('(', index_match+1)
            if index > -1 and subs_strings.find('|', index_match, index) > -1:
                # Substitutions are sorted so that the longest possible part of the original string will be substituted in each step
                sub_substitutions.sort(key=lambda x: -len(x[0]))
                substitutions.append(sub_substitutions)
                sub_substitutions = []
        sub_substitutions.sort(key=lambda x: -len(x[0]))
        substitutions.append(sub_substitutions)

    if "substitutions" not in parameters.keys():
        if len(parameters.get("quantities", [])) > 0 or parameters.get("elementary_functions", False) is True:
            substitutions += convert_to_SI_base_units
        else:
            substitutions += convert_to_SI_base_units_short_form
        if parameters["comparison"] == "dimensions":
            if "quantities" in parameters.keys():
                substitutions += convert_SI_base_units_to_dimensions
            else:
                substitutions += convert_SI_base_units_to_dimensions_short_form

    for sub in substitutions:
        answer = substitute(answer, sub)
        response = substitute(response, sub)

    # Safely try to parse answer and response into symbolic expressions
    try:
        match_group = re.match("0+(.0+)?\s", response)
        if match_group is not None:
            response = response[match_group.span()[1]:]
        res = parse_expression(response, parsing_params)
    except Exception:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parsing_feedback_responses["PARSE_ERROR_WARNING"](response)+separator+remark}

    try:
        match_group = re.match("0+(.0+)?\s", answer)
        if match_group is not None:
            answer = answer[match_group.span()[1]:]
        ans = parse_expression(answer, parsing_params)
    except Exception as e:
        raise Exception(f"SymPy was unable to parse the answer {answer}") from e

    # Add remarks found to feedback
    if "feedback" in feedback.keys():
        feedback.update({"feedback": feedback["feedback"]+remark})
    elif len(remark) > 0:
        feedback.update({"feedback": remark})

    if parameters["comparison"] == "dimensions":
        is_correct = bool(simplify(res/ans).is_constant() and res != 0)
        if is_correct:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp, **feedback}

    if parameters["comparison"] == "expression":
        # REMARK: 'pi' should be a reserve symbols but is sometimes not treated as one, possibly because of input symbols
        # The two lines below this comments fixes the issue but a more robust solution should be found for cases where there
        # are other reserved symbols.
        if "atol" in parameters.keys() or "rtol" in parameters.keys():
            ans = ans.subs(Symbol('pi'), float(pi))
            res = res.subs(Symbol('pi'), float(pi))
        if res != 0:
            equal_up_to_multiplication = bool(simplify(res/ans).is_constant() and res != 0)
        elif ans != 0:
            equal_up_to_multiplication = bool(simplify(res/ans).is_constant() and res != 0)
        else:  # This corresponds to res = ans = 0
            equal_up_to_multiplication = True
        error_below_atol = False
        error_below_rtol = False
        if equal_up_to_multiplication:
            if ans.free_symbols == res.free_symbols:
                for symbol in ans.free_symbols:
                    ans = ans.subs(symbol, 1)
                    res = res.subs(symbol, 1)
            if "atol" in parameters.keys():
                error_below_atol = bool(abs(float(ans-res)) < float(parameters["atol"]))
            else:
                error_below_atol = True
            if "rtol" in parameters.keys():
                rtol = float(parameters["rtol"])
                error_below_rtol = bool(float(abs(((ans-res)/ans).simplify())) < rtol)
            else:
                if "atol" in parameters.keys():
                    error_below_rtol = True
                elif ans == 0:
                    error_below_rtol = bool(float(abs(res)) <= sys.float_info.epsilon)
                else:
                    error_below_rtol = bool(float(abs(((ans-res)/ans).simplify())) < default_rtol)
        if error_below_atol and error_below_rtol:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp, **feedback}

    if parameters["comparison"] == "expressionExact":
        # Here nsimplify is used to transform float to rationals since some unit conversions are not exact and answers and responses might contain decimal values
        is_correct = (res.nsimplify()-ans.nsimplify()).simplify() == 0
        if is_correct:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp, **feedback}

    return {"is_correct": False, **interp, **feedback}


def find_matching_parenthesis(string, index):
    depth = 0
    for k in range(index, len(string)):
        if string[k] == '(':
            depth += 1
            continue
        if string[k] == ')':
            depth += -1
            if depth == 0:
                return k
    return -1


def expression_to_latex(expression, parameters, parsing_params, remark):
    unsplittable_symbols = parsing_params.get("unsplittable_symbols", ())
    symbol_dict = parsing_params.get("symbol_dict", {})
    if not (len(parameters.get("quantities", [])) > 0 or parsing_params.get("elementary_functions", False) is True):
        subs = convert_short_forms
        expression = substitute(expression, subs)
    try:
        expression_preview = parse_expression(expression, parsing_params)
    except Exception:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parsing_feedback_responses["PARSE_ERROR_WARNING"](expression)+separator+remark}

    symbs_dic = {}
    symbol_names = {}
    if not len(parameters.get("quantities", [])) > 0:
        symbs = expression_preview.atoms(Symbol)
        symbs_dic = {str(x): Symbol(str(x), commutative=False) for x in symbs}
        parsing_params_latex = parsing_params.copy()
        parsing_params_latex["symbol_dict"] = symbs_dic
        expression_preview = parse_expression(expression, parsing_params_latex)
        symbol_names = {}
        for x in symbs_dic.values():
            symbol_names.update({x: "~\\mathrm{"+str(x)+"}"})
    latex_str = latex(expression_preview, symbol_names=symbol_names)
    for symbol in symbs_dic.keys():
        if symbol not in symbol_dict.keys() and symbol not in unsplittable_symbols:
            if symbol in globals():
                del globals()[symbol]
    return latex_str
