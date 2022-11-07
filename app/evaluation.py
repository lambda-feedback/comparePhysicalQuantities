from sympy.parsing.sympy_parser import parse_expr, split_symbols_custom
from sympy.parsing.sympy_parser import T as parser_transformations
from sympy import simplify, latex, Matrix, Symbol, Integer, Add, Subs, pi

try:
    from .static_unit_conversion_arrays import convert_short_forms, convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_units_and_dimensions, convert_alternative_names_to_standard
    from .expression_utilities import preprocess_expression, parse_expression, create_sympy_parsing_params, substitute
except ImportError:
    from static_unit_conversion_arrays import convert_short_forms, convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_units_and_dimensions, convert_alternative_names_to_standard
    from expression_utilities import preprocess_expression, parse_expression, create_sympy_parsing_params, substitute

parse_error_warning = lambda x: f"`{x}` could not be parsed as a valid mathematical expression. Ensure that correct notation is used, that the expression is unambiguous and that all parentheses are closed."

def evaluation_function(response, answer, params) -> dict:
    """
    Function that provides some basic dimensional analysis functionality.
    """

    feedback = {}
    default_rtol = 1e-12
    if "substitutions" in params.keys():
        unsplittable_symbols = tuple()
    else:
        unsplittable_symbols = names_of_prefixes_units_and_dimensions

    parameters = {"comparison": "expression", "strict_syntax": True}
    parameters.update(params)

    remark = ""
    if "per" not in sum([[x[0]]+x[1] for x in parameters.get("input_symbols",[])],[]):
        if (" per " in response):
            remark += "Note that 'per' was interpreted as '/'. This can cause ambiguities. It is recommended to use parentheses to make your entry unambiguous."
        if (" per " in answer):
            raise Exception("Note that 'per' is interpreted as '/'. This can cause ambiguities. Use '/' and parenthesis and ensure the answer is unambiguous.")
        answer = substitute(answer+" ", convert_alternative_names_to_standard+[(" per ","/")])[0:-1]
        response = substitute(response+" ", convert_alternative_names_to_standard+[(" per ","/")])[0:-1]


    if not isinstance(answer,str):
        raise Exception("No answer was given.")
    if not isinstance(response,str):
        return {"is_correct": False, "feedback": "No response submitted."}

    answer = answer.strip()
    response = response.strip()
    if len(answer) == 0:
        raise Exception("No answer was given.")
    if len(response) == 0:
        return {"is_correct": False, "feedback": "No response submitted."}

    answer, response = preprocess_expression([answer, response],parameters)
    parsing_params = create_sympy_parsing_params(parameters, unsplittable_symbols=unsplittable_symbols)

    if parameters["strict_syntax"]:
        if "^" in response:
            separator = "" if len(remark) == 0 else "\n"
            remark += separator+"Note that `^` cannot be used to denote exponentiation, use `**` instead."
        if "^" in answer:
            raise Exception("Note that `^` cannot be used to denote exponentiation, use `**` instead.")

    if parameters["comparison"] == "buckinghamPi":
        # Parse expressions for groups in response and answer
        response_strings = response.split(',')
        response_number_of_groups = len(response_strings)
        response_number_of_groups = len(response_strings)
        response_groups = []
        for res in response_strings:
            try:
                expr = parse_expression(res,parsing_params).simplify()
                expr = expr.expand(power_base=True, force=True)
            except Exception as e:
                separator = "" if len(remark) == 0 else "\n"
                return {"is_correct": False, "feedback": parse_error_warning(response)+separator+remark}
            if isinstance(expr,Add):
                response_groups += list(expr.args)
            else:
                response_groups.append(expr)
        if answer == "-":
            answer_strings = []
        else:
            answer_strings = answer.split(',')
            answer_number_of_groups = len(answer_strings)
        answer_groups = []
        for ans in answer_strings:
            try:
                expr = parse_expression(ans,parsing_params).simplify()
                expr = expr.expand(power_base=True, force=True)
            except Exception as e:
                raise Exception("SymPy was unable to parse the answer") from e
            if isinstance(expr,Add):
                answer_groups += list(expr.args)
            else:
                answer_groups.append(expr)

        remark = ""

        # Find what different symbols for quantities there are
        if "quantities" in parameters.keys():
            quantities_strings = parameters["quantities"]
            quantities = []
            index = quantities_strings.find("(")
            while index > -1:
                index_match = find_matching_parenthesis(quantities_strings,index)
                try:
                    quantity_strings = eval(quantities_strings[index+1:index_match])
                    quantity = tuple(map(lambda x: parse_expression(x,parsing_params),quantity_strings))
                    quantities.append(quantity)
                except Exception as e:
                    raise Exception("List of quantities not written correctly.")
                index = quantities_strings.find('(',index_match+1)
            response_symbols = list(map(lambda x: x[0], quantities))
            answer_symbols = response_symbols
    
            # Check how many dimensionless groups are needed
            dimension_symbols = set()
            for quantity in quantities:
                dimension_symbols = dimension_symbols.union(quantity[1].free_symbols)
            quantity_matrix = get_exponent_matrix([q[1] for q in quantities],dimension_symbols)
            number_of_groups = len(quantities)-quantity_matrix.rank()
    
            if answer_groups == []:
                # Compute answer groups
                nullspace_basis = quantity_matrix.T.nullspace()
                for basis_vector in nullspace_basis:
                    multiplier = 1
                    for i in range(0,basis_vector.rows):
                        if not isinstance(basis_vector[i,0],Integer):
                            multiplier *= 1/basis_vector[i,0]
                    if multiplier != 1:
                        for i in range(0,basis_vector.rows):
                            basis_vector[i,0] = round(basis_vector[i,0]*multiplier)
                answer_groups = [1]*number_of_groups
                for i in range(0,len(answer_groups)):
                    for j in range(0,len(quantities)):
                        answer_groups[i] *= quantities[j][0]**nullspace_basis[i][j]

            if answer == "-":
                answer_number_of_groups = number_of_groups

            # Analyse dimensions of answers and responses
            answer_dimensions = []
            for group in answer_groups:
                dimension = group
                for quantity in quantities:
                    dimension = dimension.subs(quantity[0],quantity[1])
                answer_dimensions.append(dimension.simplify())
            
            # Check that answers are dimensionless
            for k,dimension in enumerate(answer_dimensions):
                if not dimension.is_constant():
                    raise Exception(f"Answer {answer_groups[k]} is not dimensionless.")
            
            # Check that there is a sufficient number of independent groups in the answer
            answer_matrix = get_exponent_matrix(answer_groups,answer_symbols)
            if answer_matrix.rank() < number_of_groups:
                raise Exception(f"Answer contains to few independent groups. It has {answer_matrix.rank()} independent groups and needs at least {number_of_groups} independent groups.")

            response_symbols = set()
            for res in response_groups:
                response_symbols = response_symbols.union(res.free_symbols)
            answer_symbols = set()
            for ans in answer_groups:
                answer_symbols = answer_symbols.union(ans.free_symbols)
            if not response_symbols.issubset(answer_symbols):
                feedback.update({"feedback": f"The following symbols in the response were not expected {response_symbols.difference(answer_symbols)}."})
                return {"is_correct": False, **feedback}
            answer_symbols = list(answer_symbols)

            # Check that responses are dimensionless
            response_dimensions = []
            for group in response_groups:
                dimension = group
                for quantity in quantities:
                    dimension = dimension.subs(quantity[0],quantity[1])
                response_dimensions.append(dimension.simplify())
            for k,dimension in enumerate(response_dimensions):
                if not dimension.is_constant():
                    feedback.update({"feedback": f"Response {response_groups[k]} is not dimensionless."})
                    return {"is_correct": False, **feedback}
    
            # Check that there is a sufficient number of independent groups in the response
            response_matrix = get_exponent_matrix(response_groups,response_symbols)
            if response_matrix.rank() < number_of_groups:
                feedback.update({"feedback": f"Response contains to few independent groups. It has {response_matrix.rank()} independent groups and needs at least {number_of_groups} independent groups."})
                return {"is_correct": False, **feedback}
            if response_number_of_groups > number_of_groups:
                remark = "Response has more groups than necessary."
        else:
            response_symbols = set()
            for res in response_groups:
                response_symbols = response_symbols.union(res.free_symbols)
            answer_symbols = set()
            for ans in answer_groups:
                answer_symbols = answer_symbols.union(ans.free_symbols)
            if not response_symbols.issubset(answer_symbols):
                feedback.update({"feedback": f"The following symbols in the response were not expected {response_symbols.difference(answer_symbols)}."})
                return {"is_correct": False, **feedback}
            answer_symbols = list(answer_symbols)
    
        # Extract exponents from answers and responses and compare matrix ranks
        sum_add_independent = lambda s: f"Sum in {s} group contains more independent terms that there are groups in total. Group expressions should ideally be written as a comma-separated list where each item is an entry of the form `q_1**c_1*q_2**c_2*...*q_n**c_n`."
        separator = "" if len(remark) == 0 else "\n"
        answer_matrix = get_exponent_matrix(answer_groups,answer_symbols)
        if answer_matrix.rank() > answer_number_of_groups:
            raise Exception(sum_add_independent("answer"))
        response_matrix = get_exponent_matrix(response_groups,answer_symbols)
        if response_matrix.rank() > response_number_of_groups:
            return {"is_correct": False, "feedback": sum_add_independent("response")+separator+remark}
        enhanced_matrix = answer_matrix.col_join(response_matrix)
        if answer_matrix.rank() == enhanced_matrix.rank() and response_matrix.rank() == enhanced_matrix.rank():
            return {"is_correct": True, "feedback": feedback.get("feedback","")+separator+remark}
        return {"is_correct": False, "feedback": feedback.get("feedback","")+separator+remark}

    list_of_substitutions_strings = parameters.get("substitutions",[])
    if isinstance(list_of_substitutions_strings,str):
        list_of_substitutions_strings = [list_of_substitutions_strings]

    if "quantities" in parameters.keys():
        list_of_substitutions_strings = [parameters["quantities"]]+list_of_substitutions_strings

    if not (isinstance(list_of_substitutions_strings,list) and all(isinstance(element,str) for element in list_of_substitutions_strings)):
        raise Exception("List of substitutions not written correctly.")

    try:
        interp = {"response_latex": expression_to_latex(response,parameters,parsing_params,remark)}
    except Exception as e:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parse_error_warning(response)+separator+remark}

    substitutions = []
    for subs_strings in list_of_substitutions_strings:
        # Parsing list of substitutions
        sub_substitutions = []
        index = subs_strings.find('(')
        while index > -1:
            index_match = find_matching_parenthesis(subs_strings,index)
            try:
                sub_substitutions.append(eval(subs_strings[index:index_match+1]))
            except Exception as e:
                raise Exception("List of substitutions not written correctly.")
            index = subs_strings.find('(',index_match+1)
            if index > -1 and subs_strings.find('|',index_match,index) > -1:
                # Substitutions are sorted so that the longest possible part of the original string will be substituted in each step
                sub_substitutions.sort(key=lambda x: -len(x[0]))
                substitutions.append(sub_substitutions)
                sub_substitutions = []
        sub_substitutions.sort(key=lambda x: -len(x[0]))
        substitutions.append(sub_substitutions)

    if "substitutions" not in parameters.keys():
        if "quantities" in parameters.keys():
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
        res = parse_expression(response,parsing_params)
    except Exception as e:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parse_error_warning(response)+separator+remark}

    try:
        ans = parse_expression(answer,parsing_params)
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
            ans = ans.subs(Symbol('pi'),float(pi))
        equal_up_to_multiplication = bool(simplify(res/ans).is_constant() and res != 0)
        error_below_atol = False
        error_below_rtol = False
        if equal_up_to_multiplication:
            if ans.free_symbols == res.free_symbols:
                for symbol in ans.free_symbols:
                    ans = ans.subs(symbol,1)
                    res = res.subs(symbol,1)
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

