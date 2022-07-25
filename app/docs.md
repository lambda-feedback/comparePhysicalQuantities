# - comparePhysicalQuantities -
This is an experimental evaluation function with some dimensional analysis functionality.

## Inputs
All input parameters need to be supplied via the 'Advanced - raw parameters' panel.

### substitutions

String that lists all substitutions that should be done to the answer and response inputs before processing.

Each substitution should be written on the form "('original string','substitution string')" and all pairs concatenated into a single string. Substitutions can be grouped by adding "|" between two substitutions. Then all substitutions before "|" will be performed before the substitutions after "|".

The input can contain an arbitrary number of substitutions and "|".

Note that using substitutions will replace all default definitions of quantities and dimensions.

### quantities

String that lists all quantities that can be used in the answer and response.

Each quantity should be written on the form "('quantity name','(units)')" and all pairs concatenated into a single string. See tables below for available default units.

If the "comparison" parameter is set "dimensions" it is not necessary to give exact units for each quantity but dimensions must be given instead. See tables below for available default units.

Whenever units are used they must be written exactly as in the table below and units must be multiplied (or divided) with each other and quantities. 

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
| curie             | $3.7 \cdot 10^10$ becquerel                   |
| roentgen          | $2.58 \cdot 10^{-4}$ kelvin (kilogram)$^{-1}$ |
| rad               | $10^{-2}$ gray                                |
| rem               | $10^{-2}$ sievert                             |


### rtol

Maximum relative error allowed when comparing expressions.

### comparison

Parameter that determines what kind of comparison is done.

#### expression

Convert the expression to base SI units and checks that the units are the same and that the value of the answer and response have a relative error smaller that the rtol parameter.

#### expressionExact

Convert the expression to base SI units and checks that the answer and response are identical to the highest precision allowed (note that some unit conversions are not exact and that using decimal numbers in the answer or response limits this to floating point precision).

#### dimensions

Checks that the answer and response have the same dimensions, does not compare the values of the physical quantities.

## Outputs
TODO

## Examples
TODO