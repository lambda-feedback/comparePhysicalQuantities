# ComparePhysicalQuantities
This is an **EXPERIMENTAL** evaluation function with some dimensional analysis functionality.

This function lacks a nice GUI, can be quite brittle, and will likely change significantly in the near future.

**Note:** This function cannot handle short form symbols for units, all units names must be written out in lower/case letter. For example `10 Nm` or `10 Newton metre` will not be handled correctly, but `10 newton metre` will.

**Note:** Prefixes have lower precedence exponentiation, e.g. `10 cm**2` will be interpreted as `10*10^(-2) `

**Note:** This function allows omitting `*` and using `^` instead of `**` if the grading parameter `strict_syntax` is set to false. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as a list in the grading parameter `symbols`.

## Inputs
All input parameters need to be supplied via the **Grading parameters** panel.

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

SI base units taken from Table 5 of https://physics.nist.gov/cuu/Units/prefixes.html

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

Derived SI units taken from Table 3 of https://physics.nist.gov/cuu/Units/units.html

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

Commonly used non-SI units taken from Table 6 and 7 of https://physics.nist.gov/cuu/Units/outside.html

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

How big the difference is between the value of the answer and the value of the response is decided by the `rtol` and `atol` parameters. If neither `atol` nor `rtol` is specified the function will allow a relative error of $10^{-12}$. If `atol` is specified its value will be interpreted as the maximum allowed absolute error. If `rtol` is specified its value will be interpreted as the maximum allowed relative error. If both `atol` and `rtol` the function will check both the absolute and relative error.

#### `expressionExact`

Converts the expression to base SI units and checks that the answer and response are identical to the highest precision possible (note that some unit conversions are not exact and that using decimal numbers in the answer or response limits this to floating point precision).

#### `dimensions`

Checks that the answer and response have the same dimensions, but does not compare the values of the physical quantities.

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

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units and single character symbols are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax     | Relaxed syntax  |
|-------------------|:----------------|
| `v**2`            | `v^2`           |
| `5*v**2`          | `5v^2`          |
| `(d/t)**2+v**2`   | `(d/t)^2+v^2`   |
| `d**2/t**2`       | `d^2/t^2`       |
| `d**2*t**(-2)`    | `d^2 t^(-2)`    |
| `d/t*v`           | `vd/t`          |

### b)
Checking the dimensions of a quantity directly, i.e. the dimensions of an expression of the form `number*units`, no predefined quantities are necessary.

Here a response area with input type `TEXT` and one grading parameter,`comparison`, will be used.

`comparison` is set to `dimensions`.

The answer is set two some expression with the right dimensions, e.g. `length**2/time**2`.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax                           | Relaxed syntax                        |
|-----------------------------------------|:--------------------------------------|
| `metre**2/second**2`                    | `metre^2/second^2`                    |
| `(centi*metre)**2/hour**2`              | `(centimetre)^2/hour^2`               |
| `246*ohm/(kilo*gram)*coulomb**2/second` | `246 ohm/(kilogram) coulomb^2/second` |


## 2 Checking the value of an expression or a physical quantity

This examples checks if your expression is equal to $2~\frac{\mathrm{kilometre}}{\mathrm{hour}}$.

### a)

Here an expression with predefined quantities is checked as exactly as possible. This is done with a TEXT response area with the following parameters:
`quantities` is set to:
```
('d','(length)') ('t','(time)') ('v','(length/time)')
```

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

### b)

Checking if a quantity is equal to $2~\frac{kilometre}{hour}$ with a fixed absolute tolerance of $0.05 \frac{metre}{second}$ can be done with a TEXT response area with `atol` set to `0.05` and the answer set to `2*kilo*metre/hour`. 

**Note:** `atol` is always assumed to be given in the base SI units version of the expression. This is likely to change in future versions of the function.

The `comparison` parameter could also be set to `expression` but since this is the default it is not necessary.

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax         | Relaxed syntax       |
|-----------------------|:---------------------|
| `0.556*metre/second`  | `0.556 metre/second` |
| `0.560*metre/second`  | `0.560 metre/second` |
| `0.6*metre/second`    | `0.6 metre/second`   |
| `2*kilo*metre/hour`   | `2 kilometre/hour`   |
| `1.9*kilo*metre/hour` | `1.9 kilometre/hour` |
| `2.1*kilo*metre/hour` | `2.1 kilometre/hour` |

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as incorrect:

