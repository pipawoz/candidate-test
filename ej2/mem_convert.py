import os
import argparse
import sys
import re


def mem_convert(input_file, output_file):
    """ Change mem initialization syntax """

    with open(os.path.join(os.getcwd(), input_file), 'r') as f:
        input_file_data = f.read()

    input_mem_regex = r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n'

    mem_data = re.search(input_mem_regex, input_file_data).group(0)  # Get the mem data from input file
    replaced_data = "{}\n  $readmemh(\"{}\", mem);\n".format(mem_data.splitlines()[0], output_file)  # Restore first line
    converted_data = re.sub(input_mem_regex, replaced_data, input_file_data)  # Replace with correct format

    mem_dump_regex = r'8\'h(.*);'
    dump_data = re.findall(mem_dump_regex, mem_data)  # Get the dump mem data

    with open(os.path.join(os.getcwd(), "{}.converted".format(input_file)), 'w') as f:
        f.write(converted_data)

    with open(os.path.join(os.getcwd(), output_file), 'w') as f:
        dump_data = '\n'.join(dump_data) + '\n'
        f.write(dump_data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", help="Input file to be converted", required=True)
    parser.add_argument("--output-file", help="Output dump mem file", required=True)

    argspar = parser.parse_args()
    args = vars(argspar)

    input_file = args['input_file']
    output_file = args['output_file']

    mem_convert(input_file=input_file, output_file=output_file)
