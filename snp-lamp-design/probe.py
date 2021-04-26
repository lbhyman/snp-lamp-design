import numpy as np
import random as rnd
import functools
import pickle as pk
import thermo_utils as tu

# Designates a fluorogenic probe set, including sequences and useful methods during GA and hill-climbing optimization
@functools.total_ordering
class Probe:
    
    def __init__(self,SNP,WT,minlength,normal_concentrations,SNP_concentrations,WT_concentrations,params,MUTATION_RATE,truncations=[]):
        self.SNP = SNP
        self.WT = WT
        self.minlength = minlength
        self.normal_concentrations = normal_concentrations
        self.SNP_concentrations = SNP_concentrations
        self.WT_concentrations = WT_concentrations
        self.params = params
        self.MUTATION_RATE = MUTATION_RATE
        self.truncations = truncations
        self.beta = [0,0,0,0]
        if truncations is None:
            self.truncations = tu.generate_truncations(len(self.SNP),self.minlength)
            self.id_to_sequence(self.truncations)
            while (not self.screen()):
                self.truncations = tu.generate_truncations(len(self.SNP),self.minlength)
                self.id_to_sequence(self.truncations)
        self.id_to_sequence(self.truncations)
    
    # Fitness-based sorting method for GA        
    def __lt__ (self, other):
        return self.beta[0] < other.beta[0]

    # Fitness-based sorting method for GA 
    def __eq__ (self, other):
        return self.beta[0] == other.beta[0]
    
    def get_sequences(self):
        return [self.probe,self.probeC,self.sink,self.sinkC,self.WT,self.SNP]
    
    def get_truncations(self):
        return self.truncations
    
    def get_key(self):
        return ','.join(str(elem) for elem in self.truncations)+','+self.SNP+','+self.WT
    
    def get_beta(self):
        return self.beta
    
    def set_beta(self, b):
        self.beta = b
    
    # Convert truncation representation to sequence representation    
    def id_to_sequence(self,seq_id):
        SNP_comp = tu.reverse_complement(self.SNP)
        self.probe = tu.truncate(tu.truncate(SNP_comp,5,seq_id[0]),3,seq_id[1])
        self.probeC = tu.truncate(tu.truncate(self.SNP,5,seq_id[2]),3,seq_id[3])
        WT_comp = tu.reverse_complement(self.WT)
        self.sink = tu.truncate(tu.truncate(WT_comp,5,seq_id[5]),3,seq_id[6])
        self.sinkC = tu.truncate(tu.truncate(self.WT,5,seq_id[7]),3,seq_id[8])
    
    # Create auxilliary sequence file for nupack calculations
    def generate_input_file(self,Lmax=2,prefix='temp'):
        sequences = [self.probe,self.probeC,self.sink,self.sinkC,self.WT,self.SNP]
        filename = prefix + '.in'
        outfile = open(filename,'w')
        outfile.write('6\n')
        for seq in sequences:
            outfile.write(seq+'\n')
        outfile.write(str(Lmax))
        outfile.close()
    
    # Calculate probe fitness    
    def calc_beta(self):
        self.generate_input_file()
        background = tu.get_activation(self.normal_concentrations,self.normal_concentrations,self.params)
        if background < 0:
            background = 0
        SNP = tu.get_activation(self.SNP_concentrations,self.normal_concentrations,self.params) - background
        WT = tu.get_activation(self.WT_concentrations,self.normal_concentrations,self.params) - background
        if WT < 0:
            WT = 0.0
        if SNP <= 0:
            self.beta = [0, SNP, WT, background]
            return [0, SNP, WT, background]
        b = SNP * np.log10(SNP/max(WT,background,0.0001))
        self.beta = [b, SNP, WT, background]
        return [b, SNP, WT, background]

    # Randomly change one truncation when probe is mutated during GA
    def mutate(self):
        if rnd.random() < self.MUTATION_RATE:
            index = rnd.choice([0,1,2,3,5,6,7,8])
            blunt_end = self.truncations[4]
            change = rnd.choice([-1,1])
            if blunt_end == 5 and (index == 0 or index == 3):
                self.truncations[0] = self.truncations[0] + change
                self.truncations[3] = self.truncations[3] + change
            elif blunt_end == 3 and (index == 1 or index == 2):
                self.truncations[1] = self.truncations[1] + change
                self.truncations[2] = self.truncations[2] + change
            else:
                self.truncations[index] = self.truncations[index] + change
            for i in range(len(self.truncations)):
                if self.truncations[i] < 0:
                    self.truncations[i] = 0
            self.id_to_sequence(self.truncations)
    
    # Cross the probe with another probe during GA    
    def cross(self,other_probe):
        probe_options = [self.truncations[:5],other_probe.truncations[:5]]
        sink_options = [self.truncations[5:],other_probe.truncations[5:]]
        choice = rnd.choice([0,1])
        new_truncations = probe_options[choice] + sink_options[1-choice]
        child = Probe(self.SNP,self.WT,self.minlength,self.normal_concentrations,self.SNP_concentrations,self.WT_concentrations,self.params,self.MUTATION_RATE,truncations=new_truncations)
        child.mutate()
        return child
    
    # Determine possible next steps for hill climbing
    def next_iteration(self):
        output = []
        truncations = self.truncations
        for i in range(len(truncations)):
            new_truncations = truncations.copy()
            new_truncations[i] = new_truncations[i] + 1
            if not new_truncations in output:
                output.append(new_truncations)
            new_truncations = truncations.copy()
            if truncations[i] >= 1:
                new_truncations[i] = new_truncations[i] - 1
                if not new_truncations in output:
                    output.append(new_truncations)
        return output
    
    # Determine whether the probe falls within the high-fitness design space by PCA
    def screen(self):
        probe = []
        # Determine probe and sink sequences
        SNP = self.SNP
        WT = self.WT
        tokenized = self.truncations
        probe_seq = self.probe
        probe_duplex = self.probeC
        sink_seq = self.sink
        sink_duplex = self.sinkC
        # Add probe Tms
        probe.append(tu.TM(probe_duplex))
        probe.append(tu.TM(probe_seq))
        # Add sink Tms
        probe.append(tu.TM(sink_duplex))
        probe.append(tu.TM(sink_seq))
        # Add Tm ratios
        probe.append(tu.TM(probe_duplex)-tu.TM(sink_duplex))
        probe.append(tu.TM(probe_seq)-tu.TM(sink_seq))
        probe.append(tu.TM(probe_seq)-tu.TM(probe_duplex))
        probe.append(tu.TM(sink_seq)-tu.TM(sink_duplex))
        # Add SNP proximity to ends
        SNP_pos = 0
        for i in range(len(SNP)):
            if SNP[i] != WT[i]:
                SNP_pos = i
        probe_3_dist = len(SNP) - 1 - tokenized[0] - SNP_pos
        probe_5_dist = SNP_pos - tokenized[1]
        probe_SNP_dist = min(probe_3_dist,probe_5_dist)
        probe_covered = 1
        if(probe_SNP_dist < 0):
            probe_covered = 0
        probeC_3_dist = len(SNP) - 1 - tokenized[3] - SNP_pos
        probeC_5_dist = SNP_pos - tokenized[2]
        probeC_SNP_dist = min(probeC_3_dist,probeC_5_dist)
        probeC_covered = 1
        if(probeC_SNP_dist < 0):
            probeC_covered = 0
        sink_3_dist = len(SNP) - 1 - tokenized[0] - SNP_pos
        sink_5_dist = SNP_pos - tokenized[1]
        sink_SNP_dist = min(sink_3_dist,sink_5_dist)
        sink_covered = 1
        if(sink_SNP_dist < 0):
            sink_covered = 0
        sinkC_3_dist = len(SNP) - 1 - tokenized[3] - SNP_pos
        sinkC_5_dist = SNP_pos - tokenized[2]
        sinkC_SNP_dist = min(sinkC_3_dist,sinkC_5_dist)
        sinkC_covered = 1
        if(sinkC_SNP_dist < 0):
            sinkC_covered = 0      
        probe.append(probe_SNP_dist)
        probe.append(probeC_SNP_dist)
        probe.append(sink_SNP_dist)
        probe.append(sinkC_SNP_dist)
        # Test if the probe falls within the high-fitness PCA region
        pca = pk.load(open("pca.pkl",'rb'))
        probe = np.array(probe)
        params_trans = pca.transform(probe.reshape(1,-1))
        if (params_trans[0][0] < 15 and params_trans[0][1] > -20 and params_trans[0][0] > -60 and params_trans[0][1] < 60):
            return True
        return False
    
    # Print probe sequences and key parameters    
    def display(self):
        print('beta: ' + str(self.beta[0]))
        print('SNP Activation: ' + str(self.beta[1]))
        print('WT Activation: ' + str(self.beta[2]))
        print('Background: ' + str(self.beta[3]))
        print('probe: ' + self.probe)
        print('probe*: ' + self.probeC)
        print('sink: ' + self.sink)
        print('sink*: ' + self.sinkC + '\n')
    
