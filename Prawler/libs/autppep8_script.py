import sys
import subprocess as sp


if len(sys.argv) < 3:
    print('plz input filename')
    sys.exit()

input_filename = sys.argv[1]
output_filename = sys.argv[2]
stdout = open(output_filename,'w')
sp.call(f'python -m autopep8 {input_filename}',stdout=stdout)
