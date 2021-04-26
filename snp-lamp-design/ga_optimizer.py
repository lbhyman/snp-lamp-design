import random as rnd
import math
from probe import Probe

# Stores and optimizes potential probe sets using Genetic Algorithm and hill-climbing approaches
class GAOptimizer:
    
    def __init__(self, WT, SNP, SNP_index=-1, \
            normal_concentrations=['1e-7','1e-7','1e-7','1e-7','0e1','0e1'], \
            SNP_concentrations=['1e-7','1e-7','1e-7','1e-7','0e1','1e-7'], \
            WT_concentrations=['1e-7','1e-7','1e-7','1e-7','1e-7','0e1'], \
            minlength=6, params='', generations=6, pop_size=128, num_parents=64, mut_rate=0.5):
        # GA hyperparameters
        self.population_size = pop_size
        self.num_parents = num_parents
        self.generations = generations
        if self.population_size != 128:
            self.num_parents = math.floor(self.population_size / 2)
            self.generations = math.floor(math.log2(self.num_parents))
        self.mutation_rate = mut_rate
        # Min duplex length
        self.minlength = minlength
        # Full-length sequences
        self.WT = WT
        self.SNP = SNP
        # Index of the first mismatching (SNP) base
        self.SNP_index = SNP_index
        if self.SNP_index == -1:
            for i in range(min(len(WT), len(SNP))):
                if WT[i] != SNP[i]:
                    self.SNP_index = i
                    break
        # Concentrations of each strand in M
        self.normal_concentrations = normal_concentrations
        self.SNP_concentrations = SNP_concentrations
        self.WT_concentrations = WT_concentrations
        # Buffer Conditions
        self.params = params
        # Store fitness of previously encountered probes to improve efficiency
        self.probe_dict = {}
    
    # Determine the sensitivity and specificity of a given probe
    def calculate_fitness(self, probe):
        key = probe.get_key()
        if(key in self.probe_dict):
            probe.set_beta(self.probe_dict.get(key))
        else:
            beta = probe.calc_beta()
            self.probe_dict[key] = beta
    
    # Randomly generate a starting population for the GA
    def generate_initial_population(self):
        population = []
        for i in range(self.population_size):
            parent = Probe.Probe(self.SNP,self.WT,self.minlength,self.normal_concentrations,self.SNP_concentrations,self.WT_concentrations,self.params,self.mutation_rate)
            self.calculate_fitness(parent)
            population.append(parent)
            parent.display()
        population.sort(reverse=True)
        return population

    # Run a single generation of the GA
    def run_generation(self, population):
        # Ensure that all parents are unique
        parents = {}
        for probe in population:
            key = probe.get_key()
            if(len(parents) < self.num_parents):
                if(not key in parents):
                    parents[key] = probe
        parents = list(parents.values())
        new_population = parents
        # Generate children
        for parent in new_population:
            parent.display()
        for i in range(self.population_size - self.num_parents):
            parent_1 = rnd.choice(parents)
            parent_2 = rnd.choice(parents)
            # Improve diversity by introducing randomness when parents are identical
            if(parent_2.get_truncations() == parent_1.get_truncations()):
                parent_2 = Probe.Probe(self.SNP,self.WT,self.minlength,self.normal_concentrations,self.SNP_concentrations,self.WT_concentrations,self.params,self.mutation_rate)
            if(parent_2.get_truncations() == parent_1.get_truncations()):
                if(rnd.random() < 0.5):
                    child = parent_1.cross(parent_2)
                else:
                    child = parent_2
            else:
                child = parent_1.cross(parent_2)
            self.calculate_fitness(child)
            new_population.append(child)
            child.display()
        new_population.sort(reverse=True)
        return new_population

    # Produce an optimal probe via genetic algorithm
    def run_GA_taper(self):
        output = []
        print("------------------Generation 0-------------------")
        population = self.generate_initial_population()
        output.append(population[0])
        for i in range(self.generations):
            print("------------------Generation " + str(i+1) + "-------------------")
            new_population = self.run_generation(population)
            population = new_population
            output.append(population[0])
            self.population_size = int(self.population_size/2)
            self.num_parents = int(self.num_parents/2)
        return output
    
    # Further optimize a GA-produced probe using hill-climbing
    def hill_climb_optimize(self, probe):
        iterations = [probe]
        last_beta = -1
        self.calculate_fitness(probe)
        best_beta = probe.get_beta()[0]
        best_probe = probe
        while(last_beta != best_beta):
            next_truncs = best_probe.next_iteration()
            best_beta = best_probe.get_beta()[0]
            for trunc in next_truncs:
                curr_probe = Probe.Probe(self.SNP,self.WT,self.minlength,self.normal_concentrations,  
                    self.SNP_concentrations,self.WT_concentrations,self.params,self.mutation_rate, 
                        truncations=trunc)
                self.calculate_fitness(curr_probe)
                this_beta = curr_probe.get_beta()[0]
                curr_probe.display()
                if this_beta > best_beta:
                    best_beta = this_beta
                    best_probe = curr_probe
            iterations.append(best_probe)
            last_beta = iterations[-2].get_beta()[0]
        best_probe.display()
        return iterations[1:], best_probe
    
    # Run GA, followed by hill-climbing to produce an optimized probe
    def run(self):
        iter_GA = self.run_GA_taper()
        iter_hill, best_probe = self.hill_climb_optimize(iter_GA[-1])
        return iter_hill, best_probe
        