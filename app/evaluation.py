from sympy.parsing.sympy_parser import parse_expr, split_symbols_custom
from sympy.parsing.sympy_parser import T as parser_transformations
from sympy import simplify, latex, Matrix

try:
    from .unit_system_conversions import convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_base_SI_units_and_dimensions
except ImportError:
    from unit_system_conversions import convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_base_SI_units_and_dimensions

def evaluation_function(response, answer, params) -> dict:
    """
    Funtion that provides some basic dimensional analysis functionality.
    """
    feedback = {} #{"feedback": f"{answer} {response} {params}"}
    default_rtol = 1e-12
    if "substitutions" in params.keys():
        unsplittable_symbols = tuple()
    else:
        unsplittable_symbols = names_of_prefixes_base_SI_units_and_dimensions()

    if "input_symbols" in params.keys():
        unsplittable_symbols += tuple(x[0] for x in params["input_symbols"])

    parameters = {"comparison": "expression", "strict_syntax": True}
    parameters.update(params)

    do_transformations = not parameters["strict_syntax"]

    if parameters["comparison"] == "buckinghamPi":
        # Parse expressions for groups in response and answer
        response_strings = response.split(',')
        response_groups = []
        for res in response_strings:
            try:
                expr = parse_expression(res,do_transformations,unsplittable_symbols).simplify()
            except (SyntaxError, TypeError) as e:
                raise Exception("SymPy was unable to parse the response") from e
            response_groups.append(expr)
        if answer == "-":
            answer_strings = []
        else:
            answer_strings = answer.split(',')
        answer_groups = []
        for ans in answer_strings:
            try:
                expr = parse_expression(ans,do_transformations,unsplittable_symbols).simplify()
            except (SyntaxError, TypeError) as e:
                raise Exception("SymPy was unable to parse the answer") from e
            answer_groups.append(expr)
    
        # Find what different symbols for quantities there are
        if "quantities" in parameters.keys():
            quantities_strings = parameters["quantities"]
            quantities = []
            index = quantities_strings.find("(")
            while index > -1:
                index_match = find_matching_parenthesis(quantities_strings,index)
                try:
                    quantity_strings = eval(quantities_strings[index+1:index_match])
                    quantity = tuple(map(lambda x: parse_expression(x,do_transformations,unsplittable_symbols),quantity_strings))
                    quantities.append(quantity)
                except (SyntaxError, TypeError) as e:
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
                answer_groups = [1]*number_of_groups
                for i in range(0,len(answer_groups)):
                    for j in range(0,len(quantities)):
                        answer_groups[i] *= quantities[j][0]**nullspace_basis[i][j]
    
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
                return {"is_correct": False, **feedback}
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
        answer_matrix = get_exponent_matrix(answer_groups,answer_symbols)
        response_matrix = get_exponent_matrix(response_groups,answer_symbols)
        enhanced_matrix = answer_matrix.col_join(response_matrix)
        if answer_matrix.rank() == enhanced_matrix.rank() and response_matrix.rank() == enhanced_matrix.rank():
            return {"is_correct": True, **feedback}
        return {"is_correct": False, **feedback}

    list_of_substitutions_strings = parameters.get("substitutions",[])
    if isinstance(list_of_substitutions_strings,str):
        list_of_substitutions_strings = [list_of_substitutions_strings]

    if "quantities" in parameters.keys():
        list_of_substitutions_strings = [parameters["quantities"]]+list_of_substitutions_strings

    if not (isinstance(list_of_substitutions_strings,list) and all(isinstance(element,str) for element in list_of_substitutions_strings)):
        raise Exception("List of substitutions not written correctly.")

    substitutions = []
    for subs_strings in list_of_substitutions_strings:
        # Parsing list of substitutions
        sub_substitutions = []
        index = subs_strings.find('(')
        while index > -1:
            index_match = find_matching_parenthesis(subs_strings,index)
            try:
                sub_substitutions.append(eval(subs_strings[index:index_match+1]))
            except (SyntaxError, TypeError) as e:
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
            substitutions += convert_to_SI_base_units()
        else:
            substitutions += convert_to_SI_base_units_short_form()
        if parameters["comparison"] == "dimensions":
            if "quantities" in parameters.keys():
                substitutions += convert_SI_base_units_to_dimensions()
            else:
                substitutions += convert_SI_base_units_to_dimensions_short_form()

