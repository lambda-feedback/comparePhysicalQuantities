# ComparePhysicalQuantities
This is an **EXPERIMENTAL** evaluation function with some dimensional analysis functionality.

This function lacks a nice GUI, can be quite brittle, and will likely change significantly in the near future.

**Note:** When the `quantities` grading parameter is set, this function cannot handle short form symbols for units. Thus when defining quantities all units must be given with full names in lower-case letters. For example `Nm/s` or `Newton*metre/SECOND` will not be handled correctly, but `newton*metre/second` will.

**Note:** Prefixes have lower precedence than exponentiation, e.g. `10*cm**2` will be interpreted as $10 \cdot 10^{-2}~\mathrm{metre}^2$ rather than $10 \cdot (10^{-2}~\mathrm{metre})^2$.

**Note:** This function allows omitting `*` and using `^` instead of `**` if the grading parameter `strict_syntax` is set to false. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as input symbols.

**Note:** Only the short forms listed in the tables below are accepted. Not all units that are supported have short forms (since this leads to ambiguities).

**Note:** When using the short forms the following convention is assumed:
- Long form names takes precedence over sequences of short forms, e.g.  e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Short form symbols of prefixes will take precedence over short form symbols of units from the left, e.g. `mug` will be interpreted as `micro*gram` instead `metre*astronomicalunit*gram`.
- If there is a short form symbol for a prefix that collides with the short form for a unit (i.e. `m`) then it is assumed the that unit will always be placed to the right of another unit in compound units, e.g. `mN` will be interpreted as `milli newton`, `Nm` as `newton metre`, `mmN` as `milli metre newton`, `mNm` as `milli newton metre` and `Nmm` as `newton milli metre`.
- Longer short form symbols take precedence over shorter short forms, e.g. `sr` will be interpreted as `steradian` instead of `second radian`.

**Note:** Only the short forms listed in the tables below are accepted.

## Inputs
All input parameters need to be supplied via the **Grading parameters** panel.

There are six optional parameters that can be set: `substitutions`, `quantities`, `strict_syntax`, `rtol`, `atol` and `comparison`.

## `elementary_functions`

When using implicit multiplication function names with mulitple characters are sometimes split and not interpreted properly. Setting `elementary_functions` to True will reserve the function names listed below and prevent them from being split:

`sin`, `sinc`, `csc`, `cos`, `sec`, `tan`, `cot`, `asin`, `acsc`, `acos`, `asec`, `atan`, `acot`, `atan2`,`sinh`, `cosh`, `tanh`, `csch`, `sech`, `asinh`, `acosh`, `atanh`, `acsch`, `asech`, `exp`, `log`, `sqrt`, `sign`, `Abs`, `Max`, `Min`, `arg`, `ceiling`, `floor`

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

Note that in lists of groups the items should ideally be written on the form $q_1^{c_1} \cdot q_2^{c_2} \cdots q_n^{c_n}$ where $q_1, q_2 \ldots q_n$ are quantities and $c_1, c_2 \ldots c_n$ are integers, but the function can also handle item that are sums with terms written on the form $a \cdot q_1^{c_1} \cdot q_2^{c_2} \cdots q_n^{c_n}$ where $q_1, q_2 \ldots q_n$ are quantities, $c_1, c_2 \ldots c_n$ rational numbers and $a$ a constant.

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

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax     | Relaxed syntax  |
|-------------------|:----------------|
| `v**2`            | `v^2`           |
| `5*v**2`          | `5v^2`          |
| `(d/t)**2+v**2`   | `(d/t)^2+v^2`   |
| `d**2/t**2`       | `d^2/t^2`       |
| `d**2*t**(-2)`    | `d^2 t^(-2)`    |
| `d/t*v`           | `vd/t`          |

#### b)
Checking the dimensions of a quantity directly, i.e. the dimensions of an expression of the form `number*units`, no predefined quantities are necessary.

Here a response area with input type `TEXT` and one grading parameter,`comparison`, will be used.

`comparison` is set to `dimensions`.

