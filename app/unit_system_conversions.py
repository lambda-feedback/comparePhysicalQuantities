# Remarks:
#   only K, no other temperature scales included
#   angles measures, bel an neper are all treated as identical dimensionless units

def list_of_SI_prefixes():
    """
    Prefixes taken from Table 5 https://physics.nist.gov/cuu/Units/prefixes.html
    """
    list = [
        ('yotta', 'Y',  '(10**24)'),
        ('zetta', 'Z',  '(10**21)'),
        ('exa',   'E',  '(10**18)'),
        ('peta',  'P',  '(10**15)'),
        ('tera',  'T',  '(10**12)'),
        ('giga',  'G',  '(10**9) '),
        ('mega',  'M',  '(10**6) '),
        ('kilo',  'k',  '(10**3) '),
        ('hecto', 'h',  '(10**2) '),
        ('deka',  'da', '(10**1) '),
        ('deci',  'd',  '(10**(-1)) '),
        ('centi', 'c',  '(10**(-2)) '),
        ('milli', 'm',  '(10**(-3)) '),
        ('micro', 'mu', '(10**(-6)) '),
        ('nano',  'n',  '(10**(-9)) '),
        ('pico',  'p',  '(10**(-12))'),
        ('femto', 'f',  '(10**(-15))'),
        ('atto',  'a',  '(10**(-18))'),
        ('zepto', 'z',  '(10**(-21))'),
        ('yocto', 'y',  '(10**(-24))')
        ]
    list.sort(key=lambda x: -len(x[0]))
    return list

def list_of_SI_base_unit_dimensions():
    """
    SI base units taken from Table 1 https://physics.nist.gov/cuu/Units/units.html
    Note that gram is used as a base unit instead of kilogram.
    """
    list = [
        ('metre',   'm',   'length'),
        ('gram',    'g',   'mass'),
        ('second',  's',   'time'),
        ('ampere',  'A',   'electric_current'),
        ('kelvin',  'K',   'temperature'),
        ('mole',    'mol', 'amount_of_substance'),
        ('candela', 'cd',  'luminous_intensity'),
        ]
    list.sort(key=lambda x: -len(x[0]))
    return list

def list_of_derived_SI_units_in_SI_base_units():
    """
    Derived SI units taken from Table 3 https://physics.nist.gov/cuu/Units/units.html
    Note that degrees Celsius is omitted.
    """
    list = [
        ('radian',    'r',   '(1)'), # Note: here 'r' is used instead of the more common 'rad' to avoid collision
        ('steradian', 'sr',  '(1)'),
        ('hertz',     'Hz',  '(second**(-1))'),
        ('newton',    'N',   '(metre*kilo*gram*second**(-2))'),
        ('pascal',    'Pa',  '(metre**(-1)*kilogram*second**(-2))'),
        ('joule',     'J',   '(metre**2*kilo*gram*second**(-2))'),
        ('watt',      'W',   '(metre**2*kilo*gram*second**(-3))'),
        ('coulomb',   'C',   '(second*ampere)'),
        ('volt',      'V',   '(metre**2*kilo*gram*second**(-3)*ampere**(-1))'),
        ('farad',     'F',   '(metre**(-2)*(kilo*gram)**(-1)*second**4*ampere**2)'),
        ('ohm',       'O', '(metre**2*kilo*gram*second**(-3)*ampere**(-2))'),
        ('siemens',   'S',   '(metre**(-2)*kilo*gram**(-1)*second**3*ampere**2)'),
        ('weber',     'Wb',  '(metre**2*kilo*gram*second**(-2)*ampere**(-1))'),
        ('tesla',     'T',   '(kilo*gram*second**(-2)*ampere**(-1))'),
        ('henry',     'H',   '(metre**2*kilo*gram*second**(-2)*ampere**(-2))'),
        ('lumen',     'lm',  '(candela)'),
        ('lux',       'lx',  '(metre**(-2)*candela)'),
        ('becquerel', 'Bq',  '(second**(-1))'),
        ('gray',      'Gy',  '(metre**2*second**(-2))'),
        ('sievert',   'Sv',  '(metre**2*second**(-2))'),
        ('katal',     'kat', '(second**(-1)*mole)')
        ]
    list.sort(key=lambda x: -len(x[0]))
    return list