def find_matching_parenthesis(string,index):
    depth = 0
    for k in range(index,len(string)):
        if string[k] == '(':
            depth += 1
            continue
        if string[k] == ')':
            depth += -1
            if depth == 0:
                return k
    return -1

def get_exponent_matrix(expressions,symbols):
    exponents_list = []
    for expression in expressions:
        exponents = []
        for symbol in symbols:
            exponent = expression.as_coeff_exponent(symbol)[1]
            if exponent == 0:
                exponent = -expression.subs(symbol,1/symbol).as_coeff_exponent(symbol)[1]
            exponents.append(exponent)
        exponents_list.append(exponents)
    return Matrix(exponents_list)

def expression_to_latex(expression,parameters,parsing_params,remark):
    do_transformations = parsing_params.get("do_transformations",False)
    unsplittable_symbols = parsing_params.get("unsplittable_symbols",())
    symbol_dict = parsing_params.get("symbol_dict",{})
    if "quantities" not in parameters.keys():
        subs = convert_short_forms
        expression = substitute(expression,subs)
    try:
        expression_preview = parse_expression(expression,parsing_params)
    except Exception as e:
        separator = "" if len(remark) == 0 else "\n"
        return {"is_correct": False, "feedback": parse_error_warning(expression)+separator+remark}

    symbs = expression_preview.atoms(Symbol)
    symbs_dic = {str(x): Symbol(str(x),commutative=False) for x in symbs}
    parsing_params_latex = parsing_params.copy()
    parsing_params_latex["symbol_dict"] = symbs_dic
    expression_preview = parse_expression(expression,parsing_params_latex)
    symbol_names = {}
    for x in symbs_dic.values():
        symbol_names.update({x: "~\mathrm{"+str(x)+"}"})
    latex_str = latex(expression_preview,symbol_names=symbol_names)
    for symbol in symbs_dic.keys():
        if symbol not in symbol_dict.keys() and symbol not in unsplittable_symbols:
            if symbol in globals():
                del(globals()[symbol])
    return latex_str