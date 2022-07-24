def evaluation_function(response, answer, params) -> dict:
    """
    Funtion that compares two physical quantities.
    """

    from math import pi, log
    from sympy.parsing.sympy_parser import parse_expr
    from sympy import simplify, latex
    from unit_system_conversions import convert_to_SI_base_units, convert_SI_base_units_to_dimensions

    parameters = {"substitutions": convert_to_SI_base_units(), "comparison": "expression", "rtol": 1e-12 }
    parameters.update(params)

    list_of_substitutions_strings = parameters["substitutions"]
    if isinstance(list_of_substitutions_strings,str):
        list_of_substitutions_strings = [list_of_substitutions_strings]

    if "quantities" in parameters.keys():
        list_of_substitutions_strings = [parameters["quantities"]]+list_of_substitutions_strings

    if parameters["comparison"] == "dimensions":
        list_of_substitutions_strings = list_of_substitutions_strings+[convert_SI_base_units_to_dimensions()]

# REMARK: Version that uses sympys unit system to compare dimensions 
# not currently in use but might be useful for a future versions
#    if "comparison" in params.keys():
#        if params["comparison"] == "dimensions":
#            import sympy.physics.units as u
#            answer = eval(answer)
#            response = eval(response)
#            if answer == response:
#                return {"is_correct": True, "level": params["comparison"]}

    if isinstance(list_of_substitutions_strings,str):
        list_of_substitutions_strings = [list_of_substitutions_strings]
    elif not (isinstance(list_of_substitutions_strings,list) and all(isinstance(element,str) for element in list_of_substitutions_strings)):
        raise Exception("List of substitutions not written correctly.")

    for subs_strings in list_of_substitutions_strings:
        # Parsing list of substitutions
        substitutions = []
        sub_substitutions = []
        index = subs_strings.find('(')
        while index > -1:
            index_match = find_matching_parenthesis(subs_strings,index)
            try:
                sub_substitutions.append(eval(subs_strings[index+1:index_match]))
            except (SyntaxError, TypeError) as e:
                raise Exception("List of substitutions not written correctly.")
            index = subs_strings.find('(',index_match+1)
            if index > -1 and subs_strings.find('|',index_match+1,index-1) > -1:
                # Substitutions are sorted so that the longest possible part of the original string will be substituted in each step
                sub_substitutions.sort(key=lambda x: -len(x[0]))
                substitutions.append(sub_substitutions)
                sub_substitutions = []
        sub_substitutions.sort(key=lambda x: -len(x[0]))
        substitutions.append(sub_substitutions)

        for sub in substitutions:
            answer = substitute(answer, sub)
            response = substitute(response, sub)

    # Safely try to parse answer and response into symbolic expressions
    try:
        res = parse_expr(response)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the response") from e

    try:
        ans = parse_expr(answer)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the answer") from e

#    print(f"{ans.simplify()} : {res.simplify()}")

    # Add how res was interpreted to the response
    interp = {"response_latex": latex(res)}

    if parameters["comparison"] == "dimensions":
        is_correct = bool(simplify(res/ans).is_constant() and res != 0)
        if is_correct:
            return {"is_correct": True, "level": parameters["comparison"], **interp }

    if parameters["comparison"] == "expression":
        equal_up_to_multiplication = bool(simplify(res/ans).is_constant() and res != 0)
        if ans.free_symbols == res.free_symbols:
            for symbol in ans.free_symbols:
                ans.subs(symbol,1)
                res.subs(symbol,1)
        relative_error = abs(((ans-res)/ans).evalf())
        has_correct_value = bool(relative_error < parameters["rtol"])
        if has_correct_value and equal_up_to_multiplication:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp}

    if parameters["comparison"] == "expressionExact":
        # Here nsimplify is used to transform float to rationals since some unit conversions are not exact and answers and responses might contain decimal values
        is_correct = (res.nsimplify()-ans.nsimplify()).simplify() == 0
        if is_correct:
            return {"is_correct": True, "comparison": parameters["comparison"], **interp}

    return {"is_correct": False, **interp}

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
                    i = part.find(pair[0],i+1)
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