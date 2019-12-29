import sys
from unitsclasses import FeetAndInches
import converters

if len(sys.argv) != 2:
    print('usage: %s <src.dsl>' % sys.argv[0])
    sys.exit(1)

with open(sys.argv[1], 'r') as file:
    for line in file:
        if not line or line[0] == '#':
            continue
        parts = line.split()
        function_to_call = getattr(converters, parts[0])
        quantity = parts[1].split('-')
        fractional_inches = quantity[2].split('/')
        imperial_units = FeetAndInches(float(quantity[0]), float(quantity[1]),
                                       int(fractional_inches[0])/int(fractional_inches[1]))
        print(function_to_call(imperial_units))



