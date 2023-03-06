from pysmt.shortcuts import Symbol, Int, And, Or, GE, LE, LT, Not, is_sat
from pysmt.typing import INT
from pysmt.smtlib.parser import SmtLibParser
import json

def validate_json_file(file_path):
    max_hits = Symbol('max_hits', INT)
    min_hits = Symbol('min_hits', INT)
    num_cars = Symbol('num_cars', INT)
    formula = And(
        GE(max_hits, Int(0)),
        LT(max_hits, Int(600)),
        GE(min_hits, Int(0)),
        LT(min_hits, Int(200)),
        Or(
            And(GE(num_cars, Int(0)), LT(num_cars, Int(50))),
            
        ),
        LE(num_cars, max_hits),
        LT(num_cars, min_hits),
    )

    with open(file_path, 'r') as f:
        data = json.load(f)

    if 'max_hits' in data and 'min_hits' in data and 'num_cars' in data and isinstance(data['max_hits'], int) and isinstance(data['min_hits'], int) and isinstance(data['num_cars'], int):
        substitution = {max_hits: Int(data['max_hits']), min_hits: Int(data['min_hits']), num_cars: Int(data['num_cars'])}
        simplified_formula = formula.substitute(substitution)
        print("Simplified formula:", simplified_formula)
        parser = SmtLibParser()
        #smt_formula = parser.serialize(simplified_formula)
        #print("SMT formula:", smt_formula)
        is_valid = not is_sat(Not(simplified_formula))
        print(f"Is the JSON file valid? {is_valid}")
        return is_valid
    else:
        return False

file_path = 'conf.json'
is_valid = validate_json_file(file_path)
print(f"Is the JSON file valid? {is_valid}")
