import sys
from converters import parser, return_results


if len(sys.argv) != 2:
    print('usage: %s <src.dsl>' % sys.argv[0])
    sys.exit(1)

with open(sys.argv[1], 'r') as file:
    results = map(parser, file)
    return_results(results)



