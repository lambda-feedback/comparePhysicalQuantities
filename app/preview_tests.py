import unittest

try:
    from .preview import Params, preview_function
except ImportError:
    from preview import Params, preview_function


class TestPreviewFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practice to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use preview_function() to check your algorithm works
    as it should.
    """

    def test_returns_preview_key(self):
        response, params = "test", Params()
        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])

    def test_returns_preview_key(self):
        response, params = "test", Params()
        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])

    def test_quantity_with_short_forms(self):
        params = {"strict_syntax": False}
        response = "2 km/h"
        result = preview_function(response, params)
        self.assertEqual(result["preview"]["latex"],"2 ~\\mathrm{kilo} ~\\mathrm{metre} ~\\mathrm{hour}^{-1}")

    def test_quantity_with_long_forms(self):
        params = {"strict_syntax": False}
        response = "2 kilometre/hour"
        result = preview_function(response, params)
        self.assertEqual(result["preview"]["latex"],"2 ~\\mathrm{kilo} ~\\mathrm{metre} ~\\mathrm{hour}^{-1}")

    def test_quantity_with_alternatives(self):
        params = {"strict_syntax": False}
        response = "2 megametres"
        result = preview_function(response, params)
        self.assertEqual(result["preview"]["latex"],"2 ~\\mathrm{mega} ~\\mathrm{metre}")

    def test_invalid_input(self):
        params = {"strict_syntax": False}
        response = "5+"
        result = preview_function(response, params)
        self.assertEqual(result["preview"]["latex"],"Failed to parse expression: `5+`")

    def test_buckingham_pi_two_groups(self):
        params = {"comparison": "buckinghamPi",
                  "quantities": "('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')",
                  "strict_syntax": False}
        response = "U*L/nu, (f*L)/U"
        result = preview_function(response, params)
        self.assertEqual(result["preview"]["latex"],"\\frac{L U}{\\nu},~\\frac{L f}{U}")

if __name__ == "__main__":
    unittest.main()
