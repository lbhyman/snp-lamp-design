import argparse
import sys
from os import environ
from pathlib import Path
from dotenv import load_dotenv
from ga_optimizer import GAOptimizer
import thermo_utils as tu

# Establish path to nupack installation
def setup_environment():
    load_dotenv(Path('..') / 'constants.env')
    nupackhome = environ.get('NUPACKHOME', '../nupack3.2.2')
    environ['NUPACKHOME'] = nupackhome

# Handle user input
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Create an optimal probe-sink pair to detect a SNP mutation')
    parser.add_argument('SNP', help='Mutated sequence')
    parser.add_argument('Non_SNP', help='Non-mutated sequence')
    parser.add_argument('-i', '--mut_index', type=int,
                        default=-1, help='Position of the first mutated base')
    parser.add_argument('-T', '--temperature', type=float,
                        default=21, help='Final Temperature in Celsius')
    parser.add_argument('-s', '--sodium', type=float,
                        default=0.065, help='[sodium] in M')
    parser.add_argument('-m', '--magnesium', type=float,
                        default=0.008, help='[magnesium] in M')
    parser.add_argument('-l', '--minlength', type=int,
                        default=6, help='minimum duplex length')
    parser.add_argument('-M', '--mutation_rate', type=float,
                        default=0.5, help='mutation probability')
    parser.add_argument('-P', '--pop_size', type=int,
                        default=128, help='initial population size')
    args = parser.parse_args()
    params = " -T "+str(args.temperature)+" -material "+'DNA'+" -sort 0 -sodium " + \
        str(args.sodium)+" -magnesium "+str(args.magnesium)
    return args, params

# Generate optimal probe and print output
def main(args=None):
    setup_environment()
    args, params = parse_arguments()
    optimizer = GAOptimizer(WT=args.Non_SNP, SNP=args.SNP, params=params, minlength=args.minlength,
                            mut_rate=args.mutation_rate, pop_size=args.pop_size, SNP_index=args.mut_index)
    optimizer.run()
    tu.cleanup()

if __name__ == "__main__":
    main()
