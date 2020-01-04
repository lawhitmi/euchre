from unitsclasses import FeetAndInches
from functools import reduce


def convert(imperial_units):
    return str(round(imperial_units * 0.3148, 2)) + ' m'


def build_structure(inputs):
    feet, inches, fractional_inches = inputs
    feet_structure = FeetAndInches(feet, inches, fractional_inches)
    return feet_structure


def get_decimal(instance):
    return instance.getDecimal()


def add(instances):
    instance1, instance2 = instances
    return instance1 + instance2


def build_tuple_for_feet_structure(quantity):
    feet = float(quantity[0])
    inches = float(quantity[1])
    fractional_inches = quantity[2].split('/')
    return feet, inches, int(fractional_inches[0])/int(fractional_inches[1])


def parser(line):
    if not line or line[0] == '#':
        return
    parts = line.split()
    if parts[0] == 'convert':
        quantity = parts[1].split('-')
        inputs = build_tuple_for_feet_structure(quantity)
        function_list = [convert, get_decimal, build_structure]
        combined_function = reduce(lambda f, g: lambda x: f(g(x)), function_list, lambda x: x)
        return str(combined_function(inputs))
    elif parts[0] == 'add':
        quantity1 = parts[1].split('-')
        quantity2 = parts[4].split('-')
        inputs1 = build_tuple_for_feet_structure(quantity1)
        inputs2 = build_tuple_for_feet_structure(quantity2)
        result = add(tuple(map(build_structure, [inputs1, inputs2])))
        return str(result)


def return_results(results_map):
    result_strings = tuple(results_map)
    for i in result_strings:
        print(i)
