import unittest, sys

try:
    from .evaluation import evaluation_function, parse_error_warning
    from .static_unit_conversion_arrays import list_of_SI_prefixes, list_of_SI_base_unit_dimensions, list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI, convert_alternative_names_to_standard
    from .expression_utilities import elementary_functions_names, substitute
except ImportError:
    from evaluation import evaluation_function, parse_error_warning
    from static_unit_conversion_arrays import list_of_SI_prefixes, list_of_SI_base_unit_dimensions,  list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI, convert_alternative_names_to_standard
    from expression_utilities import elementary_functions_names, substitute

# If evaluation_tests is run with the command line argument 'skip_resource_intensive_tests'
# then tests marked with @unittest.skipIf(skip_resource_intensive_tests,message_on_skip)
# will be skipped. This can be used to avoid takes that take a long time when making several
# small changes with most tests running between each change
message_on_skip = "Test skipped to save on resources"
skip_resource_intensive_tests = False
if "skip_resource_intensive_tests" in sys.argv:
    skip_resource_intensive_tests = True
    sys.argv.remove("skip_resource_intensive_tests")

class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def assertEqual_input_variations(self, response, answer, params, value):
        with self.subTest(response=response, answer=answer):
            result = evaluation_function(response, answer, params)
            self.assertEqual(result.get("is_correct"), value)
        variation_definitions = [lambda x : x.replace('**','^'),
                                 lambda x : x.replace('**','^').replace('*',' '),
                                 lambda x : x.replace('**','^').replace('*','')]
        for variation in variation_definitions:
            response_variation = variation(response)
            answer_variation = variation(answer)
            if (response_variation != response) or (answer_variation != answer):
                with self.subTest(response=response_variation, answer=answer):
                    result = evaluation_function(response_variation, answer, params)
                    self.assertEqual(result.get("is_correct"), value)
                with self.subTest(response=response, answer=answer_variation):
                    result = evaluation_function(response, answer_variation, params)
                    self.assertEqual(result.get("is_correct"), value)
                with self.subTest(response=response_variation, answer=answer_variation):
                    result = evaluation_function(response_variation, answer_variation , params)
                    self.assertEqual(result.get("is_correct"), value)

    def test_invalid_user_expression(self):
        body = {"response": "3x*", "answer": "3*x"}

        result = evaluation_function(body["response"],body["answer"],{})
        self.assertEqual(result["feedback"],parse_error_warning(body["response"]))

    def test_invalid_author_expression(self):
        body = {"response": "3*x", "answer": "3x*"}

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

    def test_substitutions_replace_no_common_substrings(self):
        body = {"response": "ab",
                "answer": "c",
                "substitutions": "('a','A') ('b','B') ('c','AB')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_substitutions_replace_common_substrings_in_replacement(self):
        body = {"response": "ab",
                "answer": "c",
                "substitutions": "('a','b') ('b','d') ('c','bd')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_substitutions_replace_common_substrings_in_original(self):
        body = {"response": "ab",
                "answer": "c",
                "substitutions": "('a','d') ('ab','e') ('c','e')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_dimensions_with_substitution(self):
        response = "2*d**2/t**2+0.5*v**2"
        answer = "5*v**2"
        params = { "comparison": "dimensions",
                   "substitutions": "('d','(distance)') ('t','(time)') ('v','(distance/time)')",
                   "input_symbols": [['distance',[]],['time',[]]],
                   "strict_syntax": False}

        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_dimensions_with_defaults(self):
        answer = "length**2/time**2"
        params = { "comparison": "dimensions",
                   "strict_syntax": False}
        responses = ["metre**2/second**2",
                     "(centi*metre)**2/hour**2",
                     "246*ohm/(kilo*gram)*coulomb**2/second"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_dimensions_with_defaults(self):
        answer = "length**2/time**2"
        params = { "comparison": "dimensions",
                   "strict_syntax": False}
        responses = ["m**2/s**2",
                     "(c*m)**2/h**2",
                     "246*O/(k*g)*C**2/s"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)

    def test_dimensionless_quantities(self):
        answer = "1"
        params = {"strict_syntax": False}
        responses = ["1",
                     "s*Hz",
                     "k*kat*m*s/mol"]
        for response in responses:
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

    def test_wrong_dimensions(self):
        answer = "1"
        params = {"strict_syntax": False}
        responses = ["m",
                     "s",
                     "s*m"]
        for response in responses:
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)

    @unittest.skipIf(skip_resource_intensive_tests, message_on_skip)
    def test_alternative_names_compound_units(self):
        params = {"strict_syntax": False}
        convert_alternative_names_to_standard
        n = len(convert_alternative_names_to_standard)
        incorrect = []
        errors = []
        for i in range(0,n):
            for j in range(0,n):
                answer = convert_alternative_names_to_standard[i][1]+"*"+convert_alternative_names_to_standard[j][1]
                for prod in ["*"," ",""]:
                    left = convert_alternative_names_to_standard[i][0]
                    if isinstance(left,tuple):
                        if len(prod) == 0:
                            left = convert_alternative_names_to_standard[i][1]
                        else:
                            left = left[0]
                    right = convert_alternative_names_to_standard[j][0]
                    if isinstance(right,tuple):
                        right = right[0]
                    response = left+prod+right
                    try:
                        result = evaluation_function(response, answer, params)
                    except:
                        errors.append((answer,response))
                        continue
                    if not result.get("is_correct"):
                        incorrect.append((answer,response))
        log_details = False
        if log_details:
            f = open("test_alternative_names_compound_units_log.txt","w")
            f.write("Incorrect:\n"+"".join([str(x)+"\n" for x in incorrect])+"\nErrors:\n"+"".join([str(x)+"\n" for x in errors]))
            f.close()
            print(f"{len(incorrect)}/{3*n*n} {len(errors)}/{3*n*n} {(len(errors)+len(incorrect))/(3*n*n)}")
        self.assertEqual((len(errors)+len(incorrect))/(3*n*n) < 0.01, True)

    @unittest.skipIf(skip_resource_intensive_tests, message_on_skip)
    def test_short_form_of_units(self):
        # NOTE: Short forms for common units are not allowed
        params = {"strict_syntax": False}
        prefixes_long_forms = [x[0] for x in list_of_SI_prefixes]
        prefixes_short_forms = [x[1] for x in list_of_SI_prefixes]
        m = len(prefixes_long_forms)
        long_forms = [x[0] for x in (list_of_SI_base_unit_dimensions+list_of_derived_SI_units_in_SI_base_units)]
        short_forms = [x[1] for x in (list_of_SI_base_unit_dimensions+list_of_derived_SI_units_in_SI_base_units)]
        n = len(long_forms)
        k = 0
        incorrect = []
        errors = []
        for i in range(0,n):
            for a in range(0,m):
                answer = prefixes_long_forms[a]+"*"+long_forms[i]
                for prod in ["*"," ",""]:
                    response = prefixes_short_forms[a]+prod+short_forms[i]
                    k += 1
                    try:
                        result = evaluation_function(response, answer, params)
                    except:
                        errors.append((answer,response))
                        continue
                    if not result.get("is_correct"):
                        incorrect.append((answer,response))
        self.assertEqual(len(errors)+len(incorrect), 0)

    @unittest.skipIf(skip_resource_intensive_tests, message_on_skip)
    def test_short_form_of_compound_units(self):
        # NOTE: Short forms for common units are not allowed
        units = list_of_SI_base_unit_dimensions\
                +list_of_derived_SI_units_in_SI_base_units\
                +list_of_very_common_units_in_SI
        all_units = list_of_SI_base_unit_dimensions\
                    +list_of_derived_SI_units_in_SI_base_units\
                    +list_of_common_units_in_SI
        all_long_forms = [x[0] for x in all_units]
        params = {"strict_syntax": False}
        prefixes_long_forms = [x[0] for x in list_of_SI_prefixes]
        prefixes_short_forms = [x[1] for x in list_of_SI_prefixes]
        m = len(prefixes_long_forms)
        long_forms = [x[0] for x in units]
        short_forms = [x[1] for x in units]
        n = len(long_forms)
        k = 0
        does_not_match_convention = []
        incorrect = []
        errors = []
        for i in range(0,n):
            for j in range(0,n):
                for a in range(0,m):
                    answer = prefixes_long_forms[a]+"*"+long_forms[i]+"*"+long_forms[j]
                    for prod in ["*"," ",""]:
                        response = prefixes_short_forms[a]+prod+short_forms[i]+prod+short_forms[j]
                        # Check if case matches convention
                        if short_forms[i] in prefixes_short_forms\
                        or prefixes_short_forms[a]+prod+short_forms[i] in prefixes_short_forms\
                        or short_forms[i]+prod+short_forms[j] in short_forms\
                        or any([x in response for x in all_long_forms]):
                            does_not_match_convention.append((answer,response))
                            continue
                        k += 1
                        try:
                            result = evaluation_function(response, answer, params)
                        except:
                            errors.append((answer,response))
                            continue
                        if not result.get("is_correct"):
                            incorrect.append((answer,response))
        log_details = False
        if log_details:
            f = open("test_short_form_of_compound_units_log.txt","w")
            f.write("Incorrect:\n"+"".join([str(x)+"\n" for x in incorrect])+"\nErrors:\n"+"".join([str(x)+"\n" for x in errors])+"\nDoes not match convention:\n"+"".join([str(x)+"\n" for x in does_not_match_convention]))
            f.close()
            print(f"{len(incorrect)}/{k} {len(errors)}/{k} {(len(errors)+len(incorrect))/k} {len(does_not_match_convention)}/{k+len(does_not_match_convention)} {len(does_not_match_convention)/(k+len(does_not_match_convention))}")
        self.assertEqual((len(errors)+len(incorrect))/k < 0.001, True)

    def test_compare_quantities_with_substitutions(self):
        response = "(d/t)**2/(3600**2)+v**2"
        answer = "2*v**2"
        params = {"substitutions": "('d','(km)') ('t','(s)') ('v','(km/h)') | ('k','1000*') ('h','(60*60*s)')",
                  "strict_syntax": False}

        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_substitutions_short_form_strict(self):
        derived_units = "('W','(J/s)')|('J','(N*m)') ('Pa','(N/(m**2))')|('N','(m*(k*g)/(s**2))')"
        prefixes = "('M','10**6') ('k','10**3') ('h','10**2') ('da','10**1') ('d','10**(-1)') ('c','10**(-2)') ('mu','10**(-6)')"
        milli_fix = "('mW','10**(-3)*W') ('mJ','10**(-3)*J') ('mPa','10**(-3)*Pa') ('mN','10**(-3)*N') ('mm','10**(-3)*m') ('mg','10**(-3)*g') ('ms','10**(-3)*s')"
        substitutions = milli_fix+"|"+derived_units+"|"+prefixes
        params = {"substitutions": substitutions, "strict_syntax": True}
        answer = "1.23*W"
        responses = ["123*c*W",
                     "0.00000123*M*W",
                     "0.00123*k*W",
                     "0.0123*h*W",
                     "0.123*da*W",
                     "12.3*d*W",
                     "123*c*W",
                     "1230*mW",
                     "1230000*mu*W",
                     "1.23*J/s",
                     "1.23*N*m/s",
                     "1.23*Pa*m**3/s"]
        for response in responses:
            result = evaluation_function(response, answer, params)
            self.assertEqual(result.get("is_correct"), True)

    def test_compare_quantities_with_substitutions_short_form(self):
        derived_units = "('W','(J/s)')|('J','(N*m)') ('Pa','(N/(m**2))')|('N','(m*(k*g)/(s**2))')"
        prefixes = "('M','(10**6)') ('k','(10**3)') ('h','(10**2)') ('da','(10**1)') ('d','(10**(-1))') ('c','(10**(-2))') ('mu','(10**(-6))')"
        milli_fix = "('mW','(10**(-3))*W') ('mJ','(10**(-3))*J') ('mPa','(10**(-3))*Pa') ('mN','(10**(-3))*N') ('mm','(10**(-3))*m') ('mg','(10**(-3))*g') ('ms','(10**(-3))*s')"
        substitutions = milli_fix+"|"+derived_units+"|"+prefixes
        params = {"substitutions": substitutions, "strict_syntax": False}
        answer = "1.23*W"
        responses = ["123*c*W",
                     "0.00000123*M*W",
                     "0.00123*k*W",
                     "0.0123*h*W",
                     "0.123*da*W",
                     "12.3*d*W",
                     "123*c*W",
                     "1230*mW",
                     "1230000*mu*W",
                     "1.23*J/s",
                     "1.23*N*m/s",
                     "1.23*Pa*m**3/s"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_costs_in_different_currencies_with_substitutions(self):
        # Based on Bank of England daily spot rates 01-08-2022
        currencies = "('EUR','(1/1.1957)*GBP') ('USD','(1/1.2283)*GBP') ('CNY','(1/8.3104)*GBP') ('INR','(1/96.9430)*GBP')"
        params = {"substitutions": currencies,
                  "atol": "0.005",
                  "input_symbols": [['GBP',[]],['EUR',[]],['USD',[]],['CNY',[]],['INR',[]]],
                  "strict_syntax": False}
        answer = "10.00*GBP"
        responses = ["11.96*EUR", "12.28*USD", "83.10*CNY", "969.43*INR"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_costs_in_different_currencies_with_substitutions_and_input_symbols(self):
        # Based on Bank of England daily spot rates 01-08-2022
        currencies = "('EUR','(1/1.1957)*GBP') ('USD','(1/1.2283)*GBP') ('CNY','(1/8.3104)*GBP') ('INR','(1/96.9430)*GBP')"
        params = {"substitutions": currencies,
                  "atol": "0.005",
                  "input_symbols": [['GBP',[]],['EUR',[]],['USD',[]],['CNY',[]],['INR',[]]],
                  "strict_syntax": False}
        answer = "10.00*GBP"
        responses = ["11.96*EUR", "12.28*USD", "83.10*CNY", "969.43*INR"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_defaults(self):
        response = "(d/t)**2*((1/3.6)**2)+v**2"
        answer = "2*v**2"
        params = { "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')",
                   "strict_syntax": False}

        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_defaults_exact(self):
        response = "(d/t)**2*((1/3.6)**2)+v**2"
        answer = "2*v**2"
        params = {"comparison": "expressionExact",
                  "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')",
                  "strict_syntax": False}

        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_defaults_and_alternatives(self):
        params = { "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')",
                   "input_symbols": [['d',['distance','D']],['t',['time','T']],['v',['velocity','speed','V']]],
                   "strict_syntax": False}

        response = "(distance/time)**2*((1/3.6)**2)+velocity**2"
        answer = "2*speed**2"
        self.assertEqual_input_variations(response, answer, params, True)

        response = "(D/T)**2*((1/3.6)**2)+2*V**2-velocity**2"
        answer = "2*v**2"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_defaults_and_short_alternatives(self):
        params = { "quantities": "('distance','(metre)') ('time','(second)') ('velocity','(kilo*metre/hour)')",
                   "input_symbols": [['distance',['d','D']],['time',['t','T']],['velocity',['v','speed','s']]],
                   "strict_syntax": False}

        response = "(distance/time)**2*((1/3.6)**2)+velocity**2"
        answer = "2*speed**2"
        self.assertEqual_input_variations(response, answer, params, True)

        response = "(D/T)**2*((1/3.6)**2)+2*s**2-velocity**2"
        answer = "2*v**2"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_compare_quantities_with_rtol(self):
        for k in [1,2,3]:
            # Checks that sufficiently accurate responses are considered correct
            answer = "111111*metre"
            params = {"rtol": "0."+"0"*k+"1", "strict_syntax": False}
            response = "1"*(k+1)+"0"*(4-k)+"*deka*metre"
            self.assertEqual_input_variations(response, answer, params, True)
            # Checks that insufficiently accurate responses are considered wrong
            response = "1"*k+"0"*(5-k)+"*metre"
            self.assertEqual_input_variations(response, answer, params, False)
            # Check that rtol can be specified as a float
            params["rtol"] = float(params["rtol"])
            response = "1"*(k+1)+"0"*(4-k)+"*deka*metre"
            self.assertEqual_input_variations(response, answer, params, True)
            response = "1"*k+"0"*(5-k)+"*metre"
            self.assertEqual_input_variations(response, answer, params, False)

    def test_compare_quantities_with_rtol_short_form(self):
        correct_results = []
        incorrect_results = []
        for k in [1,2,3]:
            # Checks that sufficiently accurate responses are considered correct
            response = "1"*(k+1)+"0"*(4-k)+"*da*m"
            answer = "111111*m"
            params = {"rtol": "0."+"0"*k+"1", "strict_syntax": False}
            self.assertEqual_input_variations(response, answer, params, True)
            # Checks that insufficiently accurate responses are considered wrong
            response = "1"*k+"0"*(5-k)+"*m"
            self.assertEqual_input_variations(response, answer, params, False)

    def test_compare_quantities_with_atol(self):
        answer = "1.0*metre"
        params = {"atol": "0.05", "strict_syntax": False}
        responses = ["1.04*metre", "0.96*metre"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)
        responses = ["1.06*metre", "0.94*metre"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, False)

    def test_compare_quantities_with_atol_short_form(self):
        answer = "1.0*m"
        params = {"atol": "0.05", "strict_syntax": False}
        responses = ["1.04*m", "0.96*m"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, True)
        responses = ["1.06*m", "0.94*m"]
        for response in responses:
            self.assertEqual_input_variations(response, answer, params, False)

    def test_compare_quantities_with_atol_and_rtol(self):
        answer = "1.0*kilo*metre"
        # Both absolute and relative error small enough
        response = "1098*metre"
        params = {"atol": "100", "rtol": "0.1", "strict_syntax": False}
        self.assertEqual_input_variations(response, answer, params, True)
        # Both absolute and relative error too large
        response = "1102*metre"
        self.assertEqual_input_variations(response, answer, params, False)
        # Absolute error small enough and relative error too large
        response = "1098*metre"
        params.update({"atol": "100", "rtol": "0.05"})
        self.assertEqual_input_variations(response, answer, params, False)
        # Absolute error too large and relative error small enough
        response = "1098*metre"
        params.update({"atol": "50", "rtol": "0.1"})
        self.assertEqual_input_variations(response, answer, params, False)

    def test_compare_quantities_with_atol_and_rtol_short_form(self):
        answer = "1.0*k*m"
        # Both absolute and relative error small enough
        response = "1098*m"
        params = {"atol": "100", "rtol": "0.1", "strict_syntax": False}
        self.assertEqual_input_variations(response, answer, params, True)
        # Both absolute and relative error too large
        response = "1102*m"
        self.assertEqual_input_variations(response, answer, params, False)
        # Absolute error small enough and relative error too large
        response = "1098*m"
        params.update({"atol": "100", "rtol": "0.05"})
        self.assertEqual_input_variations(response, answer, params, False)
        # Absolute error too large and relative error small enough
        response = "1098*m"
        params.update({"atol": "50", "rtol": "0.1"})
        self.assertEqual_input_variations(response, answer, params, False)

    def test_buckingham_pi_one_group(self):
        answer = "U*L/nu"
        params = {"comparison": "buckinghamPi", "input_symbols": [['U',[]],['L',[]],['nu',[]]], "strict_syntax": False}
        correct_responses = ["U*L/nu",
                             "L*U/nu",
                             "nu/U/L",
                             "(U*L/nu)**2",
                             "2*U*L/nu"]
        incorrect_responses = ["U*L/n/u",
                               "1",
                               "U*L*nu",
                               "A*U*L/nu",
                               "A",
                               "U/nu",
                               "U*L"]
        for response in correct_responses:
            self.assertEqual_input_variations(response, answer, params, True)
        for response in incorrect_responses:
            self.assertEqual_input_variations(response, answer, params, False)

    def test_buckingham_pi_two_groups(self):
        params = {"comparison": "buckinghamPi", "strict_syntax": False,
                  "input_symbols": [['g',[]],['v',[]],['h',[]],['l',[]]]}
        # This corresponds to p1 = 1, p2 = 2, q1 = 3, q2 = 4
        answer = "g**(-2)*v**4*h*l**3, g**(-2)*v**4*h**2*l**4"
        # This corresponds to p1 = 3, p2 = 3, q1 = 2, q2 = 1
        response = "g*v**(-2)*h**3*l**2, g**2*v**(-4)*h**3*l"
        self.assertEqual_input_variations(response, answer, params, True)
        # This corresponds to p1 = 1, p2 = 2, q1 = 1, q2 = 2
        response = "h*l, h**2*l**2"
        self.assertEqual_input_variations(response, answer, params, False)
        # This does not correspond to any consistent values of p1, p2, q1 and q2
        response = "g**1*v**2*h**3*l**4, g**4*v**3*h**2*l**1"
        self.assertEqual_input_variations(response, answer, params, False)

    def test_buckingham_pi_two_groups_with_quantities(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": [['U',[]],['L',[]],['nu',[]],['f',[]]]}
        answer = "U*L/nu, f*L/U"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_buckingham_pi_two_groups_with_quantities_no_answer(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": [['U',[]],['L',[]],['nu',[]],['f',[]]]}
        answer = "-"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertEqual_input_variations(response, answer, params, True)
        response = "U*L/nu, f*L/U"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_buckingham_pi_two_groups_with_quantities_not_dimensionless(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": [['U',[]],['L',[]],['nu',[]],['f',[]]]}
        answer = "f*U*L/nu, f*L/U"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            params,
        )
        answer = "U*L/nu, f*L/U"
        response = "U*L/nu, U*nu/(f*L**2)"
        result = evaluation_function(response, answer, params)
        self.assertIn("feedback",result)

    def test_buckingham_pi_two_groups_with_quantities_too_few_independent_groups_in_answer(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": [['U',[]],['L',[]],['nu',[]],['f',[]]]}
        answer = "U*L/nu"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            params,
        )
        answer = "U*L/nu, (U*L/nu)**2"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            params,
        )

    def test_buckingham_pi_two_groups_with_quantities_too_few_independent_groups_in_response(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": [['U',[]],['L',[]],['nu',[]],['f',[]]]}
        answer = "U*L/nu, f*L/U"
        response = "U*L/nu, (U*L/nu)**2"
        self.assertEqual_input_variations(response, answer, params, False)

    def test_empty_input_symbols_codes_and_alternatives(self):
        answer = '10*gamma km/s'
        response = '10*gamma km/s'
        params = {'strict_syntax': False,
                   'input_symbols': [['gamma', ['']], ['', ['A']], [' ', ['B']], ['C', ['  ']]]
                 }
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], True)

    def test_warning_inappropriate_symbol(self):
        answer = '2**4'
        response = '2^4'
        params = {'strict_syntax': True }
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["feedback"], "Note that `^` cannot be used to denote exponentiation, use `**` instead.")

        answer = '2**4'
        response = '2^0.5'
        params = {'strict_syntax': True }
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["feedback"], parse_error_warning(response)+"\n"+"Note that `^` cannot be used to denote exponentiation, use `**` instead.")

    def test_empty_response_answer(self):
        with self.subTest(tag="Empty response"):
            answer = "5*x"
            response = ""
            result = evaluation_function(response, answer, {})
            self.assertEqual(result["feedback"], "No response submitted.")
        with self.subTest(tag="Whitespace response"):
            answer = "5*x"
            response = "  \t\n"
            result = evaluation_function(response, answer, {})
            self.assertEqual(result["feedback"], "No response submitted.")
        with self.subTest(tag="Whitespace answer"):
            answer = ""
            response = "5*x"
            self.assertRaises(
                Exception,
                evaluation_function,
                response,
                answer,
                {},
            )
        with self.subTest(tag="Whitespace answer"):
            answer = "  \t\n"
            response = "5*x"
            self.assertRaises(
                Exception,
                evaluation_function,
                response,
                answer,
                {},
            )

    def test_per(self):
        per_warning = "Note that 'per' was interpreted as '/'. This can cause ambiguities. It is recommended to use parentheses to make your entry unambiguous."
        with self.subTest(tag="Correct response with per"):
            answer = "50*kilometre/hour"
            response = "50 kilometres per hour"
            params = {"strict_syntax": False, "input_symbols": [["alpha",["A"]],["beta",["b"]],["gamma",["g"]]]}
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)
            self.assertEqual(per_warning in result["feedback"], True)

        with self.subTest(tag="Ambiguity in denominator"):
            answer = "50*kilometre/(hour*ampere)"
            response = "50 kilometres per hour ampere"
            params = {"strict_syntax": False, "input_symbols": [["alpha",["A"]],["beta",["b"]],["gamma",["g"]]]}
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)
            self.assertEqual(per_warning in result["feedback"], True)

        with self.subTest(tag="With 'per' in input symbol"):
            answer = "50*kilometre/hour"
            response = "50 kilometres per hour"
            params = {"strict_syntax": False, "input_symbols": [["per",["A"]],["beta",["b"]],["gamma",["g"]]]}
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)
            self.assertEqual(per_warning in result.get("feedback",""), False)

        with self.subTest(tag="With 'per' in input symbol alternative"):
            answer = "50*kilometre/hour"
            response = "50 kilometres per hour"
            params = {"strict_syntax": False, "input_symbols": [["A",["per"]],["beta",["b"]],["gamma",["g"]]]}
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)
            self.assertEqual(per_warning in result.get("feedback",""), False)

    def test_error_inappropriate_symbol(self):
        answer = '0.5'
        response = '0,5'
        params = {'strict_syntax': True }
        result = evaluation_function(response, answer, params)
        self.assertEqual(parse_error_warning(response) in result["feedback"], True)

        answer = '(0.002*6800*v)/1.2'
        response = '(0,002*6800*v)/1,2'
        params = {'strict_syntax': False }
        result = evaluation_function(response, answer, params)
        self.assertEqual(parse_error_warning(response) in result["feedback"], True)

        answer = '-inf'
        response = '-∞'
        params = {'strict_syntax': False }
        result = evaluation_function(response, answer, params)
        self.assertEqual(parse_error_warning(response) in result["feedback"], True)

        answer = 'x*y'
        response = 'x.y'
        params = {'strict_syntax': False }
        result = evaluation_function(response, answer, params)
        self.assertEqual(parse_error_warning(response) in result["feedback"], True)

    def test_fractional_powers_buckingham_pi(self):
        params = {"strict_syntax": False, "comparison": "buckinghamPi"}
        with self.subTest(tag="square root in answer"):
            answer = "f*(((m*l)/T)**0.5)"
            response = "f**2*((m*l)/T)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

        with self.subTest(tag="fractional power that can be written exactly as a decimal in answer"):
            answer = "f*(((m*l)/T)**0.25)"
            response = "f**4*((m*l)/T)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

        with self.subTest(tag="fractional power written as a fraction in answer"):
            answer = "f*(((m*l)/T)**(1/3))"
            response = "f**3*((m*l)/T)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

        with self.subTest(tag="fractional power that that is not an n:th root in answer"):
            answer = "f*(((m*l)/T)**(2/3))"
            response = "f**3*((m*l)/T)**2"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

    def test_sums_buckingham_pi(self):
        params = {"strict_syntax": False, "comparison": "buckinghamPi"}

        with self.subTest(tag="sum of valid dimensionless terms"):
            answer = "f*(((m*l)/T)**0.5)"
            response = "5*f**2*((m*l)/T)+sin(10)*f*((m*l)/T)**0.5+1"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

        with self.subTest(tag="sum that contains an invalid dimensionless terms"):
            answer = "f*(((m*l)/T)**0.5)"
            response = "f**2*((m*l)/T)+((m*l)/T)**0.5+1"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)

        params = {"strict_syntax": False,
                  "comparison": "buckinghamPi",
                  "quantities": "('F','(gram*metre*second**(-2))') ('U','(metre/second)') ('rho','(gram/(metre**3))') ('D','(metre)') ('omega','(second**(-1))')",
                  "input_symbols": [["F",[]],["U",[]],["rho",[]],["D",[]],["omega",[]]]}

        with self.subTest(tag="two groups, one is sum of valid terms"):
            answer = "-"
            response = "U/(omega*D),U/(omega*D)+F/(rho*D**4*omega**2)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], True)

        with self.subTest(tag="two groups, one has an invalid terms"):
            answer = "-"
            response = "U/(omega*D),U/(omega*D)+1/(rho*D**4*omega**2)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)

        with self.subTest(tag="a sum with two independent valid terms instead of two groups"):
            answer = "-"
            response = "U/(omega*D)+F/(rho*D**4*omega**2)"
            result = evaluation_function(response, answer, params)
            self.assertEqual(result["is_correct"], False)

    def test_MECH50010_set_5(self):
        # Dimensional homogeneity a)
        params = {"strict_syntax": False,
                  "comparison": "buckinghamPi"}
        answer = "f*(((m*l)/T)**0.5)"
        response = "f**2*((m*l)/T)"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], True)

        # Aircraft propeller a)
        params = {"strict_syntax": False,
                  "comparison": "buckinghamPi",
                  "quantities": "('F','(gram*metre*second**(-2))') ('U','(metre/second)') ('rho','(gram/(metre**3))') ('D','(metre)') ('omega','(second**(-1))')",
                  "input_symbols": [["F",[]],["U",[]],["rho",[]],["D",[]],["omega",[]]]}
        answer = "-"
        response = "U/(omega*D),F/(rho*D**4*omega**2)"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], True)

        response = "U/(omega*D),F/(rho*D**2*U**2)"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], True)

        response = "F/(rhoD^4omega^2)"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], False)

        # Comparing to actual solutions b)
        params = {'rtol': 0.05,
                  'strict_syntax': False,
                  'cases': [{'answer': '3.1415926', 'feedback': '', 'mark': 1, 'params': {}}],
                  'input_symbols': [['pi', ['Pi', 'PI', 'π']]]
                  }
        answer = "pi"
        response = "3.14"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result["is_correct"], True)

    def assertEqual_elementary_function_aliases(self,answer,response,params,value):
        with self.subTest(alias_tag="name"):
            result = evaluation_function(response, answer, params)
            print(result["response_latex"])
            self.assertEqual(result["is_correct"], value)
        names = []
        alias_substitutions = []
        for (name,alias) in elementary_functions_names:
            if name in answer or name in response:
                names.append(name)
                alias_substitutions += [(name,x) for x in alias]
        alias_substitutions.sort(key=lambda x: -len(x[0]))
        for substitution in alias_substitutions:
            with self.subTest(alias_tag=substitution):
                subs_answer = substitute(answer,alias_substitutions)
                subs_response = substitute(response,alias_substitutions)
                result = evaluation_function(subs_response, subs_answer, params)
                self.assertEqual(result["is_correct"], value)

    def test_AAA_elementary_functions(self):
        params = {"strict_syntax": False, "elementary_functions": True}
        with self.subTest(tag="sin"):
            answer = "0"
            response = "Bsin(pi)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sinc"):
            answer = "B"
            response = "Bsinc(0)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="csc"):
            answer = "B"
            response = "Bcsc(pi/2)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="cos"):
            answer = "0"
            response = "Bcos(pi/2)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sec"):
            answer = "B"
            response = "Bsec(0)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="tan"):
            answer = "B"
            response = "Btan(pi/4)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="cot"):
            answer = "B"
            response = "Bcot(pi/4)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="asin"):
            answer = "B*pi/2"
            response = "Basin(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="acsc"):
            answer = "B*pi/2"
            response = "Bacsc(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="acos"):
            answer = "0"
            response = "Bacos(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="asec"):
            answer = "0"
            response = "Basec(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="atan"):
            answer = "B*pi/4"
            response = "Batan(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="acot"):
            answer = "B*pi/4"
            response = "Bacot(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="atan2"):
            answer = "B*pi/4"
            response = "Batan2(1,1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sinh"):
            answer = "B*exp(x)"
            response = "Bsinh(x)+Bcosh(x)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="cosh"):
            answer = "B*cosh(-1)"
            response = "Bcosh(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="tanh"):
            answer = "B*tanh(2*x)"
            response = "B*2*tanh(x)/(1+tanh(x)^2)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="csch"):
            answer = "B/sinh(x)"
            response = "Bcsch(x)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sech"):
            answer = "B/cosh(x)"
            response = "Bsech(x)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="asinh"):
            answer = "B"
            response = "Basinh(sinh(1))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="acosh"):
            answer = "B"
            response = "Bacosh(cosh(1))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="atanh"):
            answer = "B"
            response = "Batanh(tanh(1))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="asech"):
            answer = "B"
            response = "Bsech(asech(1))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="exp"):
            answer = "B*exp(2*x)"
            response = "Bexp(x)*exp(x)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="exp2"):
            answer = "a+b*exp(2)"
            response = "a+b*E^2"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="log"):
            answer = "10B"
            response = "Bexp(log(10))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sqrt"):
            answer = "2B"
            response = "Bsqrt(4)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="sign"):
            answer = "B"
            response = "Bsign(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="Abs"):
            answer = "2B"
            response = "BAbs(-2)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="Max"):
            answer = "B"
            response = "BMax(0,1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="Min"):
            answer = "B"
            response = "BMin(1,2)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="arg"):
            answer = "0"
            response = "Barg(1)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="ceiling"):
            answer = "B"
            response = "Bceiling(0.6)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="floor"):
            answer = "0"
            response = "Bfloor(0.6)"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)
        with self.subTest(tag="MECH50001_7.2"):
            answer = "fs/(1-M*cos(theta))"
            response = "fs/(1-Mcos(theta))"
            self.assertEqual_elementary_function_aliases(answer,response,params,True)

if __name__ == "__main__":
    unittest.main()