#    new_answer = answer
#    new_response = response
    for sub in substitutions:
#        answer = substitute(answer, sub)
        answer = new_substitute(answer, sub)
#        response = substitute(response, sub)
        response = new_substitute(response, sub)

#    if new_answer != answer or new_response != response:
#        return {"is_correct": False}

    # Safely try to parse answer and response into symbolic expressions
    try:
        res = parse_expression(response,do_transformations,unsplittable_symbols)
    except (SyntaxError, TypeError) as e:
        raise Exception(f"SymPy was unable to parse the response {response}") from e

    try:
        ans = parse_expression(answer,do_transformations,unsplittable_symbols)
    except (SyntaxError, TypeError) as e:
        raise Exception(f"SymPy was unable to parse the answer {answer}") from e

    # Add how res was interpreted to the response
    interp = {"response_latex": latex(res)}

    if parameters["comparison"] == "dimensions":
        is_correct = bool(simplify(res/ans).is_constant() and res != 0)
        if is_correct:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp, **feedback}

    if parameters["comparison"] == "expression":
        equal_up_to_multiplication = bool(simplify(res/ans).is_constant() and res != 0)
        if ans.free_symbols == res.free_symbols:
            for symbol in ans.free_symbols:
                ans = ans.subs(symbol,1)
                res = res.subs(symbol,1)
        if "atol" in parameters.keys():
            error_below_atol = bool(abs(float(ans-res)) < float(parameters["atol"]))
        else:
            error_below_atol = True
        if "rtol" in parameters.keys():
            parameters["rtol"] = eval(parameters["rtol"])
            error_below_rtol = bool(abs(((ans-res)/ans).evalf()) < parameters["rtol"])
        else:
            if "atol" in parameters.keys():
                error_below_rtol = True
            else:
                error_below_rtol = bool(abs(((ans-res)/ans).evalf()) < default_rtol)
        if error_below_atol and error_below_rtol and equal_up_to_multiplication:
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

def substitute(string, substitutions):
    if isinstance(string,str):
        string = [string]

    # Perform substitutions
    for k,pair in enumerate(substitutions):
        new_string = []
        for part in string:
            if not isinstance(part, str):
                new_string.append(part)
            else:
                substitution_locations = []
                i = part.find(pair[0])
                while i > -1:
                    substitution_locations.append(i)
                    i = part.find(pair[0],i+len(pair[0]))
                j = 0
                for i in substitution_locations:
                    if i > 0:
                        new_string.append(part[j:i])
                    new_string.append(k)
                    j = i + len(pair[0])
                if j < len(part):
                    new_string.append(part[j:len(part)])
        if len(new_string) >= len(string):
            string = new_string

    for k, elem in enumerate(string):
        if isinstance(elem,int):
            string[k] = substitutions[elem][1]

    return "".join(string)

def new_substitute(string, substitutions):
    if isinstance(string,str):
        string = [string]

    # Perform substitutions
    new_string = []
    for part in string:
        if not isinstance(part, str):
            new_string.append(part)
        else:
            index = 0
            string_buffer = ""
            while index < len(part):
                matched_start = False
                for k,pair in enumerate(substitutions):
                    if part.startswith(pair[0],index):
                        matched_start = True
                        if len(string_buffer) > 0:
                            new_string.append(string_buffer)
                            string_buffer = ""
                        new_string.append(k)
                        index += len(pair[0])
                        break
                if not matched_start:
                    string_buffer += part[index]
                    index += 1
            if len(string_buffer) > 0:
                new_string.append(string_buffer)

    for k, elem in enumerate(new_string):
        if isinstance(elem,int):
            new_string[k] = substitutions[elem][1]

    return "".join(new_string)

def parse_expression(expr,do_transformations,unsplittable_symbols):
    if do_transformations:
        transformations = parser_transformations[0:4,6,8]+(split_symbols_custom(lambda x: x not in unsplittable_symbols),)+parser_transformations[8]
    else:
        transformations = parser_transformations[0:4]
    return parse_expr(expr,transformations=transformations)

def get_exponent_matrix(expressions,symbols):
    exponents_list = []
    for expression in expressions:
        exponents = []
        for symbol in symbols:
            exponents.append(expression.as_coeff_exponent(symbol)[1])
        exponents_list.append(exponents)
    return Matrix(exponents_list)