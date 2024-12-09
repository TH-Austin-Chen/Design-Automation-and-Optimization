# 設定基因bit數、染色體數、代數、產生子代方式機率
import random
import math
import matplotlib.pyplot as plt

bit_num = 10  # num of bit in a chromosome
chromosome_num = 1000  # num of chromosome in a generation
generation_num = 200  # num of interation
crossover_rate = 0.75
mutation_rate = 0.05
reproduction_rate = 0.20
dimension = 5


# 產生第一代，每個染色體會長成['基因1', '基因2']的形式
# 將一整代存成一個名為"generation"的list
# generation的list也作為container，裡面還有代表每個染色體的list(稱為chromosome)
# 基因為染色體list裡的第一個item
def encode(generation):
    # 生成n個chromosome
    for i in range(chromosome_num):
        chromosome = []
        # 每個染色體內放入隨機生成的基因
        for i in range(dimension):
            gene = ''.join(str(random.randint(0, 1)) for _ in range(bit_num))
            chromosome.append(gene)
        generation.append(chromosome)
    # print(generation)
    return generation


# 解碼
# 每個染色體會長成['基因1', '基因2..., '基因5', '解碼且有理化後的基因1', '解碼且有理化後的基因2',..., '解碼且有理化後的基因5']的形式
def decode(generation):
    for inner_list in generation:
        binary_string1 = inner_list[0]
        binary_string2 = inner_list[1]
        binary_string3 = inner_list[2]
        binary_string4 = inner_list[3]
        binary_string5 = inner_list[4]
        # 轉成題目要求的範圍
        decimal_number = int(binary_string1, 2) * 65.536 / (2 ** bit_num - 1) - 32.768
        inner_list.append(decimal_number)
        decimal_number = int(binary_string2, 2) * 65.536 / (2 ** bit_num - 1) - 32.768
        inner_list.append(decimal_number)
        decimal_number = int(binary_string3, 2) * 65.536 / (2 ** bit_num - 1) - 32.768
        inner_list.append(decimal_number)
        decimal_number = int(binary_string4, 2) * 65.536 / (2 ** bit_num - 1) - 32.768
        inner_list.append(decimal_number)
        decimal_number = int(binary_string5, 2) * 65.536 / (2 ** bit_num - 1) - 32.768
        inner_list.append(decimal_number)
    return generation


# Ackley’s Path Function & fitness
def apf(generation):
    a = 20
    b = 0.2
    c = 2 * math.pi
    result_list = []
    for inner_list in generation:
        x1 = inner_list[5]
        x2 = inner_list[6]
        x3 = inner_list[7]
        x4 = inner_list[8]
        x5 = inner_list[9]
        sum1 = x1 ** 2 + x2 ** 2 + x3 ** 2 + x4 ** 2 + x5 ** 2
        sum2 = math.cos(c * x1) + math.cos(c * x2) + math.cos(c * x3) + math.cos(c * x4) + math.cos(c * x5)
        after = -a * (math.e ** (-b * ((sum1 / 5) ** 0.5))) - (math.e ** (sum2 / 5)) + a + math.e
        inner_list.append(after)
        result_list.append(inner_list)
        result_list.sort(key=lambda x: x[10])
    min_result = result_list[0][10]
    # 順便抓最小值
    #min_result = min([inner_list[10] for inner_list in result_list])
    # print(result_list)
    return result_list, min_result, result_list[0][5:10]


# proportion
def proportion(result_list):
    # 取出最大值
    max_result = max([inner_list[10] for inner_list in result_list])
    # print(max_result)
    for inner_list in result_list:
        inner_list.append('')
    # print(result_list)
    for inner_list in result_list:
        # 所有值改為"最大值-原值+1"，會+1是為了使最大值也有機會被挑中
        inner_list[11] = max_result - inner_list[10] + 1
    # print(result_list)
    return result_list


# roulette for method
def roulette_for_method():
    rand_num = random.random()
    if rand_num <= crossover_rate:
        method = 'crossover'
    elif rand_num > crossover_rate and rand_num <= (crossover_rate + mutation_rate):
        method = 'mutation'
    else:
        method = 'reproduction'
    # print(method)
    return method


