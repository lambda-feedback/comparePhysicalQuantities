import unittest, sys

try:
    from .evaluation import evaluation_function
    from .static_unit_conversion_arrays import list_of_SI_prefixes, list_of_SI_base_unit_dimensions, list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI
except ImportError:
    from evaluation import evaluation_function
    from static_unit_conversion_arrays import list_of_SI_prefixes, list_of_SI_base_unit_dimensions, list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI

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

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

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
            f = open("symbols_log.txt","w")
            f.write("Incorrect:\n"+"".join([str(x)+"\n" for x in incorrect])+"\nErrors:\n"+"".join([str(x)+"\n" for x in errors])+"\nDoes not match convention:\n"+"".join([str(x)+"\n" for x in does_not_match_convention]))
            f.close()
            print(f"{len(incorrect)}/{k} {len(errors)}/{k} {(len(errors)+len(incorrect))/k} {len(does_not_match_convention)}/{k+len(does_not_match_convention)} {len(does_not_match_convention)/(k+len(does_not_match_convention))}")
        self.assertEqual(len(errors)+len(incorrect), 0)

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

if __name__ == "__main__":
    unittest.main()
