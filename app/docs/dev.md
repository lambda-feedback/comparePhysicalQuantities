# ComparePhysicalQuantities

Evaluation function which proveds some basic some dimensional analysis functionality.

- **DEPRECATED** Comparing physical quantities **RECOMMENDED ALTERNATIVE:** CompareExpressions with the `physical_quantity` parameter set to `true`
- Substitutions of symbols before comparison of expressions is done
- Checking if a comma separated list of expressions can be interpreted as a set groups that satisfies the Buckingham Pi theorem

**Note:** When the `quantities` grading parameter is set, this function cannot handle short form symbols for units. Thus when defining quantities all units must be given with full names in lower-case letters. For example `Nm/s` or `Newton*metre/SECOND` will not be handled correctly, but `newton*metre/second` will.

**Note:** Prefixes have lower precedence than exponentiation, e.g. `10*cm**2` will be interpreted as $10 \cdot 10^{-2} \mathrm{metre}^2$ rather than $10 (10^(-2)\mathrm{metre})^2$.

**Note:** This function allows omitting `*` and using `^` instead of `**` if the grading parameter `strict_syntax` is set to false. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as input symbols.

**Note:** Only the short forms listed in the tables below are accepted. Not all units that are supported have short forms (since this leads to ambiguities).

**Note:** When using the short forms the following convention is assumed:
- Long form names takes precedence over sequences of short forms, e.g.  e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Short form symbols of prefixes will take precedence over short form symbols of units from the left, e.g. 
- If there is a short form symbol for a prefix that collides with the short form for a unit (i.e. `m`) then it is assumed the that unit will always be placed to the right of another unit in compound units, e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Longer short form symbols take precedence over shorter short forms, e.g. `sr` will be interpreted as `steradian` instead of `second radian`.

**Note:** setting `elementary_functions` to true will disable using short forms symbols for units.

**Note:** When running the unit test some tests are expected to take much longer than the other. These tests can be skipped by adding `skip_resource_intensive_tests` as a command line argument to improve iteration times.

## Changing default feedback messages

The feedback messages can be set on a per-task basis (see description of the `custom_feedback` input parameter).

The default feedback messages are defined in `feedback_responses_list` defined near the top of `evaulation.py`, which contains a list of dictionaries of feedback responses that are used througout the code. All feedback messages visible to learners are defined in these dictionaries. The entries in the dictionaries are either be string of functions that return strings.

## Inputs
All input parameters need to be supplied via the **Grading parameters** panel.

There are seven optional parameters that can be set: `elementary_functions`, `substitutions`, `quantities`, `strict_syntax`, `rtol`, `atol` and `comparison`.

## `custom_feedback`

Custom feedback can be set on a per-task basis. **Note:** Custom feedback only supports fixed strings, this means that for some situations the custom feedback cannot be as detailed as the default feedback.

The parameter must be set as a dictionary with keys from the feedback tags listed below. The value for each key can be any string.

### Feedback tags for all comparisons
- `PARSE_ERROR_WARNING` Response cannot be parsed as an expression or physical quantity.
- `PER_FOR_DIVISION` Warns about risk of ambiguity when using `per` instead `/` for division.
- `STRICT_SYNTAX_EXPONENTIATION` Warns that `^` cannot be used for exponentiation when `strict_syntax` is set to `true`.
- `QUANTITIES_NOT_WRITTEN_CORRECTLY` Text in error message that appears if list of quantities could not be parsed.
- `SUBSTITUTIONS_NOT_WRITTEN_CORRECTLY` Text in error message that appears if list of substitutions could not be parsed.

### Feedback tags for `buckinghamPi` comparison

- `VALID_CANDIDATE_SET` Message that is displayed when a response is found to be a valid set of groups. **Note:** setting this will not affect the Correct/Incorrect message, it will only add further text.
- `NOT_DIMENSIONLESS` Message displayed when at least one groups is not dimensionless.
- `MORE_GROUPS_THAN_REFERENCE_SET` Message displayed when the response contains more groups than necessary.
- `CANDIDATE_GROUPS_NOT_INDEPENDENT` Message displayed when the groups in the response are not independent.
- `TOO_FEW_INDEPENDENT_GROUPS` Message displayed when the response contains fewer groups than necessary.
- `UNKNOWN_SYMBOL` Message displayed when the response contains some undefined symbol.
- `SUM_WITH_INDEPENDENT_TERMS`  Message displayed when the response has too few groups but one (or more) of the groups is a sum with independent terms.

