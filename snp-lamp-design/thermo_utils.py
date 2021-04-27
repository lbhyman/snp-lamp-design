import sys
import math
import random as rnd
import nupack as nu
# Allow nupack to use all available cores
nu.config.parallelism = True
# Allow nupack to use 1/4 of all available memory per job
import psutil
nu.config.cache = float(math.floor(psutil.virtual_memory()[0] / (4 * 1000000000)))


# Quick, approximate Tm calculation for a DNA sequence without using nupack
def TM(sequence):
    if len(sequence) < 1:
        return 1.0
    GC_count = float(sequence.count('G') + sequence.count('C'))
    AT_count = float(sequence.count('A') + sequence.count('T'))
    if len(sequence) > 13:
        # Wallace Formula - Wallace RB et al. (1979) Nucleic Acids Res 6:3543-3557, PMID 158748
        return 64.9 +41.0*(GC_count-16.4)/(GC_count+AT_count)
    else:
        # Marmur Formula
        return float(4*GC_count + 2*AT_count)

# Returns the reverse complement of the input DNA sequence
def reverse_complement(sequence):
    sequence = sequence[::-1].upper()
    sequence = sequence.replace('A','1').replace('T','2').replace('G','3').replace('C','4')
    sequence = sequence.replace('1','T').replace('2','A').replace('3','C').replace('4','G')
    return sequence

# Truncate a DNA sequence to a specific length
def truncate(sequence, end, trunc_size=1):
    length = len(sequence)
    if end == 3:
        sequence = sequence[:length-trunc_size]
    elif end == 5:
        sequence = sequence[trunc_size:]
    else:
        print("Improper args given to truncate()!")
        sys.exit(1)
    return sequence

# Randomly truncate a DNA sequence
def generate_truncations(seqlength,minlength):
    # Probe truncations
    trunc_length = rnd.randint(0,seqlength-minlength)
    five_trunc = rnd.randint(0,trunc_length)
    output = [five_trunc, trunc_length - five_trunc]
    # Probe complement truncation
    if rnd.randint(0,1) == 0:
        try:
            output += [output[1], rnd.randint(output[0],seqlength-minlength-trunc_length), 3]
        except(ValueError):
            output += [output[1], output[0], 3]
    else:
        try:
            output += [rnd.randint(output[1],seqlength-minlength-trunc_length), output[0], 5]
        except(ValueError):
            output += [output[1], output[0], 5]
    #Sink truncations
    trunc_length = rnd.randint(0,seqlength-minlength)
    five_trunc = rnd.randint(0,trunc_length)
    output += [five_trunc, trunc_length - five_trunc]
    # Sink complement truncation
    trunc_length = rnd.randint(trunc_length,seqlength-minlength)
    five_trunc = rnd.randint(output[6],trunc_length)
    output += [five_trunc, trunc_length - five_trunc]
    return output

# Helper function to process nupack output objects
def parse_nupack_output(result, tube_label, initial_concentrations):
    result_dict = result[tube_label].__dict__['complex_concentrations']
    for key in result_dict.keys():
        if key.name == '(probeF+probeQ)' or key.name == '(probeQ+probeF)':
            return 1.0 - (result_dict[key] / initial_concentrations['probeF'])

# Estimate the proportion of active probe when either or no target is present in solution
def get_activation(sequences, concentrations, params):
    model = nu.Model(material='dna', celsius=params['temperature'], sodium=params['sodium'], magnesium=params['magnesium'])
    # Define strands and sequences
    probeF = nu.Strand(sequences['probeF'], name='probeF')
    probeQ = nu.Strand(sequences['probeQ'], name='probeQ')
    sink = nu.Strand(sequences['sink'], name='sink')
    sinkC = nu.Strand(sequences['sinkC'], name='sinkC')
    non_mut_target = nu.Strand(sequences['non_mut_target'], name='non_mut_target')
    mut_target = nu.Strand(sequences['mut_target'], name='mut_target')
    # Define 3 tubes: one without target (initial), one with mutated target (mut), and one with non-mutated target (non_mut)
    initial_state = nu.Tube(strands={probeF:concentrations['probeF'],probeQ:concentrations['probeQ'],
                                     sink:concentrations['sink'],sinkC:concentrations['sinkC']},
                            complexes=nu.SetSpec(max_size=2, include=[[probeF,probeQ,sink,sinkC]]),
                            name='initial_state')
    mut_state = nu.Tube(strands={probeF:concentrations['probeF'],probeQ:concentrations['probeQ'],
                                     sink:concentrations['sink'],sinkC:concentrations['sinkC'],
                                     mut_target:concentrations['mut_target']},
                            complexes=nu.SetSpec(max_size=2, include=[[probeF,probeQ,sink,sinkC,mut_target]]),
                            name='mut_state')
    non_mut_state = nu.Tube(strands={probeF:concentrations['probeF'],probeQ:concentrations['probeQ'],
                                     sink:concentrations['sink'],sinkC:concentrations['sinkC'],
                                     non_mut_target:concentrations['non_mut_target']},
                            complexes=nu.SetSpec(max_size=2, include=[[probeF,probeQ,sink,sinkC,non_mut_target]]),
                            name='non_mut_state')
    # Compute proportion of probe which is active in each tube
    result = nu.tube_analysis(tubes=[initial_state,mut_state,non_mut_state], compute=['pairs', 'mfe'], model=model)
    initial_activation = parse_nupack_output(result, 'initial_state', concentrations)
    mut_activation = parse_nupack_output(result, 'mut_state', concentrations)
    non_mut_activation = parse_nupack_output(result, 'non_mut_state', concentrations)
    return initial_activation, mut_activation, non_mut_activation