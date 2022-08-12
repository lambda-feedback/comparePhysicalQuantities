# Remarks:
#   only K, no other temperature scales included
#   angles measures, bel an neper are all treated as identical dimensionless units

def names_of_prefixes_base_SI_units_and_dimensions():
    return ('yotta','zetta','exa','peta','tera','giga','mega','kilo','hecto','deka',
            'deci','centi','milli','micro','nano','pico','femto','atto','zepto','yocto',
            'metre','gram','second','ampere','kelvin','mole','candela',
            'length','mass','time','electric_current','temperature','amount_of_substance','luminous_intensity')


def remove_SI_prefixes():
    """
    Prefixes taken from Table 5 https://physics.nist.gov/cuu/Units/prefixes.html
    """
    return ''.join("\
        ('yotta','(10**24)') \
        ('zetta','(10**21)') \
        ('exa',  '(10**18)') \
        ('peta', '(10**15)') \
        ('tera', '(10**12)') \
        ('giga', '(10**9) ') \
        ('mega', '(10**6) ') \
        ('kilo', '(10**3) ') \
        ('hecto','(10**2) ') \
        ('deka', '(10**1) ') \
        ('deci', '(10**(-1)) ') \
        ('centi','(10**(-2)) ') \
        ('milli','(10**(-3)) ') \
        ('micro','(10**(-6)) ') \
        ('nano', '(10**(-9)) ') \
        ('pico', '(10**(-12))') \
        ('femto','(10**(-15))') \
        ('atto', '(10**(-18))') \
        ('zepto','(10**(-21))') \
        ('yocto','(10**(-24))')\
        ".split())

def convert_SI_base_units_to_dimensions(): 
    """
    SI base units taken from Table 1 https://physics.nist.gov/cuu/Units/units.html
    Note that gram is used as a base unit instead of kilogram.
    """
    return ''.join("\
        ('metre',  'length') \
        ('gram',   'mass') \
        ('second', 'time') \
        ('ampere', 'electric_current') \
        ('kelvin', 'temperature') \
        ('mole',   'amount_of_substance') \
        ('candela','luminous_intensity')\
        ".split())

def convert_derived_SI_units_to_SI_base_units():
    """
    Derived SI units taken from Table 3 https://physics.nist.gov/cuu/Units/units.html
    Note that degrees Celsius is omitted.
    """
    return ''.join("\
        ('radian',   '(1)') \
        ('steradian','(1)') \
        ('hertz',    '(second**(-1))') \
        ('newton',   '(metre*kilo*gram*second**(-2))') \
        ('pascal',   '(metre**(-1)*kilogram*second**(-2))') \
        ('joule',    '(metre**2*kilo*gram*second**(-2))') \
        ('watt',     '(metre**2*kilo*gram*second**(-3))') \
        ('coulomb',  '(second*ampere)') \
        ('volt',     '(metre**2*kilo*gram*second**(-3)*ampere**(-1))') \
        ('farad',    '(metre**(-2)*(kilo*gram)**(-1)*second**4*ampere**2)') \
        ('ohm',      '(metre**2*kilo*gram*second**(-3)*ampere**(-2))') \
        ('siemens',  '(metre**(-2)*kilo*gram**(-1)*second**3*ampere**2)') \
        ('weber',    '(metre**2*kilo*gram*second**(-2)*ampere**(-1))') \
        ('tesla',    '(kilo*gram*second**(-2)*ampere**(-1))') \
        ('henry',    '(metre**2*kilo*gram*second**(-2)*ampere**(-2))') \
        ('lumen',    '(candela)') \
        ('lux',      '(metre**(-2)*candela)') \
        ('becquerel','(second**(-1))') \
        ('gray',     '(metre**2*second**(-2))') \
        ('sievert',  '(metre**2*second**(-2))') \
        ('katal',    '(second(-1)*mole)')\
        ".split())

def convert_common_units_to_SI():
    """
    Commonly used non-SI units taken from Table 6 and 7 https://physics.nist.gov/cuu/Units/outside.html
    """
    return ''.join("\
    ('min',              '(60*second)') \
    ('hour',             '(3600*second)') \
    ('day',              '(86400*second)') \
    ('angle_degree',     '(pi/180)') \
    ('angle_minute',     '(pi/10800)') \
    ('angle_second',     '(pi/648000)') \
    ('liter',            '(10**(-3)*metre**3)') \
    ('metric_ton',       '(10**3*kilo*gram)') \
    ('neper',            '(1)') \
    ('bel',              '((1/2)*log(10))') \
    ('electronvolt',     '(1.60218*10**(-19)*joule)') \
    ('atomic_mass_unit', '(1.66054*10**(-27)*kilo*gram)') \
    ('astronomical_unit','(149597870700*metre)') \
    ('nautical_mile',    '(1852*metre)') \
    ('knot',             '((1852/3600)*metre/second)') \
    ('are',              '(10**2*metre**2)') \
    ('hectare',          '(10**4*metre**2)') \
    ('bar',              '(10**5*pascal)') \
    ('angstrom',         '(10**(-10)*metre)') \
    ('barn',             '(10**(-28)*metre**2)') \
    ('curie',            '(3.7*10**10*becquerel)') \
    ('roentgen',         '(2.58*10**(-4)*kelvin/(kilo*gram))') \
    ('rad',              '(10**(-2)*gray)') \
    ('rem',              '(10**(-2)*sievert)')\
    ".split())

def convert_to_SI_base_units():
    return [convert_common_units_to_SI(), convert_derived_SI_units_to_SI_base_units(), remove_SI_prefixes()]