# roulette for chromosome
def roulette_for_chromosome(result_list):
    total_weight = sum([inner_list[11] for inner_list in result_list])
    rand_num = random.uniform(0, total_weight)

    # Initialize variables for cumulative weight and selected inner list
    cumulative_weight = 0
    selected_inner_list = None

    # Iterate over inner lists
    for inner_list in result_list:
        # Add weight of current inner list to cumulative weight
        cumulative_weight += inner_list[11]

        # If cumulative weight is greater than or equal to random number, select current inner list
        if cumulative_weight >= rand_num:
            selected_inner_list = inner_list[:5]
            break

    # print(selected_inner_list)
    return selected_inner_list


# main
generation = []
c5 = encode(generation)
min_gens = []
best = float("inf")
for i in range(generation_num):
    c10 = decode(c5)
    c11, min_result, coordinate = apf(c10)
    if min_result < best:
        best = min_result
        xy = coordinate
    print(coordinate, ':', min_result)
    min_gens.append(min_result)
    c12 = proportion(c11)
    new_list = []
    while len(new_list) < chromosome_num:
        method = roulette_for_method()
        if method == 'crossover':
            s1 = roulette_for_chromosome(c12)
            s2 = roulette_for_chromosome(c12)
            d1 = ['', '', '', '', '']
            d2 = ['', '', '', '', '']
            point = random.randint(1, (bit_num * 5 - 1))
            if point < bit_num - 1:
                d1[0] = s1[0][:point] + s2[0][point:]
                d1[1] = s2[1]
                d1[2] = s2[2]
                d1[3] = s2[3]
                d1[4] = s2[4]
                d2[0] = s2[0][:point] + s1[0][point:]
                d2[1] = s1[1]
                d2[2] = s1[2]
                d2[3] = s1[3]
                d2[4] = s1[4]
            elif point < bit_num * 2 - 1:
                d1[0] = s1[0]
                d1[1] = s1[1][:point] + s2[1][point:]
                d1[2] = s2[2]
                d1[3] = s2[3]
                d1[4] = s2[4]
                d2[0] = s2[0]
                d2[1] = s2[1][:point] + s1[1][point:]
                d2[2] = s1[2]
                d2[3] = s1[3]
                d2[4] = s1[4]
            elif point < bit_num * 3 - 1:
                d1[0] = s1[0]
                d1[1] = s1[1]
                d1[2] = s1[2][:point] + s2[2][point:]
                d1[3] = s2[3]
                d1[4] = s2[4]
                d2[0] = s2[0]
                d2[1] = s2[1]
                d2[2] = s2[2][:point] + s1[2][point:]
                d2[3] = s1[3]
                d2[4] = s1[4]
            elif point < bit_num * 4 - 1:
                d1[0] = s1[0]
                d1[1] = s1[1]
                d1[2] = s1[2]
                d1[3] = s1[3][:point] + s2[3][point:]
                d1[4] = s2[4]
                d2[0] = s2[0]
                d2[1] = s2[1]
                d2[2] = s2[2]
                d2[3] = s2[3][:point] + s1[3][point:]
                d2[4] = s1[4]
            else:
                d1[0] = s1[0]
                d1[1] = s1[1]
                d1[2] = s1[2]
                d1[3] = s1[3]
                d1[4] = s1[4][:point] + s2[4][point:]
                d2[0] = s2[0]
                d2[1] = s2[1]
                d2[2] = s2[2]
                d2[3] = s2[3]
                d2[4] = s2[4][:point] + s1[4][point:]
            new_list.append(d1)
            new_list.append(d2)
        elif method == 'mutation':
            p3 = roulette_for_chromosome(c12)
            d3 = [''.join(['1' if c == '0' else '0' for c in s]) for s in p3]
            new_list.append(d3)
        else:
            p4 = roulette_for_chromosome(c12)
            new_list.append(p4)
    c5.clear()
    c5.extend(new_list)
    #print(i)

print('best:')
print(xy, ':', best)

#print(min_gens)
# Plot the minimum value of each generation
plt.plot(min_gens)
plt.title('Minimum Value per Generation')
plt.xlabel('Generation')
plt.ylabel('Minimum Value')
plt.show()