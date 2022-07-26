# - comparePhysicalQuantities -
This is an **EXPERIMENTAL** evaluation function with some dimensional analysis functionality.

This function lacks nice GUI, can be quite brittle and will likely change significantly in the near future.

## Inputs
All input parameters need to be supplied via the **Grading parameters** panel.

### substitutions

String that lists all substitutions that should be done to the answer and response inputs before processing.

Each substitution should be written on the form `('original string','substitution string')` and all pairs concatenated into a single string. Substitutions can be grouped by adding `|` between two substitutions. Then all substitutions before `|` will be performed before the substitutions after `|`.

The input can contain an arbitrary number of substitutions and `|`.

Note that using substitutions will replace all default definitions of quantities and dimensions.

### `quantities`

String that lists all quantities that can be used in the answer and response.

Each quantity should be written on the form `('quantity name','(units)')` and all pairs concatenated into a single string. See tables below for available default units.

Whenever units are used they must be written exactly as in the left columns of tables given below (no short forms or single symbols) and units must be multiplied (or divided) with each other and quantities. 

If the `comparison` parameter is set `dimensions` it is not necessary to give exact units for each quantity but dimensions must be given instead. See tables below for available default dimensions.

If the `comparison` parameter is set `buckinghamPi` then `quantities` should be set in a different way. See the detailed description of `buckinghamPi` further down.

#### Table: Base SI units

SI base units taken from Table 1 https://physics.nist.gov/cuu/Units/units.html

Note that gram is used as a base unit instead of kilogram.

| SI base unit | Dimension name      |
|--------------|:--------------------|
| metre        | length              |
| gram         | mass                |
| second       | time                |
| ampere       | electric_current    |
| kelvin       | temperature         |
| mole         | amount_of_substance |
| candela      | luminous_intensity  |

#### Table: SI prefixes

SI base units taken from Table 5 https://physics.nist.gov/cuu/Units/prefixes.html

| SI Prefix | Factor     | | SI Prefix | Factor     |
|-----------|:-----------|-|-----------|:-----------|
| yotta     | $10^{24}$  | | deci      | $10^{-1}$  |
| zetta     | $10^{21}$  | | centi     | $10^{-2}$  |
| exa'      | $10^{18}$  | | milli     | $10^{-3}$  |
| peta      | $10^{15}$  | | micro     | $10^{-6}$  |
| tera      | $10^{12}$  | | nano      | $10^{-9}$  |
| giga      | $10^{9}$   | | pico      | $10^{-12}$ |
| mega      | $10^{6}$   | | femto     | $10^{-15}$ |
| kilo      | $10^{3}$   | | atto      | $10^{-18}$ |
| hecto     | $10^{2}$   | | zepto     | $10^{-21}$ |
| deka      | $10^{1}$   | | yocto     | $10^{-24}$ |

#### Table: Derived SI units

Derived SI units taken from Table 3 https://physics.nist.gov/cuu/Units/units.html

Note that degrees Celsius is omitted.

Note that the function treats radians and steradians as dimensionless values.

| Unit name | Expressed in base SI units                          |
|-----------|:----------------------------------------------------|
| radian    | 1                                                   |
| steradian | 1                                                   |
| hertz     | second$^{-1}$                                       |
| newton    | metre kilogram second                               |
| pascal    | metre$^{-1}$ kilogram second$^{-2}$                 |
| joule     | metre$^2$ kilogram second$^{-2}$                    |
| watt      | metre$^2$ kilogram second$^{-3}$                    |
| coulomb   | second ampere                                       |
| volt      | metre$^2$ kilogram second$^{-3}$ ampere$^{-1}$      |
| farad     | metre$^{-2}$ kilogram$^{-1}$ second$^4$ ampere$^2$  |
| ohm       | metre$^2$ kilogram second$^{-3}$ ampere$^{-2}$      |
| siemens   | metre$^{-2}$ kilogram$^{-1}$ second$^3$ ampere$^2$  |
| weber     | metre$^2$ kilogram second$^{-2}$ ampere$^{-1}$      |
| tesla     | kilo gram second$^{-2}$ ampere$^{-1}$               |
| henry     | metre$^2$ kilogram second$^{-2}$ ampere$^{-2}$      |
| lumen     | candela                                             |
| lux       | metre$^{-2}$ candela                                |
| becquerel | second$^{-1}$                                       |
| gray      | metre$^2$ second$^{-2}$                             |
| sievert   | metre$^2$ second$^{-2}$                             |
| katal     | mole second$^{-1}$                                  |

#### Table: Common non-SI units

Commonly used non-SI units taken from Table 6 and 7 https://physics.nist.gov/cuu/Units/outside.html

Note that the function treats angles, neper and bel as dimensionless values.