## `elementary_functions`

When using implicit multiplication function names with mulitple characters are sometimes split and not interpreted properly. Setting `elementary_functions` to true will reserve the function names listed below and prevent them from being split. If a name is said to have one or more alternatives this means that it will accept the alternative names but the reserved name is what will be shown in the preview.

`sin`, `sinc`, `csc` (alternative `cosec`), `cos`, `sec`, `tan`, `cot` (alternative `cotan`), `asin` (alternative `arcsin`), `acsc` (alternatives `arccsc`, `arccosec`), `acos` (alternative `arccos`), `asec` (alternative `arcsec`), `atan` (alternative `arctan`), `acot` (alternatives `arccot`, `arccotan`), `atan2` (alternative `arctan2`), `sinh`, `cosh`, `tanh`, `csch` (alternative `cosech`), `sech`, `asinh` (alternative `arcsinh`), `acosh` (alternative `arccosh`), `atanh` (alternative `arctanh`), `acsch` (alternatives `arccsch`, `arcosech`), `asech` (alternative `arcsech`), `exp` (alternative `Exp`), `E` (equivalent to `exp(1)`, alternative `e`), `log`, `sqrt`, `sign`, `Abs` (alternative `abs`), `Max` (alternative `max`), `Min` (alternative `min`), `arg`, `ceiling` (alternative `ceil`), `floor`

**Note:** setting `elementary_functions` to true will disable using short forms symbols for units.

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

| Unit name | Symbol | Expressed in base SI units                                                       |
|-----------|:-------|:---------------------------------------------------------------------------------|
| radian    |   r    | 1                                                                                |
| steradian |  sr    | 1                                                                                |
| hertz     |  Hz    | $\mathrm{second}^{-1}$                                                           |
| newton    |   N    | $\mathrm{metre}~\mathrm{kilogram}~\mathrm{second}^{-2}$                         |
| pascal    |  Pa    | $\mathrm{metre}^{-1}~\mathrm{kilogram}~\mathrm{second}^{-2}$                     |
| joule     |   J    | $\mathrm{metre}^2~\mathrm{kilogram~second}^{-2}$                                 |
| watt      |   W    | $\mathrm{metre}^2~\mathrm{kilogram~second}^{-3}$                                 |
| coulomb   |   C    | $\mathrm{second~ampere}$                                                         |
| volt      |   V    | $\mathrm{metre}^2~\mathrm{kilogram second}^{-3}~\mathrm{ampere}^{-1}$            |
| farad     |   F    | $\mathrm{metre}^{-2}~\mathrm{kilogram}^{-1}~\mathrm{second}^4~\mathrm{ampere}^2$ |
| ohm       |   O    | $\mathrm{metre}^2~\mathrm{kilogram second}^{-3}~\mathrm{ampere}^{-2}$            |
| siemens   |   S    | $\mathrm{metre}^{-2}~\mathrm{kilogram}^{-1}~\mathrm{second}^3~\mathrm{ampere}^2$ |
| weber     |  Wb    | $\mathrm{metre}^2~\mathrm{kilogram~second}^{-2}~\mathrm{ampere}^{-1}$            |
| tesla     |   T    | $\mathrm{kilogram~second}^{-2} \mathrm{ampere}^{-1}$                            |
| henry     |   H    | $\mathrm{metre}^2~\mathrm{kilogram~second}^{-2}~\mathrm{ampere}^{-2}$            |
| lumen     |  lm    | $\mathrm{candela}$                                                               |
| lux       |  lx    | $\mathrm{metre}^{-2}~\mathrm{candela}$                                            |
| becquerel |  Bq    | $\mathrm{second}^{-1}$                                                            |
| gray      |  Gy    | $\mathrm{metre}^2~\mathrm{second}^{-2}$                                          |
| sievert   |  Sv    | $\mathrm{metre}^2~\mathrm{second}^{-2}$                                          |
| katal     |  kat   | $\mathrm{mole~second}^{-1}$                                                      |

#### Table: Common non-SI units

Commonly used non-SI units taken from Table 6 and 7 of https://physics.nist.gov/cuu/Units/outside.html

Note that the function treats angles, neper and bel as dimensionless values.

Note that only the first table in this section has short form symbols defined, the second table does not.