| Strict syntax         | Relaxed syntax       |
|-----------------------|:---------------------|
| `0.61*metre/second`   | `0.61 metre/second`  |
| `2.2*kilo*metre/hour` | `2.2 kilometre/hour` |


### c)

Checking if a quantity is equal to $2~\frac{kilometre}{hour}$ with a fixed relative tolerance of $0.05$ can be done with a TEXT response area with `rtol` set to `0.05` and the answer set to `2*kilo*metre/hour`. 

The `comparison` parameter could also be set to `expression` but since this is the default it is not necessary.

In the example given in the example problem set, the following responses are tested and evaluated as correct:

| Strict syntax          | Relaxed syntax        |
|------------------------|:----------------------|
| `0.533*metre/second`   | `0.533 metre/second`  |
| `2.08*kilo*metre/hour` | `2.08 kilometre/hour` |

With default settings it is required to put `*` (or `/`) between each part of the response and answer. To remove this requirement the grading parameter `strict_syntax` is set to false. Since only default SI units are expected in the answer we will not set the grading parameter `symbols`.

In the example given in the example problem set, the following responses are tested and evaluated as incorrect:

| Strict syntax          | Relaxed syntax        |
|------------------------|:----------------------|
| `0.522*metre/second`   | `0.522 metre/second`  |
| `2.11*kilo*metre/hour` | `2.11 kilometre/hour` |

## 3 Checking if a set of quantities match the Buckingham pi theorem

### a)

In this example the task is: Given $U$, $L$ and $\nu$, suggest a dimensionless group.

For this problem we do not need to predefine any quantities and give exact dimensions. The algorithm assumes that all symbols in the answer (that are not numbers or predefined constants such as $\pi$) are quantities and that there are no other quantities that should appear in the answer. 

**Note:** This means that the algorithm does not in any way check that the stated answer is dimensionless, ensuring that that is left to the problem author.

For this example a TEXT response area is used with `comparison` set to `buckinghamPi` and answer set to `['U*L/nu']`. Note that even though there is only one expression it still needs to written like a python list. It is also not necessary to use this specific answer, any example of a correct dimensionless group should work.

### b)

See example for context, see worked solution for a terse and probably more obtuse than necessary solution.

At the time of writing it was 3 weeks ago that I promised Peter I would properly write down how this worked. Hopefully I will do that soon.

The neat part is that for this problem you do not need to define any quantities, you just set `comparison` to `buckinghamPi` and then give a list of correct group expressions formatted as the code for a python list. For this example I used the answer `['g**(-2)*v**4*h*l**3', 'g**(-2)*v**4*h**2*l**4']`.

## 4 Using the evaluation function for things other than it's intended purpose

In this problem we use `substitutions` to define costum units in different ways.

### a)

Here a problem is constructed with answer $1.23$ watt where the short form symbol (e.g. $1.23$ W) can be used for the answer.

Here the `substitutions` parameter will be set in such a way that the short form symbols for some SI units can be used. This is somewhat complicated since there are ambiguities in the meanings of the short symbols. Only an illustrative subset of the SI units will be implemented.

Note that using `substitutions` this way means that the default SI units can no longer be used.

The short form symbols in the table below will be implemented.

| Unit or prefix | Symbol |
|----------------|:-------|
| metre          | m      |
| gram           | g      |
| second         | s      |
| newton         | N      |
| watt           | W      |
| joule          | J      |
| pascal         | Pa     |
| mega           | M      |
| kilo           | k      |
| hecto          | h      |
| deka           | da     |
| deci           | d      |
| centi          | c      |
| milli          | m      |
| micro          | mu     |

There are three SI base units and four derived SI units in the table. One way to define an appropriate set of substitution is to start with converting the derived SI units into base SI units. For instance the string `('W','(J/s)')|('J','(N*m)')('Pa','(N/(m**2))')|('N','(m*(k*g)/(s**2))')` will first substitute watts with joules per second, then substitutes joules and pascals to with expressions involving newtons and metres, and finally substitutes newtons with an expression only invovling base SI units. note the `|` placed in the strring to ensure that the substitutions are done in the correct order.

