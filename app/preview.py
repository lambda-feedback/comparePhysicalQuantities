import re
from typing import Any, Dict, List, TypedDict

from sympy import simplify, latex, Symbol, Integer, Add, Subs, pi, posify
import sympy
from latex2sympy2 import latex2sympy

from .static_unit_conversion_arrays import convert_short_forms, convert_to_SI_base_units, convert_to_SI_base_units_short_form, convert_SI_base_units_to_dimensions, convert_SI_base_units_to_dimensions_short_form, names_of_prefixes_units_and_dimensions, convert_alternative_names_to_standard
from .expression_utilities import preprocess_expression, parse_expression, create_sympy_parsing_params, substitute

class Params(TypedDict):
    pass

class Result(TypedDict):
    preview: Any

class Preview(TypedDict):
    latex: str
    sympy: str

class SymbolData(TypedDict):
    latex: str
    aliases: List[str]

SymbolDict = Dict[str, SymbolData]

symbol_latex_re = re.compile(
    r"(?P<start>\\\(|\$\$|\$)(?P<latex>.*?)(?P<end>\\\)|\$\$|\$)"
)

def extract_latex(symbol):
    """Returns the latex portion of a symbol string.

    Note:
        Only the first matched expression is returned.

    Args:
        symbol (str): The string to extract latex from.

    Returns:
        str: The latex string.
    """
    if (match := symbol_latex_re.search(symbol)) is None:
        return symbol

    return match.group("latex")

def parse_latex(response: str, symbols: SymbolDict) -> str:
    """Parse a LaTeX string to a sympy string while preserving custom symbols.

    Args:
        response (str): The LaTeX expression to parse.
        symbols (SymbolDict): A mapping of sympy symbol strings and LaTeX
        symbol strings.

    Raises:
        ValueError: If the LaTeX string or symbol couldn't be parsed.

    Returns:
        str: The expression in sympy syntax.
    """
    substitutions = {}

    for sympy_symbol_str in symbols:
        symbol_str = symbols[sympy_symbol_str]["latex"]
        latex_symbol_str = extract_latex(symbol_str)

        try:
            latex_symbol = latex2sympy(latex_symbol_str)
        except Exception:
            raise ValueError(
                f"Couldn't parse latex symbol {latex_symbol_str} "
                f"to sympy symbol."
            )

        substitutions[latex_symbol] = sympy.Symbol(sympy_symbol_str)

    try:
        expression = latex2sympy(response, substitutions)

        if isinstance(expression, list):
            expression = expression.pop()

        return str(expression.xreplace(substitutions))  # type: ignore

    except Exception as e:
        raise ValueError(str(e))

def expression_to_latex(expression,parameters,parsing_params):
    unsplittable_symbols = parsing_params.get("unsplittable_symbols",())
    symbol_dict = parsing_params.get("symbol_dict",{})
    if not (len(parameters.get("quantities",[])) > 0 or parsing_params.get("elementary_functions",False) == True or parsing_params.get("comparison","") == "buckinghamPi"):
        subs = convert_short_forms
        expression = substitute(expression,subs)
    try:
        expression_preview = parse_expression(expression,parsing_params)
    except Exception as exc:
        raise ValueError("Cannot parse response") from exc

    symbs_dic = {}
    symbol_names = {}
    if not len(parameters.get("quantities",[])) > 0:
        symbs = expression_preview.atoms(Symbol)
        symbs_dic = {str(x): Symbol(str(x),commutative=False) for x in symbs}
        parsing_params_latex = parsing_params.copy()
        parsing_params_latex["symbol_dict"] = symbs_dic
        expression_preview = parse_expression(expression,parsing_params_latex)
        for x in symbs_dic.values():
            symbol_names.update({x: "~\\mathrm{"+str(x)+"}"})
    latex_str = latex(expression_preview,symbol_names=symbol_names)
    sympy_str = str(expression_preview)
    for symbol in symbs_dic.keys():
        if symbol not in symbol_dict.keys() and symbol not in unsplittable_symbols:
            if symbol in globals():
                del(globals()[symbol])
    return latex_str, sympy_str

def find_matching_parenthesis(string, index, delimiters=None):
    depth = 0
    if delimiters == None:
        delimiters = ('(', ')')
    for k in range(index, len(string)):
        if string[k] == delimiters[0]:
            depth += 1
            continue
        if string[k] == delimiters[1]:
            depth += -1
            if depth == 0:
                return k
    return -1

def sanitise_latex(response):
    response = response.replace('~',' ')
    response = "".join(response.split())
    wrappers = [r"\mathrm",r"\text"]
    for wrapper in wrappers:
        processed_response = []
        index = 0
        while index < len(response):
            wrapper_start = response.find(wrapper+"{", index)
            if wrapper_start > -1:
                processed_response.append(response[index:wrapper_start])
                wrapper_end = find_matching_parenthesis(response, wrapper_start+1, delimiters=('{','}'))
                inside_wrapper = response[(wrapper_start+len(wrapper+"{")):wrapper_end]
                processed_response.append(inside_wrapper)
                index = wrapper_end+1
            else:
                processed_response.append(response[index:])
                index = len(response)
        response = "".join(processed_response)
    return response

def preview_function(response: Any, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """

    response = sanitise_latex(response)

    symbols = params.get("symbols", {})
    if params.get("is_latex", False):
        if ',' in response:
            responses = response.split(',')
            resp_list = []
            for resp in responses:
                resp_list.append(parse_latex(resp, symbols))
            response = ",".join(resp_list)
        else:
            response = parse_latex(response, symbols)

    if "substitutions" in params.keys() or params.get("comparison", "") == "buckinghamPi":
        unsplittable_symbols = tuple()
    else:
        unsplittable_symbols = names_of_prefixes_units_and_dimensions

    parameters = {"comparison": "expression", "strict_syntax": True}
    parameters.update(params)

    response = preprocess_expression([response],parameters)[0]
    parsing_params = create_sympy_parsing_params(parameters, unsplittable_symbols=unsplittable_symbols)
    parsing_params.update({"comparison": parameters["comparison"]})

    if "per" not in sum([[x[0]]+x[1] for x in parameters.get("input_symbols",[])],[]):
        response = substitute(response+" ", convert_alternative_names_to_standard+[(" per ","/")])[0:-1]

    try:
        if parameters["comparison"] == "buckinghamPi":
            preview_latex = []
            response_strings = response.split(',')
            for current_response in response_strings:
                latex, _ = expression_to_latex(current_response, parameters, parsing_params)
                preview_latex.append(latex)
            preview_latex = ",~".join(preview_latex)
            preview_sympy = response
        else:
            preview_latex, preview_sympy = expression_to_latex(response, parameters, parsing_params)
    except Exception as exc:
        raise ValueError("Cannot parse response") from exc

    return Result(preview=Preview(latex=preview_latex, sympy=preview_sympy))