def list_of_very_common_units_in_SI():
    """
    Commonly used non-SI units taken from Table 6 and 7 https://physics.nist.gov/cuu/Units/outside.html
    This is the subset of common symbols whose short form symbols are allowed
    """
    list = [
        ('minute',            'min', '(60*second)'),
        ('hour',              'h',   '(3600*second)'),
        ('degree',            'deg', '(pi/180)'),
        ('liter',             'L',   '(10**(-3)*metre**3)'),
        ('metricton',         't',   '(10**3*kilo*gram)'),
        ('neper',             'Np',  '(1)'),
        ('bel',               'B',   '((1/2)*log(10))'),
        ('electronvolt',      'eV',  '(1.60218*10**(-19)*joule)'),
        ('atomicmassunit',    'u',   '(1.66054*10**(-27)*kilo*gram)'),
        ('angstrom',          'å',   '(10**(-10)*metre)'),
        ]
    list.sort(key=lambda x: -len(x[0]))
    return list

def list_of_common_units_in_SI():
    """
    Commonly used non-SI units taken from Table 6 and 7 https://physics.nist.gov/cuu/Units/outside.html
    Note that short form symbols are defined here, but not used since they cause to many ambiguities
    """
    list = [
        ('day',               'd',   '(86400*second)'),
        ('angleminute',      "'",   '(pi/10800)'),
        ('anglesecond',      '"',   '(pi/648000)'),
        ('astronomicalunit', 'au',  '(149597870700*metre)'),
        ('nauticalmile',     'nmi', '(1852*metre)'), #Note: no short form in source, short form from Wikipedia
        ('knot',              'kn',  '((1852/3600)*metre/second)'), #Note: no short form in source, short form from Wikipedia
        ('are',               'a',   '(10**2*metre**2)'),
        ('hectare',           'ha',  '(10**4*metre**2)'),
        ('bar',               'bar', '(10**5*pascal)'),
        ('barn',              'b',   '(10**(-28)*metre**2)'),
        ('curie',             'Ci',  '(3.7*10**10*becquerel)'),
        ('roentgen',          'R',   '(2.58*10**(-4)*kelvin/(kilo*gram))'),
        ('rad',               'rad', '(10**(-2)*gray)'),
        ('rem',               'rem', '(10**(-2)*sievert)'),
        ]+list_of_very_common_units_in_SI()
    list.sort(key=lambda x: -len(x[0]))
    return list

def names_of_prefixes_units_and_dimensions():
    return tuple(x[0] for x in list_of_SI_prefixes())\
          +tuple(x[0] for x in list_of_SI_base_unit_dimensions())\
          +tuple(x[2] for x in list_of_SI_base_unit_dimensions())\
          +tuple(x[0] for x in list_of_derived_SI_units_in_SI_base_units())\
          +tuple(x[0] for x in list_of_common_units_in_SI())

def convert_short_forms():
    units = list_of_SI_base_unit_dimensions()\
           +list_of_derived_SI_units_in_SI_base_units()\
           +list_of_very_common_units_in_SI()
    protect_long_forms = [(x[0],x[0]) for x in units]\
                        +[(x[0],x[0]) for x in list_of_common_units_in_SI()]\
                        +[(x[2],x[2]) for x in list_of_SI_base_unit_dimensions()]\
                        +[(x[0],x[0]) for x in list_of_SI_prefixes()]
    protect_long_forms.sort(key=lambda x: -len(x[0]))
    collision_fixes = []
    for prefix in list_of_SI_prefixes():
        for unit in units:
            collision_fixes.append((prefix[1]+unit[1],     prefix[0]+"*("+unit[0]+")"))
            collision_fixes.append((prefix[1]+"*"+unit[1], prefix[0]+"*("+unit[0]+")"))
            collision_fixes.append((prefix[1]+" "+unit[1], prefix[0]+"*("+unit[0]+")"))
    collision_fixes.sort(key=lambda x: -len(x[0]))
    convert_short_forms_list = [(x[1],x[0]) for x in units]
    convert_short_forms_list.sort(key=lambda x: -len(x[0]))
    return protect_long_forms+collision_fixes+convert_short_forms_list

def convert_to_SI_base_units():
    return [[(x[0],x[2]) for x in list_of_common_units_in_SI()],\
            [(x[0],x[2]) for x in list_of_derived_SI_units_in_SI_base_units()],\
            [(x[0],x[2]) for x in list_of_SI_prefixes()]]

def convert_to_SI_base_units_short_form():
    return [convert_short_forms()]+convert_to_SI_base_units()

def convert_SI_base_units_to_dimensions(): 
    return convert_to_SI_base_units()+[[(x[0],x[2]) for x in list_of_SI_base_unit_dimensions()]]

def convert_SI_base_units_to_dimensions_short_form(): 
    return convert_to_SI_base_units_short_form()+[[(x[0],x[2]) for x in list_of_SI_base_unit_dimensions()]]