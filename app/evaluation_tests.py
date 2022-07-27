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

    def test_invalid_user_expression(self):
        body = {"response": "3x", "answer": "3*x"}

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

    def test_invalid_author_expression(self):
        body = {"response": "3*x", "answer": "3x"}

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
        body = {"response": "2*d**2/t**2+0.5*v**2", 
                "answer": "5*v**2", 
                "comparison": "dimensions", 
                "substitutions": "('d','(distance)') ('t','(time)') ('v','(distance/time)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_substitutions(self):
        body = {"response": "(d/t)**2/(3600**2)+v**2", 
                "answer": "2*v**2", 
                "substitutions": "('d','(km)') ('t','(s)') ('v','(km/h)') | ('k','1000*') ('h','(60*60*s)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_dimensions_with_defaults(self):
        body = {"response": "(d/t)**2*((1/3.6)**2)+v**2", 
                "answer": "2*v**2", 
                "comparison": "dimensions", 
                "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_defaults_simple(self):
        body = {"response": "2*v", 
                "answer": "2*(kilo*metre/hour)", 
                "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

    def test_compare_quantities_with_defaults(self):
        body = {"response": "(d/t)**2*((1/3.6)**2)+v**2", 
                "answer": "2*v**2", 
                "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_defaults_exact(self):
        response = "(d/t)**2*((1/3.6)**2)+v**2"
        answer = "2*v**2"
        params = {"comparison": "expressionExact", 
                  "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(response, answer, params)
        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_rtol(self):
        correct_results = []
        incorrect_results = []
        for k in [1,2,3]:
            # Checks that sufficiently accurate responses are considered correct
            response = "1"*(k+1)+"0"*(4-k)+"*deka*metre"
            answer = "111111*metre"
            params = {"rtol": "0."+"0"*k+"1"}
            result = evaluation_function(response, answer, params)
            correct_results.append(result.get("is_correct"))
            # Checks that insufficiently accurate responses are considered wrong
            response = "1"*k+"0"*(5-k)+"*metre"
            result = evaluation_function(response, answer, params)
            incorrect_results.append(result.get("is_correct"))

        self.assertEqual(all(correct_results) and not any(incorrect_results), True)

    def test_compare_quantities_with_atol(self):
        answer = "1.0*metre"
        response = "1.04*metre"
        params = {"atol": "0.05"}
        is_correct = bool(evaluation_function(response, answer, params).get("is_correct"))
        response = "0.96*metre"
        is_correct = bool(is_correct and evaluation_function(response, answer, params).get("is_correct"))
        response = "1.06*metre"
        is_correct = bool(is_correct and not evaluation_function(response, answer, params).get("is_correct"))
        response = "0.94*metre"
        is_correct = bool(is_correct and not evaluation_function(response, answer, params).get("is_correct"))

        self.assertEqual(is_correct, True)

    def test_compare_quantities_with_atol_and_rtol(self):
        answer = "1.0*kilo*metre"
        # Both absolute and relative error small enough
        response = "1098*metre"
        params = {"atol": "100", "rtol": "0.1"}
        is_correct = bool(evaluation_function(response, answer, params).get("is_correct"))
        # Both absolute and relative error too large
        response = "1102*metre"
        is_correct = bool(is_correct and not evaluation_function(response, answer, params).get("is_correct"))
        # Absolute error small enough and relative error too large
        response = "1098*metre"
        params = {"atol": "100", "rtol": "0.05"}
        is_correct = bool(is_correct and not evaluation_function(response, answer, params).get("is_correct"))
        # Absolute error too large and relative error small enough
        response = "1098*metre"
        params = {"atol": "50", "rtol": "0.1"}
        is_correct = bool(is_correct and not evaluation_function(response, answer, params).get("is_correct"))

        self.assertEqual(is_correct, True)

    def test_buckingham_pi_one_group(self):
        answer = "['U*L/nu']"
        params = {"comparison": "buckinghamPi"}
        correct_responses = ["['U*L/nu']",
                             "['L*U/nu']",
                             "['nu/U/L']",
                             "['(U*L/nu)**2']",
                             "['2*U*L/nu']"]
        incorrect_responses = ["['U*L/n/u']",
                               "['1']",
                               "['U*L*nu']",
                               "['A*U*L/nu']",
                               "['A']",
                               "['U/nu']",
                               "['U*L']"]
        is_correct = True
        for response in correct_responses:
            result = evaluation_function(response, answer, params)
            is_correct = result.get("is_correct") and is_correct
        for response in incorrect_responses:
            result = evaluation_function(response, answer, params)
            is_correct = (not result.get("is_correct")) and is_correct
        self.assertEqual(is_correct, True)

    def test_buckingham_pi_two_groups(self):
        # This corresponds to p1 = 1, p2 = 2, q1 = 3, q2 = 4
        answer = "['g**(-2)*v**4*h*l**3', 'g**(-2)*v**4*h**2*l**4']"
        # This corresponds to p1 = 3, p2 = 3, q1 = 2, q2 = 1
        response = "['g*v**(-2)*h**3*l**2', 'g**2*v**(-4)*h**3*l']"
        params = {"comparison": "buckinghamPi"}
        result = evaluation_function(response, answer, params)
        correct_response_is_correct = result.get("is_correct")
        # This corresponds to p1 = 1, p2 = 2, q1 = 1, q2 = 2
        response = "['h*l', 'h**2*l**2']"
        result = evaluation_function(response, answer, params)
        incorrect_response_is_incorrect = not result.get("is_correct")
        # This does not correspond to any consistent values of p1, p2, q1 and q2
        response = "['g**1*v**2*h**3*l**4', 'g**4*v**3*h**2*l**1']"
        result = evaluation_function(response, answer, params)
        incorrect_response_is_incorrect = (not result.get("is_correct")) and incorrect_response_is_incorrect
        self.assertEqual(correct_response_is_correct and incorrect_response_is_incorrect, True)

#REMARK: Test for version that uses sympy's unit system to check dimensions, this is not used in th code at the moment
#    def test_compare_dimensions_with_sympy_unit_system(self):
#        body = {"response": "2*d**2/t**2+0.5*v**2", "answer": "5*v**2", "comparison": "dimensions", "substitutions": "('d','(u.length)') ('t','(u.time)') ('v','(u.length/u.time)')"}
#
#        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})
#
#        self.assertEqual(response.get("is_correct"), True)

if __name__ == "__main__":
    unittest.main()
