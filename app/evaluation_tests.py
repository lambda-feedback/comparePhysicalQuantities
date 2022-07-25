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
        body = {"response": "ab", "answer": "c", "substitutions": "('a','A') ('b','B') ('c','AB')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_substitutions_replace_common_substrings_in_replacement(self):
        body = {"response": "ab", "answer": "c", "substitutions": "('a','b') ('b','d') ('c','bd')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_substitutions_replace_common_substrings_in_original(self):
        body = {"response": "ab", "answer": "c", "substitutions": "('a','d') ('ab','e') ('c','e')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_dimensions_with_substitution(self):
        body = {"response": "2*d**2/t**2+0.5*v**2", "answer": "5*v**2", "comparison": "dimensions", "substitutions": "('d','(distance)') ('t','(time)') ('v','(distance/time)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_substitutions(self):
        body = {"response": "(d/t)**2/(3600**2)+v**2", "answer": "2*v**2", "substitutions": "('d','(km)') ('t','(s)') ('v','(km/h)') | ('k','1000*') ('h','(60*60*s)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_dimensions_with_defaults(self):
        body = {"response": "(d/t)**2*((1/3.6)**2)+v**2", "answer": "2*v**2", "comparison": "dimensions", "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_defaults(self):
        body = {"response": "(d/t)**2*((1/3.6)**2)+v**2", "answer": "2*v**2", "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_defaults_exact(self):
        body = {"response": "(d/t)**2*((1/3.6)**2)+v**2", "answer": "2*v**2", "comparison": "expressionExact", "quantities": "('d','(metre)') ('t','(second)') ('v','(kilo*metre/hour)')"}

        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})

        self.assertEqual(response.get("is_correct"), True)

    def test_compare_quantities_with_rtol(self):
        correct_results = []
        incorrect_results = []
        for k in [1,2,3]:
            # Checks that sufficiently accurate responses are considered correct
            body = {"response": "1"*(k+1)+"0"*(4-k)+"*deka*metre", "answer": "111111*metre", "rtol": "0."+"0"*k+"1"}
            response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})
            correct_results.append(response.get("is_correct"))
            # Checks that insufficiently accurate responses are considered wrong
            body["response"] = "1"*k+"0"*(5-k)+"*metre"
            response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})
            incorrect_results.append(response.get("is_correct"))

        self.assertEqual(all(correct_results) and not any(incorrect_results), True)

#REMARK: Test for version that uses sympy's unit system to check dimensions, this is not used in th code at the moment
#    def test_compare_dimensions_with_sympy_unit_system(self):
#        body = {"response": "2*d**2/t**2+0.5*v**2", "answer": "5*v**2", "comparison": "dimensions", "substitutions": "('d','(u.length)') ('t','(u.time)') ('v','(u.length/u.time)')"}
#
#        response = evaluation_function(body["response"], body["answer"], {k:v for k,v in body.items() if k not in ["response","answer"]})
#
#        self.assertEqual(response.get("is_correct"), True)

if __name__ == "__main__":
    unittest.main()
