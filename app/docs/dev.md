# ComparePhysicalQuantities
This is an **EXPERIMENTAL** evaluation function with some dimensional analysis functionality.

This function lacks a nice GUI, can be quite brittle, and will likely change significantly in the near future.

**Note:** When the `quantities` grading parameter is set, this function cannot handle short form symbols for units. Thus when defining quantities all units must be given with full names in lower-case letters. For example `Nm/s` or `Newton*metre/SECOND` will not be handled correctly, but `newton*metre/second` will.

**Note:** Prefixes have lower precedence than exponentiation, e.g. `10*cm**2` will be interpreted as $10 \cdot 10^{-2} \mathrm{metre}^2$ rather than $10 (10^(-2)\mathrm{metre})^2$.

**Note:** This function allows omitting `*` and using `^` instead of `**` if the grading parameter `strict_syntax` is set to false. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as input symbols.

**Note:** Only the short forms listed in the tables below are accepted. Not all units that are supported have short forms (since this leads to ambiguities).

**Note:** When using the short forms the following convention is assumed:
- Long form names takes precedence over sequences of short forms, e.g.  e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Short form symbols of prefixes will take precedence over short form symbols of units from the left, e.g. 
- If there is a short form symbol for a prefix that collides with the short form for a unit (i.e. `m`) then it is assumed the that unit will always be placed to the right of another unit in compound units, e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Longer short form symbols take precedence over shorter short forms, e.g. `sr` will be interpreted as `steradian` instead of `second radian`.

**Note:** Only the short forms listed in the tables below are accepted. This means some common practices, such as writing `h` for hour will not be handled correctly.

**Note:** When running the unit test some tests are expected to take much longer than the other. These tests can be skipped by adding `skip_resource_intensive_tests` as a command line argument to improve iteration times.

## Inputs
All input parameters need to be supplied via the **Grading parameters** panel.

There are six optional parameters that can be set: `substitutions`, `quantities`, `strict_syntax`, `rtol`, `atol` and `comparison`.

### `substitutions`

String that lists all substitutions that should be done to the answer and response inputs before processing.

Each substitution should be written in the form `('original string','substitution string')` and all pairs concatenated into a single string. Substitutions can be grouped by adding `|` between two substitutions. Then all substitutions before `|` will be performed before the substitutions after `|`.

The input can contain an arbitrary number of substitutions and `|` symbols.

Note that using substitutions will replace all default definitions of quantities and dimensions.

### `quantities`

String that lists all quantities that can be used in the answer and response.

Each quantity should be written in the form `('quantity name','(units)')` and all pairs concatenated into a single string. See tables below for available default units.

Whenever units are used they must be written exactly as in the left columns of the tables given below (no short forms or single-character symbols) and units must be multiplied (or divided) by each other, as well as any accompanying quantities. 

**NOTE:** Using units and predefined quantities at the same time in an answer or response can cause problems (especially if quantities are denoted using single characters). Ideally it should be clear that either predefined quantities, or units should only be used from the question.

If the `comparison` parameter is set to `dimensions`, it is not necessary to give exact units for each quantity, but the dimensions must be given instead. See tables below for available default dimensions.

If the `comparison` parameter is set to `buckinghamPi`, then `quantities` should be set in a different way. See the detailed description of `buckinghamPi` further down.

#### Table: Base SI units

These tables list the units defined in `unit_system_conversions.py`. Note that the evaluation function uses static version of these arrays created by running `generate_unit_conversion_arrays.py` and stored in `static_unit_conversion_arrays.py`.

SI base units taken from Table 1 of https://physics.nist.gov/cuu/Units/units.html

Note that gram is used as a base unit instead of kilogram.

| SI base unit | Symbol | Dimension name      |
|--------------|:-------|:--------------------|
| metre        |   m    | length              |
| gram         |   g    | mass                |
| second       |   s    | time                |
| ampere       |   A    | electriccurrent     |
| kelvin       |   k    | temperature         |
| mole         |  mol   | amountofsubstance   |
| candela      |  cd    | luminousintensity   |

#### Table: SI prefixes

SI base units taken from Table 5 of https://physics.nist.gov/cuu/Units/prefixes.html

| SI Prefix | Symbol | Factor     | | SI Prefix | Symbol | Factor     |
|-----------|:-------|:-----------|-|-----------|:-------|:-----------|
| yotta     |   Y    | $10^{24}$  | | deci      |   d    | $10^{-1}$  |
| zetta     |   Z    | $10^{21}$  | | centi     |   c    | $10^{-2}$  |
| exa'      |   E    | $10^{18}$  | | milli     |   m    | $10^{-3}$  |
| peta      |   P    | $10^{15}$  | | micro     |   mu   | $10^{-6}$  |
| tera      |   T    | $10^{12}$  | | nano      |   n    | $10^{-9}$  |
| giga      |   G    | $10^{9}$   | | pico      |   p    | $10^{-12}$ |
| mega      |   M    | $10^{6}$   | | femto     |   f    | $10^{-15}$ |
| kilo      |   k    | $10^{3}$   | | atto      |   a    | $10^{-18}$ |
| hecto     |   h    | $10^{2}$   | | zepto     |   z    | $10^{-21}$ |
| deka      |   da   | $10^{1}$   | | yocto     |   y    | $10^{-24}$ |

#### Table: Derived SI units

Derived SI units taken from Table 3 of https://physics.nist.gov/cuu/Units/units.html

Note that degrees Celsius is omitted.

Note that the function treats radians and steradians as dimensionless values.