The answer is set two some expression with the right dimensions, e.g. `length**2/time**2`.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer we do not need to set any input symbols.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax                           | Relaxed syntax                        | Using symbols      |
|-----------------------------------------|:--------------------------------------|:-------------------|
| `metre**2/second**2`                    | `metre^2/second^2`                    | `m^2/s^2`          |
| `(centi*metre)**2/hour**2`              | `(centimetre)^2/h^2`                  | `(cm)^2/h^2`       |
| `246*ohm/(kilo*gram)*coulomb**2/second` | `246 ohm/(kilogram) coulomb^2/second` | `246 O/(kg) c^2/s` |


### 2 Checking the value of an expression or a physical quantity

This examples checks if your expression is equal to $2~\frac{\mathrm{kilometre}}{\mathrm{hour}}$.

#### a)

Here an expression with predefined quantities is checked as exactly as possible. This is done with a TEXT response area with the following parameters:
`quantities` is set to:
```
('d','(length)') ('t','(time)') ('v','(length/time)')
```
Note that short form symbols cannot be used when defining quantities.

`comparison` is set to `expressionExact`.

The response area answer is set to `2*v` but there are many other expressions that would work just as well. Note that we cannot write `2*kilo*metre/second` as response or answer since the predefined quantity `t` will substitute the `t` in `metre` which results in unparseable input.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units and single character symbols are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax   | Relaxed syntax  |
|-----------------|:----------------|
| `2*v`           | `2v`            |
| `2000/3600*d/t` | `2000/3600 d/t` |
| `1/1.8*d/t`     | `d/(1.8t)`      |
| `v+1/3.6*d/t`   | `v+d/(3.6t)`    |

#### b)

Checking if a quantity is equal to $2~\frac{kilometre}{hour}$ with a fixed absolute tolerance of $0.05 \frac{metre}{second}$ can be done with a TEXT response area with `atol` set to `0.05` and the answer set to `2*kilo*metre/hour`. 

**Note:** `atol` is always assumed to be given in the base SI units version of the expression. This is likely to change in future versions of the function.

The `comparison` parameter could also be set to `expression` but since this is the default it is not necessary.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer no input symbols are necessary.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax         | Relaxed syntax       | Using symbols |
|-----------------------|:---------------------|:--------------|
| `0.556*metre/second`  | `0.556 metre/second` | `0.556 m/s`   |
| `0.560*metre/second`  | `0.560 metre/second` | `0.560 m/s`   |
| `0.6*metre/second`    | `0.6 metre/second`   | `0.6 m/s`     |
| `2*kilo*metre/hour`   | `2 kilometre/hour`   | `2 km/h`      |
| `1.9*kilo*metre/hour` | `1.9 kilometre/hour` | `1.9 km/h`    |
| `2.1*kilo*metre/hour` | `2.1 kilometre/hour` | `2.1 km/h`    |

In the example given in the example problem set, the following responses are tested and evaluated as incorrect:

| Strict syntax         | Relaxed syntax       | Using symbols  |
|-----------------------|:---------------------|:--------------|
| `0.61*metre/second`   | `0.61 metre/second`  | `0.61 m/s`    |
| `2.2*kilo*metre/hour` | `2.2 kilometre/hour` | `2.2 km/h`    |

#### c)

Checking if a quantity is equal to $2~\frac{kilometre}{hour}$ with a fixed relative tolerance of $0.05$ can be done with a TEXT response area with `rtol` set to `0.05` and the answer set to `2*kilo*metre/hour`. 

The `comparison` parameter could also be set to `expression` but since this is the default it is not necessary.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax          | Relaxed syntax        | Using symbols  |
|------------------------|:----------------------|:---------------|
| `0.533*metre/second`   | `0.533 metre/second`  | `0.533 m/s`    |
| `2.08*kilo*metre/hour` | `2.08 kilometre/hour` | `2.08 km/h`    |

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected it is not necessary to set any input symbols.

In the example given in the example problem set, the following responses are tested and evaluated as incorrect:

| Strict syntax          | Relaxed syntax        | Using symbols  |
|------------------------|:----------------------|:---------------|
| `0.522*metre/second`   | `0.522 metre/second`  | `0.522 m/s`    |
| `2.11*kilo*metre/hour` | `2.11 kilometre/hour` | `2.11 km/h`    |

### 3 Checking if a set of quantities match the Buckingham pi theorem

#### a)

In this example the task is: Given $U$, $L$ and $\nu$, suggest a dimensionless group.

