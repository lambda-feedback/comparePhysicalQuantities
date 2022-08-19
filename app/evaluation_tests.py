import unittest

try:
    from .evaluation import evaluation_function
except ImportError:
    from evaluation import evaluation_function


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
        result = evaluation_function(response, answer, params)
        variation_definitions = [lambda x : x.replace('**','^'),
                                 lambda x : x.replace('**','^').replace('*',' '),
                                 lambda x : x.replace('**','^').replace('*','')]
        for variation in variation_definitions:
            response_variation = variation(response)
            answer_variation = variation(answer)
            self.assertEqual(result.get("is_correct"), value)
            if (response_variation != response) or (answer_variation != answer):
                result = evaluation_function(response_variation, answer, params)
                self.assertEqual(result.get("is_correct"), value)
                result = evaluation_function(response, answer_variation, params)
                self.assertEqual(result.get("is_correct"), value)
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
                   "input_symbols": ['distance','time'],
                   "strict_syntax": False}

        self.assertEqual_input_variations(response, answer, params, True)

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
        params = {"substitutions": substitutions, "strict_syntax": False,
                  "input_symbols": ['mPa','Pa','da','mu','mg','mm','mW','mN','ms']}
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
                  "input_symbols": ['GBP','EUR','USD','CNY','INR'],
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
                  "input_symbols": ['GBP','EUR','USD','CNY','INR'],
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

    def test_compare_quantities_with_rtol(self):
        correct_results = []
        incorrect_results = []
        for k in [1,2,3]:
            # Checks that sufficiently accurate responses are considered correct
            response = "1"*(k+1)+"0"*(4-k)+"*deka*metre"
            answer = "111111*metre"
            params = {"rtol": "0."+"0"*k+"1", "strict_syntax": False}
            self.assertEqual_input_variations(response, answer, params, True)
            # Checks that insufficiently accurate responses are considered wrong
            response = "1"*k+"0"*(5-k)+"*metre"
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

    def test_buckingham_pi_one_group(self):
        answer = "U*L/nu"
        params = {"comparison": "buckinghamPi", "input_symbols": ['U','L','nu'], "strict_syntax": False}
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
        is_correct = True
        for response in correct_responses:
            self.assertEqual_input_variations(response, answer, params, True)
        for response in incorrect_responses:
            self.assertEqual_input_variations(response, answer, params, False)

    def test_buckingham_pi_two_groups(self):
        params = {"comparison": "buckinghamPi", "strict_syntax": False,
                  "input_symbols": ['g','v','h','l']}
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
                  "input_symbols": ['U','L','nu','f']}
        answer = "U*L/nu, f*L/U"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_buckingham_pi_two_groups_with_quantities_no_answer(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": ['U','L','nu','f']}
        answer = "-"
        response = "U*L/nu, nu/(f*L**2)"
        self.assertEqual_input_variations(response, answer, params, True)

    def test_buckingham_pi_two_groups_with_quantities_not_dimensionless(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": ['U','L','nu','f']}
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
        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            params,
        )

    def test_buckingham_pi_two_groups_with_quantities_too_few_independent_groups_in_answer(self):
        params = {"comparison": "buckinghamPi",
                  "strict_syntax": False,
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "input_symbols": ['U','L','nu','f']}
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
                  "input_symbols": ['U','L','nu','f']}
        answer = "U*L/nu, f*L/U"
        response = "U*L/nu, (U*L/nu)**2"
        self.assertEqual_input_variations(response, answer, params, False)

#REMARK: Test for version that uses sympy's unit system to check dimensions, this is not used in the code at the moment
#    def test_compare_dimensions_with_sympy_unit_system(self):
#        body = {"response": "2*d**2/t**2+0.5*v**2", "answer": "5*v**2", "comparison": "dimensions", "substitutions": "('d','(u.length)') ('t','(u.time)') ('v','(u.length/u.time)')"}
#
#        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})
#
#        self.assertEqual(response.get("is_correct"), True)

if __name__ == "__main__":
    unittest.main()