| Unit name | Symbol | Expressed in base SI units                          |
|-----------|:-------|:----------------------------------------------------|
| radian    |   r    | 1                                                   |
| steradian |  sr    | 1                                                   |
| hertz     |  Hz    | second$^{-1}$                                       |
| newton    |   N    | metre kilogram second$^{-2}$                        |
| pascal    |  Pa    | metre$^{-1}$ kilogram second$^{-2}$                 |
| joule     |   J    | metre$^2$ kilogram second$^{-2}$                    |
| watt      |   W    | metre$^2$ kilogram second$^{-3}$                    |
| coulomb   |   C    | second ampere                                       |
| volt      |   V    | metre$^2$ kilogram second$^{-3}$ ampere$^{-1}$      |
| farad     |   F    | metre$^{-2}$ kilogram$^{-1}$ second$^4$ ampere$^2$  |
| ohm       |   O    | metre$^2$ kilogram second$^{-3}$ ampere$^{-2}$      |
| siemens   |   S    | metre$^{-2}$ kilogram$^{-1}$ second$^3$ ampere$^2$  |
| weber     |  Wb    | metre$^2$ kilogram second$^{-2}$ ampere$^{-1}$      |
| tesla     |   T    | kilo gram second$^{-2}$ ampere$^{-1}$               |
| henry     |   H    | metre$^2$ kilogram second$^{-2}$ ampere$^{-2}$      |
| lumen     |  lm    | candela                                             |
| lux       |  lx    | metre$^{-2}$ candela                                |
| becquerel |  Bq    | second$^{-1}$                                       |
| gray      |  Gy    | metre$^2$ second$^{-2}$                             |
| sievert   |  Sv    | metre$^2$ second$^{-2}$                             |
| katal     |  kat   | mole second$^{-1}$                                  |

#### Table: Common non-SI units

Commonly used non-SI units taken from Table 6 and 7 of https://physics.nist.gov/cuu/Units/outside.html

Note that the function treats angles, neper and bel as dimensionless values.

Note that only the first table in this section has short form symbols defined, the second table does not.

| Unit name         | Symbol | Expressed in SI units                         |
|-------------------|:-------|:----------------------------------------------|
| minute            |  min   | 60 second                                     |
| hour              |   h    | 3600 second                                   |
| degree            |  deg   | $\frac{\pi}{180}$                             |
| liter             |   l    | $10^{-3}$ metre$^3$                           |
| metric_ton        |   t    | $10^3$ kilo gram                              |
| neper             |  Np    | 1                                             |
| bel               |   B    | $\frac{1}{2} \ln(10)$                         |
| electronvolt      |  eV    | $1.60218 \cdot 10^{-19}$ joule                |
| atomic_mass_unit  |   u    | $1.66054 \cdot 10^{-27}$ kilogram             |
| angstrom          |   å    | $10^{-10}$ metre                              |

| Unit name        | Expressed in SI units                         |
|------------------|:----------------------------------------------|
| day              | $86400$ second                                |
| angleminute      | $\frac{pi}{10800}$                            |
| anglesecond      | $\frac{pi}{648000}$                           |
| astronomicalunit | $149597870700$ metre                          |
| nauticalmile     | $1852$ metre                                  |
| knot             | $\frac{1852}{3600}$ metre second$^{-1}$       |
| are              | $10^2$ metre$^2$                              |
| hectare          | $10^4$ metre$^2$                              |
| bar              | $10^5$ pascal                                 |
| barn             | $10^{-28}$ metre                              |
| curie            | $3.7 \cdot 10^{10}$ becquerel                 |
| roentgen         | $2.58 \cdot 10^{-4}$ kelvin (kilogram)$^{-1}$ |
| rad              | $10^{-2}$ gray                                |
| rem              | $10^{-2}$ sievert                             |

### `strict_syntax`

If `strict_syntax` is set to true then the answer and response must have `*` or `/` between each part of the expressions and exponentiation must be done using `**`, e.g. `10*kilo*metre/second**2` is accepted but `10 kilometre/second^2` is not.

If `strict_syntax` is set to false, then `*` can be omitted and `^` used instead of `**`. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as input symbols.

By default `strict_syntax` is set to true.

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

How big the difference is between the value of the answer and the value of the response is decided by the `rtol` and `atol` parameters. If neither `atol` nor `rtol` is specified the function will allow a relative error of $10^{-12}$. If `atol` is specified its value will be interpreted as the maximum allowed absolute error. If `rtol` is specified its value will be interpreted as the maximum allowed relative error. If both `atol` and `rtol` the function will check both the absolute and relative error.

#### `expressionExact`

Converts the expression to base SI units and checks that the answer and response are identical to the highest precision possible (note that some unit conversions are not exact and that using decimal numbers in the answer or response limits this to floating point precision).

#### `dimensions`

Checks that the answer and response have the same dimensions, but does not compare the values of the physical quantities.

With this option the quantities (specified by the `quantities` parameter) can be given either dimension only, or units.

#### `buckinghamPi`

Checks that the set of quantities in the response matches the set of quantities in the sense given by the Buckingham Pi theorem.

There are three different ways of supplying this function with the necessary information.
- In the answer, supply a list of groups on the form `['` first group `','` second group `','` ... `','` last group `']`. Note that if there is only one group it still needs to be written as a list `['` group `']`. When used this way the function assumes that the given list is correct and contains at least the minimum number of groups.
- In the `quantities` parameter, supply a list of what the dimensions for each quantity is and set answer to `-`. The function will then compute a list of sufficiently many independen dimensionless quantities and compare to the response.
- In the `quantities` parameter, supply a list of what the dimensions for each quantity is and in the answer, supply a list of groups as in the first option. The function will then check that the supplied answer is dimensionless and has a sufficient number of independent groups before comparing it to the response.

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