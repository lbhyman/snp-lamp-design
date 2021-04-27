import random as rnd
from probe import Probe
from ga_optimizer import GAOptimizer

# Provides methods for randomly sampling the probe design space in addition to GA_Optimizer functionality
class RandomSampler(GAOptimizer):
    
    def __init__(self):
        super().__init__()

    # Randomly generate SNP and WT target sequences
    def generate_target(self, minlength=25, maxlength=40, minSNP=7):
        length = rnd.randint(minlength,maxlength)
        self.SNP = ''
        self.WT = ''
        for i in range(length):
            base = rnd.choice(['A','T','G','C'])
            self.SNP += base
            self.WT += base
        self.SNP_index = rnd.randint(minSNP,len(self.SNP)-1-minSNP)
        curr_base = self.SNP[self.SNP_index]
        new_base = self.SNP[self.SNP_index]
        while(curr_base == new_base):
            new_base = rnd.choice(['A','T','G','C'])
        self.SNP = self.SNP[:self.SNP_index] + new_base + self.SNP[self.SNP_index + 1:]
        return [self.SNP, self.WT, self.SNP_index]
    
    # Generate random probe and sink sequences based on pre-defined WT and SNP targets
    def sample_space(self, iterations, output_filename):
        outfile = open(output_filename,'w')
        outfile.write('Probe 5 trunc,Probe 3 trunc,Probe* 5 trunc,Probe* 3 trunc,Probe blunt end,Sink 5 trunc,Sink 3 trunc,Sink* 5 trunc,Sink* 3 trunc,beta,self.SNP activation,self.WT activation,Background activation\n')
        for i in range(iterations):
            print('Iteration: '+str(i))
            p = Probe.Probe(self.SNP,self.WT,self.minlength,self.concentrations,self.params,self.mutation_rate)
            p.display()
            for t in p.truncations:
                outfile.write(str(t)+',')
            for b in p.beta:
                outfile.write(str(b)+',')
            outfile.write('\n')
        outfile.close()
    
    # Generate random probe and sink sequences based on random WT and SNP targets        
    def sample_space_random(self, iterations, output_filename):
        outfile = open(output_filename,'w')
        outfile.write('Probe 5 trunc,Probe 3 trunc,Probe* 5 trunc,Probe* 3 trunc,Probe blunt end,Sink 5 trunc,Sink 3 trunc,Sink* 5 trunc,Sink* 3 trunc,beta,self.SNP activation,self.WT activation,Background activation, self.SNP Sequence, self.WT Sequence, self.SNP Index\n')
        for i in range(iterations):
            print('Iteration: '+str(i))
            sequences = self.generate_target()
            self.SNP = sequences[0]
            self.WT = sequences[1]
            self.SNP_index = sequences[2]
            p = Probe.Probe(self.SNP,self.WT,self.minlength,self.concentrations,self.params,self.mutation_rate)
            p.display()
            for t in p.truncations:
                outfile.write(str(t)+',')
            for b in p.beta:
                outfile.write(str(b)+',')
            outfile.write(self.SNP+',')
            outfile.write(self.WT+',')
            outfile.write(str(self.SNP_index))
            outfile.write('\n')
        outfile.close()