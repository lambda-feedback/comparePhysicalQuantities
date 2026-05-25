# comparePhysicalQuantities (Deprecated)

> **Deprecated:** This evaluation function is no longer maintained. It has been superseded by [compareExpressions](https://github.com/lambda-feedback/compareExpressions), which provides equivalent functionality with broader support. Please migrate to `compareExpressions`.

This evaluation function compares physical quantities submitted by students against a reference answer, handling unit conversions and symbolic expressions.

## Table of Contents
- [comparePhysicalQuantities (Deprecated)](#comparephysicalquantities-deprecated)
  - [Table of Contents](#table-of-contents)
  - [Repository Structure](#repository-structure)
  - [How it works](#how-it-works)
    - [Docker & Amazon Web Services (AWS)](#docker--amazon-web-services-aws)
    - [Middleware Functions](#middleware-functions)
    - [GitHub Actions](#github-actions)

## Repository Structure

```
app/
    __init__.py
    evaluation.py              # Main evaluation function
    evaluation_test.py         # Unit tests
    preview.py                 # Preview function
    preview_test.py            # Preview tests
    expression_utilities.py    # Expression parsing utilities
    unit_system_conversions.py # Unit conversion logic
    static_unit_conversion_arrays.py  # Pre-generated conversion data
    generate_unit_conversion_arrays.py  # Script to regenerate conversion data
    requirements.txt           # Python dependencies
    Dockerfile                 # Image definition for AWS deployment
    docs/
        user.md                # End-user documentation
        dev.md                 # Developer documentation

.github/
    workflows/
        test-lint.yml           # Run tests and linting on PRs
        pre_production_tests.yml
        staging-deploy.yml      # Deploy to staging
        production-deploy.yml   # Deploy to production

config.json   # Evaluation function name
```

## How it works

The function is built on top of a custom base layer, [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer), which provides tooling, tests, and schema checking common to all evaluation functions.

### Docker & Amazon Web Services (AWS)

The function is hosted on AWS Lambda using a Docker container image. For more information on Docker, see this [introduction to containerisation](https://www.freecodecamp.org/news/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b/). To learn more about AWS Lambda, click [here](https://geekflare.com/aws-lambda-for-beginners/).

### Middleware Functions

Middleware provided by [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer) handles request validation, routing, and response formatting.

### GitHub Actions

Commits trigger the GitHub Actions pipelines in `.github/workflows/`, which run tests and linting before building and deploying the Docker image to AWS.