try:
    from .evaluation import evaluation_function
    from .unit_system_conversions import list_of_SI_prefixes, list_of_SI_base_unit_dimensions, list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI
except ImportError:
    from evaluation import evaluation_function
    from unit_system_conversions import list_of_SI_prefixes, list_of_SI_base_unit_dimensions, list_of_derived_SI_units_in_SI_base_units, list_of_very_common_units_in_SI, list_of_common_units_in_SI
	
def test_short_form_of_compound_units():
    # NOTE: Short forms for common units are not allowed
    units = [("","","")]\
            +list_of_SI_base_unit_dimensions()\
            +list_of_derived_SI_units_in_SI_base_units()\
            +list_of_very_common_units_in_SI()
    all_units = list_of_SI_base_unit_dimensions()\
                +list_of_derived_SI_units_in_SI_base_units()\
                +list_of_common_units_in_SI()
    all_long_forms = [x[0] for x in all_units]
    params = {"strict_syntax": False}
    prefixes_long_forms = [x[0] for x in list_of_SI_prefixes()]
    prefixes_short_forms = [x[1] for x in list_of_SI_prefixes()]
    m = len(prefixes_long_forms)
    long_forms = [x[0] for x in units]
    short_forms = [x[1] for x in units]
    n = len(long_forms)
    k = 0
    does_not_match_convention = []
    incorrect = []
    errors = []
    for i in range(0,n):
        for j in range(0,n):
            for a in range(0,m):
                answer = prefixes_long_forms[a]+"*"+long_forms[i]+"*"+long_forms[j]
                for prod in ["*"," ",""]:
                    response = prefixes_short_forms[a]+prod+short_forms[i]+prod+short_forms[j]
                    # Check if case matches convention
                    if short_forms[i] in prefixes_short_forms\
                    or prefixes_short_forms[a]+prod+short_forms[i] in prefixes_short_forms\
                    or short_forms[i]+prod+short_forms[j] in short_forms\
                    or any([x in response for x in all_long_forms]):
                        does_not_match_convention.append((answer,response))
                        continue
                    k += 1
                    print(f"{k} {answer}, {response}")
                    try:
                        result = evaluation_function(response, answer, params)
                    except:
                        errors.append((answer,response))
                        continue
                    if not result.get("is_correct"):
                        incorrect.append((answer,response))
    log_details = True
    if log_details:
        f = open("symbols_log.txt","w")
        f.write("Incorrect:\n"+"".join([str(x)+"\n" for x in incorrect])+"\nErrors:\n"+"".join([str(x)+"\n" for x in errors]))
        f.close()
        print(f"{len(incorrect)}/{k} {len(errors)}/{k} {(len(errors)+len(incorrect))/k} {len(does_not_match_convention)}/{k+len(does_not_match_convention)} {len(does_not_match_convention)/(k+len(does_not_match_convention))}")

test_short_form_of_compound_units()