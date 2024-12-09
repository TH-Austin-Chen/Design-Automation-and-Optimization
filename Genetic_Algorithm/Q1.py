import random
import math
import matplotlib.pyplot as plt

bit_num = 10
chromosome_num = 1000
generation_num = 100
crossover_rate = 0.75
mutation_rate = 0.05
reproduction_rate = 0.20

def encode(generation):
    for i in range(chromosome_num):
        chromosome = []
        for i in range(2):
            gene = ''.join(str(random.randint(0, 1)) for _ in range(bit_num))
            chromosome.append(gene)
        generation.append(chromosome)
    return generation

def decode(generation):
    for inner_list in generation:
        binary_string1 = inner_list[0]
        binary_string2 = inner_list[1]
        decimal_number = int(binary_string1, 2) * 20 / (2 ** bit_num - 1) - 10
        inner_list.append(decimal_number)
        decimal_number = int(binary_string2, 2) * 20 / (2 ** bit_num - 1) - 10
        inner_list.append(decimal_number)
    return generation

def shubert(generation):
    result_list = []
    for inner_list in generation:
        x1 = inner_list[2]
        x2 = inner_list[3]
        sum1 = 0
        sum2 = 0
        for i in range(1, 6):
            sum1 += i * math.cos((i + 1) * x1 + i)
            sum2 += i * math.cos((i + 1) * x2 + i)
        after = sum1 * sum2
        inner_list.append(after)
        result_list.append(inner_list)
        result_list.sort(key=lambda x: x[4])
    min_result = result_list[0][4]
    # min_result = min([inner_list[4] for inner_list in result_list])
    return result_list, min_result, result_list[0][2:4]

def proportion(result_list):
    max_result = max([inner_list[4] for inner_list in result_list])
    for inner_list in result_list:
        inner_list.append('')
    for inner_list in result_list:
        inner_list[5] = (max_result - inner_list[4] + 1) ** 2
    return result_list

def roulette_for_method():
    rand_num = random.random()
    if rand_num <= crossover_rate:
        method = 'crossover'
    elif rand_num > crossover_rate and rand_num <= (crossover_rate + mutation_rate):
        method = 'mutation'
    else:
        method = 'reproduction'
    return method

def roulette_for_chromosome(result_list):
    total_weight = sum([inner_list[5] for inner_list in result_list])
    rand_num = random.uniform(0, total_weight)
    cumulative_weight = 0
    selected_inner_list = None

    for inner_list in result_list:
        cumulative_weight += inner_list[5]

        if cumulative_weight >= rand_num:
            selected_inner_list = inner_list[:2]
            break

    return selected_inner_list


generation = []
c2 = encode(generation)
min_gens = []
best = float("inf")
for i in range(generation_num):
    c4 = decode(c2)
    c5, min_result, coordinate = shubert(c4)
    if min_result < best:
        best = min_result
        xy = coordinate
    print(coordinate, ':', min_result)
    min_gens.append(min_result)
    c6 = proportion(c5)
    new_list = []
    while len(new_list) < chromosome_num:
        method = roulette_for_method()
        if method == 'crossover':
            point = random.randint(1, bit_num * 2 - 1)
            s1 = roulette_for_chromosome(c6)
            s2 = roulette_for_chromosome(c6)
            new_gene1 = ['', '']
            new_gene2 = ['', '']
            if point < bit_num:
                new_gene1[0] = s1[0][:point] + s2[0][point:]
                new_gene1[1] = s2[1]
                new_gene2[0] = s2[0][:point] + s1[0][point:]
                new_gene2[1] = s1[1]
            else:
                new_gene1[0] = s1[0]
                new_gene1[1] = s1[1][:point] + s2[1][point:]
                new_gene2[0] = s2[0]
                new_gene2[1] = s2[1][:point] + s1[0][point:]
            new_list.append(new_gene1)
            new_list.append(new_gene2)
        elif method == 'mutation':
            p3 = roulette_for_chromosome(c6)
            d3 = [''.join(['1' if c == '0' else '0' for c in s]) for s in p3]
            new_list.append(d3)
        else:
            p4 = roulette_for_chromosome(c6)
            new_list.append(p4)
        #print(i)
        c2.clear()
        c2.extend(new_list)
print('best:')
print(xy, ':', best)

#rint(min_gens)
plt.plot(min_gens)
plt.title('Minimum Value per Generation')
plt.xlabel('Generation')
plt.ylabel('Minimum Value')
plt.show()