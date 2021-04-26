import sys
import os
import subprocess as sub
import random as rnd

# Quick, approximate Tm calculation for a DNA sequence without using nupack
@staticmethod
def TM(sequence):
    if len(sequence) < 1:
        return 1.0
    GC_count = float(sequence.count('G') + sequence.count('C'))
    AT_count = float(sequence.count('A') + sequence.count('T'))
    if len(sequence) > 13:
        # Wallace Formula - Wallace RB et al. (1979) Nucleic Acids Res 6:3543-3557, PMID 158748
        return 64.9 +41.0*(GC_count-16.4)/(GC_count+AT_count)
    else:
        return float(4*GC_count + 2*AT_count)

# Returns the reverse complement of the input DNA sequence
@staticmethod    
def reverse_complement(sequence):
    sequence = sequence[::-1].upper()
    sequence = sequence.replace('A','1').replace('T','2').replace('G','3').replace('C','4')
    sequence = sequence.replace('1','T').replace('2','A').replace('3','C').replace('4','G')
    return sequence

# Truncate a DNA sequence to a specific length
@staticmethod
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
@staticmethod
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

# Generate auxilliary 'concentrations' file for nupack
@staticmethod
def generate_con_file(concentrations,prefix='temp'):
    filename = prefix + '.con'
    outfile = open(filename,'w')
    for con in concentrations:
        outfile.write(str(con)+'\n')
    outfile.close()

# Wrapper for the nupack 'complexes' function
@staticmethod        
def complexes(params,prefix='temp'):
    if (prefix+'.ocx') in os.listdir('./'):
        os.remove(prefix+'.ocx')
    args = os.environ['NUPACKHOME'] + "/build/bin/complexes " + prefix + params
    call = sub.Popen(args, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.STDOUT)
    sub.Popen.wait(call)

# Wrapper for the nupack 'concentrations' function
@staticmethod  
def concentrations(params,prefix='temp'):
    if (prefix+'.eq') in os.listdir('./'):
        os.remove(prefix+'.eq')
    args = os.environ['NUPACKHOME'] + "/build/bin/concentrations " + prefix + params
    call = sub.Popen(args, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.STDOUT)
    sub.Popen.wait(call)

# Calculate the proportion of fluorescent probe which is unquenched
@staticmethod    
def get_activation(input_concentrations,normal_concentrations,params,prefix='temp'):
    generate_con_file(input_concentrations)
    complexes(params)
    concentrations(params)
    filename = prefix + ".eq"
    file = open(filename, 'r')
    text = file.read()
    file.close()
    lines = text.split('\n')
    try:
        final_concentration = float(lines[52].split('\t')[9])
        initial_concentration = float(normal_concentrations[0])
        activation = (initial_concentration - final_concentration) / initial_concentration
        return activation
    except:
        return -1

# Delete auxilliary files used by nupack    
@staticmethod
def cleanup(prefix='temp'):
    filenames = [prefix+'.con',prefix+'.ocx',prefix+'.eq',prefix+'.in']
    for filename in filenames:
        try:
            os.remove(filename)
        except:
            pass
    return