Next note that both metre and milli use the symbol m. This ambiguity can be resolved by extending the table with extra symbols where milli is already applied to the base SI units.

| Unit or prefix | Symbol |
|----------------|:-------|
| metre          | m      |
| gram           | g      |
| second         | s      |
| millimetre     | mm     |
| milligram      | mg     |
| milliwatt      | mW     |
| millinewton    | mN     |
| millipascal    | mPa    |
| millisecond    | ms     |
| mega           | M      |
| kilo           | k      |
| hecto          | h      |
| deka           | da     |
| deci           | d      |
| centi          | c      |
| micro          | mu     |

The string 
```
('mW','(10**(-3))*W') ('mJ','(10**(-3))*J') ('mPa','(10**(-3))*Pa') ('mN','(10**(-3))*N') ('mm','(10**(-3))*m') ('mg','(10**(-3))*g') ('ms','(10**(-3))*s')
```
defines the substitutions corresponding to these extra table symbols. The remaining prefixes do not cause any collisions so defining their substitutions is straightforward `('M','10**6') ('k','10**3') ('h','10**2') ('da','10**1') ('d','10**(-1)') ('c','10**(-2)') ('mu','10**(-6)')`. **Note:** the parenthesis around the substitutions for the prefixes help avoiding some parsing problems that can be difficult to predict.

Thus the entire sequence of substitutions can be defined by joining the different substitution strings into a single string with appropriately placed `|`. The substitutions need to be ordered such that the SI units with milliprefixes are substituted first, then other SI units, then the remaining prefixes.

This gives the grading parameter:
```json
"substitutions":"('mW','(10**(-3))*W') ('mJ','(10**(-3))*J') ('mPa','(10**(-3))*Pa') ('mN','(10**(-3))*N') ('mm','(10**(-3))*m') ('mg','(10**(-3))*g') ('ms','(10**(-3))*s')|('W','(J/s)')|('J','(N*m)') ('Pa','(N/(m**2))')|('N','(m*(k*g)/(s**2))')|('M','10**6') ('k','10**3') ('h','10**2') ('da','10**1') ('d','10**(-1)') ('c','10**(-2)') ('mu','10**(-6)')"
```

With default settings it is required to put `*` (or `/`) between each part of the response and answer. By setting the grading parameter `strict_syntax` to false the `*` can be omitted and `^` can be used instead of `**`. To ensure that this works correctly it is necessary to list the multicharacter symbols that are expected to appear in the answer and response in the grading parameter `symbols`. For this example this means setting `symbols` to `mPa,Pa,da,mu,mg,mm,mW,mN,ms`.

Setting the answer of the question to be `1.23*W` gives the desired answer.

In the example given in the example problem set, the following responses are tested and evaluated as correct:
| Strict syntax  | Relaxed syntax  |
|----------------|:----------------|
`1.23*W`         | `1.23 W`        |
`123*c*W`        | `123 cW`        |
`0.00000123*M*W` | `0.00000123 MW` |
`0.00123*k*W`    | `0.00123 kW`    |
`0.0123*h*W`     | `0.0123 hW`     |
`0.123*da*W`     | `0.123 daW`     |
`12.3*d*W`       | `12.3 dW`       |
`123*c*W`        | `123 cW`        |
`1230*mW`        | `1230 mW`       |
`1230000*mu*W`   | `1230000 muW`   |
`1.23*J/s`       | `1.23 J/s`      |
`1.23*N*m/s`     | `1.23 Nm/s`     |
`1.23*Pa*m**3/s` | `1.23 Pam^3/s`  |

### b)

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

With default settings it is required to put `*` (or `/`) between each part of the response and answer. By setting the grading parameter `strict_syntax` to false the `*` can be omitted and `^` can be used instead of `**`. To ensure that this works correctly it is necessary to list the multicharacter symbols that are expected to appear in the answer and response in the grading parameter `symbols`. For this example this means setting `symbols` to `EUR,USD,CNY,INR`.

In the example given in the example problem set, the answer set to `10*GBP` and the following responses are tested and evaluated as correct:

| Strict syntax | Relaxed syntax |
|---------------|:---------------|
| `11.96*EUR`   | `11.96 EUR`    |
| `12.28*USD`   | `12.28 USD`    |
| `83.10*CNY`   | `83.10 CNY`    |
| `969.43*INR`  | `969.43 INR`   |