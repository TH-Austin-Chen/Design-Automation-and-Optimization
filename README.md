# Genetic Algorithm

## Overview

This project implements a Genetic Algorithm (GA) in Python. The main steps are as follows:

1. **Initialize Parameters**: Declare the following:
   - Number of generations
   - Number of chromosomes per generation
   - Number of genes per chromosome
   - Crossover rate
   - Mutation rate
   - Reproduction rate
2. **Encoding**: Generate the initial population (first generation).
3. **Decoding**: Decode chromosomes into decimal values, ensuring the results fall within the specified range.
4. **Fitness Calculation**: Evaluate the decoded results using the given equation to compute fitness. Collect the minimum fitness value of each generation.
5. **Proportion Calculation**: Determine the probability of selecting each chromosome based on fitness for the roulette wheel selection.
6. **Roulette Wheel Selection**: Choose the method to generate offspring based on the roulette wheel.
7. **Generate Offspring**: Use the selected method to generate offspring.
8. **Replace Parent Generation**: Replace the parent generation with the offspring.
9. **Repeat Steps 2–8**: Iterate for the specified number of generations.
10. **Plot Results**: Visualize the results.

## Implementation Details

- After encoding, chromosomes are stored as a list:
  ```python
  ['Gene1', 'Gene2']
  ```
- A generation would look like:
  ```python
  [['gene1', 'gene2'],
   ['gene1', 'gene2'],
   ['gene1', 'gene2']]
  ```
- After decoding, each chromosome includes decoded values:
  ```python
  [['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2'], 
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2'],
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2']]
  ```
- After calculating fitness, each chromosome includes fitness values:
  ```python
  [['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness'],
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness'],
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness']]
  ```
- After calculating proportion, each chromosome includes selection probability:
  ```python
  [['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness', 'proportion'],
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness', 'proportion'],
   ['gene1', 'gene2', 'decoded_gene1', 'decoded_gene2', 'fitness', 'proportion']]
  ```
- Proportion Calculation: 
  Calculate selection probabilities by subtracting each fitness value from the maximum fitness value (max_fitness - fitness + 1), ensuring that even the best fitness has a chance of selection. You can also apply an exponent to amplify the differences.
- Crossover: 
  Choose a random crossover point. If there are two variables (x1, x2) and 10 genes per chromosome, there are 19 possible crossover points. Two offspring are generated and collected.
- Mutation: 
Perform a 0-to-1 or 1-to-0 flip for all genes.
- Reproduction: 
  Copy the selected parent directly into the offspring population.
