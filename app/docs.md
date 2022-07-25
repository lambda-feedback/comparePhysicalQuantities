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
Note that gram is used as a base unit instead of kilogram.

| SI base unit | Dimension name      |
|--------------|:--------------------|
| yotta        | 10e24               |
| zetta        | 10e21               |
| exa'         | 10e18               |
| peta         | 10e15               |
| tera         | 10e12               |
| giga         | 10e9                |
| mega         | 10e6                |
| kilo         | 10e3                |
| hecto        | 10e2                |
| deka         | 10e1                |
| deci         | 10e-1               |
| centi        | 10e-2               |
| milli        | 10e-3               |
| micro        | 10e-6               |
| nano         | 10e-9               |
| pico         | 10e-12              |
| femto        | 10e-15              |
| atto         | 10e-18              |
| zepto        | 10e-21              |
| yocto        | 10e-24              |

#### Table: Derived SI units

Derived SI units taken from Table 3 https://physics.nist.gov/cuu/Units/units.html
Note that degrees Celsius is omitted.

| Unit name | Expressed in base SI units                                                       |
|-----------|:---------------------------------------------------------------------------------|
| radian    | 1                                                                                |
| steradian | 1                                                                                |
| hertz     | $\text{second}^{-1}$                                                             |
| newton    | $\text{metre}~\text{kilo}~\text{gram}~\text{second}$                             |
| pascal    | $\text{metre}^{-1}~\text{kilogram}~\text{second}^{-2}$                           |
| joule     | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-2}$                      |
| watt      | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-3}$                      |
| coulomb   | $\text{second}~\text{ampere}$                                                    |
| volt      | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-3}~\text{ampere}^{-1}$   |
| farad     | $\text{metre}^{-2}~\text{kilogram}^{-1}~\text{second}^4~\text{ampere}^2$         |
| ohm       | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-3}~\text{ampere}^{-2}$   |
| siemens   | $\text{metre}^{-2}~\text{kilo}~\text{gram}^{-1}~\text{second}^3~\text{ampere}^2$ |
| weber     | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-2}~\text{ampere}^{-1}$   |
| tesla     | $\text{kilo}~\text{gram}~\text{second}^{-2}~\text{ampere}^{-1}$                  |
| henry     | $\text{metre}^2~\text{kilo}~\text{gram}~\text{second}^{-2}~\text{ampere}^{-2}$   |
| lumen     | $\text{candela}$                                                                 |
| lux       | $\text{metre}^{-2}~\text{candela}$                                               |
| becquerel | $\text{second}^{-1}$                                                             |
| gray      | $\text{metre}^2~\text{second}^{-2}$                                              |
| sievert   | $\text{metre}^2~\text{second}^{-2}$                                              |
| katal     | $\text{mole}~\text{second}^{-1}$                                                  |

### comparison

Parameter that determines what kind of comparison is done.

#### expression

Convert the expression to base SI units and checks that the units are the same and that the value of the answer and response have a relative error smaller that the rtol parameter.

#### expressionExact

Convert the expression to base SI units and checks that the answer and response are identical to the highest precision allowed (note that some unit conversions are not exact and that using decimal numbers in the answer or response limits this to floating point precision).

#### dimensions

Checks that the answer and response have the same dimensions, does not compare the values.

### rtol

Maximum relative error allowed when comparing expressions.

## Outputs
TODO

## Examples
TODO