| Unit name         | Expressed in SI units                         |
|-------------------|:----------------------------------------------|
| min               | 60 second                                     |
| hour              | 3600 second                                   |
| day               | 86400 second                                  |
| angle_degree      | $\frac{\pi}{180}$                             |
| angle_minute      | $\frac{\pi}{10800}$                           |
| angle_second      | $\frac{\pi}{648000}$                          |
| liter             | $10^{-3}$ metre$^3$                           |
| metric_ton        | $10^3$ kilo gram                              |
| neper             | 1                                             |
| bel               | $\frac{1}{2} \ln(10)$                         |
| electronvolt      | $1.60218 \cdot 10^{-19}$ joule                |
| atomic_mass_unit  | $1.66054 \cdot 10^{-27}$ kilogram             |
| astronomical_unit | $149597870700$ metre                          |
| nautical_mile     | $1852$ metre                                  |
| knot              | $\frac{1852}{3600}$ metre second$^{-1}$       |
| are               | $10^2$ metre$^2$                              |
| hectare           | $10^4$ metre$^2$                              |
| bar               | $10^5$ pascal                                 |
| angstrom          | $10^{-10}$ metre                              |
| barn              | $10^{-28}$ metre                              |
| curie             | $3.7 \cdot 10^{10}$ becquerel                 |
| roentgen          | $2.58 \cdot 10^{-4}$ kelvin (kilogram)$^{-1}$ |
| rad               | $10^{-2}$ gray                                |
| rem               | $10^{-2}$ sievert                             |


### `rtol`

Maximum relative error allowed when comparing expressions.

### `atol`

Maximum absolute error allowed when comparing expressions.

### `comparison`

Parameter that determines what kind of comparison is done. There are four possible options:

 - `expression` Converts the expression to base SI units and checks that the units are the same and that the value of the answer and response is sufficienty close (as specified by the `atol` and `rtol` parameters).
 - `expressionExact` Converts the expression to base SI units and checks that the units are the same and that the value of the answer and response is identical to as high precision as possible.
 - `dimensions` Checks that the answer and response have the same dimensions, does not compare the values of the physical quantities.
 - `buckinghamPi` Checks that the set of quantities in the response matches the set of quantities in the sense given by the Buckingham Pi theorem.

For more details on each options see the description below and the correspondig examples.

If `comparison` is not specified it defaults to `expression`.

#### `expression`

Converts the expression to base SI units and checks that the units are the same and that the value of the answer and response is sufficienty close.

How big the difference between the value of the answer and the value of the response is decided by the `rtol` and `atol` parameters. If neither `atol` nor `rtol` is specified the function will allow a relative error of $10^{-12}$. If `atol` is specified its value will be interpreted as the maximum allowed absolute error. If `rtol` is specified its value will be interpreted as the maximum allowed relative error. If both `atol` and `rtol` the function will check both the absolute and relative error.

#### `expressionExact`

Converts the expression to base SI units and checks that the answer and response are identical to the highest precision possible (note that some unit conversions are not exact and that using decimal numbers in the answer or response limits this to floating point precision).

#### `dimensions`

Checks that the answer and response have the same dimensions, does not compare the values of the physical quantities.

With this option the quantities (specified by the `quantities` parameter) can be given either dimension only, or units.

#### `buckinghamPi`

Checks that the set of quantities in the response matches the set of quantities in the sense given by the Buckingham Pi theorem.

Note that when this options is chosen the `quantities` parameter should be set differently. It should be written as a list of products of quantities in python notation, see the example "Using the buckinghamPi comparison" below.

## Outputs
Outputs vary depending on chosen comparison options. This is likely to change in near future. Below is the minimum common set of outputs.
```json
{
  "command": "eval",
  "result": {
    "is_correct": "<bool>",
  }
}

```

## Examples

Implemented versions of these examples can be found in the module 'Examples: Evaluation Functions'.

### 1 Checking the dimensions of an expression or physical quantity

This example will check if the response has dimensions $\frac{\mathrm{length}^2}{\mathrm{time}^2}$.

#### a)
To check an expression there needs to be some predefined quantities that can be used in the expression. Since only dimensions will be checked units are not necessary (but could be used as well).

Here a response area with input type `TEXT` and two grading parameters, `quantities` and `comparison`, will be used.

`quantities` is defined as follows:
```
('d','(length)') ('t','(time)') ('v','(length/time)')
```

`comparison` is set to `dimensions`.

The answer is set two some expression with the right dimensions, e.g. `v**2`.

### b)
Checking the dimensions of a quantity directly, i.e. the dimensions of an expression of the form `number*units`, no predefined quantities are necessary.

Here a response area with input type `TEXT` and one grading parameter,`comparison`, will be used.

`comparison` is set to `dimensions`.

The answer is set two some expression with the right dimensions, e.g. `length**2/time**2`.