| Unit name         | Symbol | Expressed in SI units                      |
|-------------------|:-------|:-------------------------------------------|
| minute            |  min   | $60~\mathrm{second}$                       |
| hour              |   h    | $3600~\mathrm{second}$                     |
| degree            |  deg   | $\frac{\pi}{180}$                          |
| liter             |   l    | $10^{-3}~\mathrm{metre}^3$                 |
| metric_ton        |   t    | $10^3~\mathrm{kilogram}$                   |
| neper             |  Np    | $1$                                        |
| bel               |   B    | $\frac{1}{2}~\ln(10)$                      |
| electronvolt      |  eV    | $1.60218 \cdot 10^{-19}~\mathrm{joule}$    |
| atomic_mass_unit  |   u    | $1.66054 \cdot 10^{-27}~\mathrm{kilogram}$ |
| angstrom          |   å    | $10^{-10}~\mathrm{metre}$                  |

| Unit name        | Expressed in SI units                                |
|------------------|:-----------------------------------------------------|
| day              | $86400~\mathrm{second}$                              |
| angleminute      | $\frac{\pi}{10800}$                                  |
| anglesecond      | $\frac{\pi}{648000}$                                 |
| astronomicalunit | $149597870700~\mathrm{metre}$                        |
| nauticalmile     | $1852~\mathrm{metre}$                                |
| knot             | $\frac{1852}{3600}~\mathrm{metre~second}^{-1}$       |
| are              | $10^2~\mathrm{metre}^2$                              |
| hectare          | $10^4~\mathrm{metre}^2$                              |
| bar              | $10^5~\mathrm{pascal}$                               |
| barn             | $10^{-28}~\mathrm{metre}$                            |
| curie            | $3.7 \cdot 10^{10}~\mathrm{becquerel}                |
| roentgen         | $2.58 \cdot 10^{-4}~\mathrm{kelvin~(kilogram)}^{-1}$ |
| rad              | $10^{-2}~\mathrm{gray}$                              |
| rem              | $10^{-2}~\mathrm{sievert}$                           |

#### Table: Imperial units

Commonly imperial units taken from https://en.wikipedia.org/wiki/Imperial_units

| Unit name         | Symbol | Expressed in SI units                         |
|-------------------|:-------|:----------------------------------------------|
| inch              |   in   | $0.0254~\mathrm{metre}$                       |
| foot              |   ft   | $0.3048~\mathrm{metre}$                       |
| yard              |   yd   | $0.9144~\mathrm{metre}$                       |
| mile              |   mi   | $1609.344~\mathrm{metre}$                     |
| fluid ounce       |  fl oz | $28.4130625~\mathrm{millilitre}$              |
| gill              |   gi   | $142.0653125~\mathrm{millilitre}$             |
| pint              |   pt   | $568.26125~\mathrm{millilitre}$               |
| quart             |   qt   | $1.1365225~\mathrm{litre}$                    |
| gallon            |   gal  | $4546.09~\mathrm{litre}$                      |
| ounce             |   oz   | $28.349523125~\mathrm{gram}$                  |
| pound             |   lb   | $0.45359237~\mathrm{kilogram}$                |
| stone             |   st   | $6.35029318~\mathrm{kilogram}$                |

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

For more details on each options see the description below and the corresponding examples.

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
- In the answer, provide an example set of groups as a comma seprated list. When used this way the function assumes that the given list is correct and contains at least the minimum number of groups.
- In the `quantities` parameter, supply a list of what the dimensions for each quantity is and set answer to `-`. The function will then compute a list of sufficiently many independen dimensionless quantities and compare to the response.
- In the `quantities` parameter, supply a list of what the dimensions for each quantity is and in the answer, supply a list of groups as in the first option. The function will then check that the supplied answer is dimensionless and has a sufficient number of independent groups before comparing it to the response.

Note that in lists of groups the items should ideally be written on the form $q_1^{c_1} \cdot q_2^{c_2} \cdots q_n^{c_n}$ where $q_1, q_2 \ldots q_n$ are quantities and $c_1, c_2 \ldots c_n$ are integers, but the function can also handle item that are sums with terms written on the form $a \cdot q_1^{c_1} \cdot q_2^{c_2} \cdots q_n^{c_n}$ where $q_1, q_2 \ldots q_n$ are quantities, $c_1, c_2 \ldots c_n$ rational numbers and $a$ a constant. If the total number of groups is less than required the set of groups is considered invalid, even if there is a sufficient number of terms with independent power products in the response.