For this problem we do not need to predefine any quantities and give exact dimensions. The algorithm assumes that all symbols in the answer (that are not numbers or predefined constants such as $\pi$) are quantities and that there are no other quantities that should appear in the answer.

**Note:** This means that the algorithm does not in any way check that the stated answer is dimensionless, ensuring that that is left to the problem author.

For this example a TEXT response area is used with `comparison` set to `buckinghamPi` and answer set to `['U*L/nu']`. It is not necessary to use this specific answer, any example of a correct dimensionless group should work.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since `nu` is a multicharacter symbol it needs to be added as an input symbol.

#### b)

In this example the task is: Given $U$, $L$, $\nu$ and $f$, determine the necessary number of dimensionless groups and give one example of possible expressions for them.

This task is similar to example a) with two significant differences. First, adding $f$ means that there are now two groups required, and second the problem will constructed by defining the quantities and let the function compute the rest on its own instead of supplying a reference example.

For this example a TEXT response area is used with `comparison` set to `buckinghamPi`, `quantities` set to `('U','(length/time)') ('L','(length)') ('nu','(length**2/time)') ('f','(1/time)')` and `answer` set to `-`.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since `nu` is a multicharacter symbol it needs to be added as an input symbol.

#### c)

In this example the task is:
Suppose we are studying water waves that move under the influence of gravity. We suppose that the variables of interest are the acceleration in free fall $g$, the velocity of the wave $v$, the height of the wave $h$ and the wave length $\ell$. We also suppose that they are related by a dimensionally consistent equation $f(g,v,h,l) = 0$. Determine the minimum number of dimensionless $\pi$-variables needed to describe this problem according to the Buckingham pi-theorem and give one example of possible expressions for the dimensionless quantities.

For this problem two dimensionless groups are needed, see the worked solution for a terse solution that gives the general form of the dimensionless quantities.

For this example a TEXT response area is used with `comparison` set to `buckinghamPi` and then give a list of correct group expressions formatted as the code for a python list. For this example the answer `['g**(-2)*v**4*h*l**3', 'g**(-2)*v**4*h**2*l**4']` was used (this corresponds to $p_1 = 1$, $p_2 = 2$, $q_1 = 3$, $q_2 = 4$ in the worked solution).

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since `nu` is a multicharacter symbol it needs to be added as an input symbol.

### 4 Defining costum sets of units

In this problem it is demonstrated how to use `substitutions` to define costum units.

#### a)

In this problem currencies will be us as units, and thus the quantities will no longer be physical.

Here the `substitutions` parameter will be set so that the evaluation function can be used to compare. Note that using `substitutions` this way means that the default SI units can no longer be used.

The following exchange rates (from Bank of England 1 August 2022) will be used:

| Currency | Exchange rate |
|----------|:--------------|
| $1$ EUR  | $1.1957$ GBP  |
| $1$ USD  | $1.2283$ GBP  |
| $1$ CNY  | $8.3104$ GBP  |
| $1$ INR  | $96.943$ GBP  |

To compare prices written in different currencies a reference currency needs to be chosen. In this case GBP will be used. To substitute other currencies for their corresponding value in GBP the following grading parameter can be used:
```json
"substitutions":"('EUR','(1/1.1957)*GBP') ('USD','(1/1.2283)*GBP') ('CNY','(1/8.3104)*GBP') ('INR','(1/96.9430)*GBP')"
```
Since these conversion are not exact and for practical purposes prices are often not gives with more than two decimals of precision we also want to set the absolute tolerance, `atol`, to $0.05$.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. By setting the grading parameter `strict_syntax` to false the `*` can be omitted and `^` can be used instead of `**`. To ensure that this works correctly it is necessary to list the multicharacter symbols that are expected to appear in the answer and response as input symbols. For this example this means setting `EUR`, `USD`, `CNY` and `INR` as codes for inut symbols.

In the example given in the example problem set, the answer set to `10*GBP` and the following responses are tested and evaluated as correct:

| Strict syntax | Relaxed syntax |
|---------------|:---------------|
| `11.96*EUR`   | `11.96 EUR`    |
| `12.28*USD`   | `12.28 USD`    |
| `83.10*CNY`   | `83.10 CNY`    |
| `969.43*INR`  | `969.43 INR`   |
