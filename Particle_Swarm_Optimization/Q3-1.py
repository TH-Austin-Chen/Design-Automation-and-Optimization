import random
import matplotlib.pyplot as plt
import numpy as np


F = [
    0.475814929, 73.62871899, 315.7651478, 699.8888924, 1076.003744, 1340.113494, 1472.221934, 1498.332855, 1451.450047, 1348.577303,
    1216.718414, 1074.87717, 943.0573626, 833.2627837, 749.4972241, 679.7644751, 590.0683279, 486.4125737, 402.8010038, 365.2374093,
    371.7255815, 418.2693115, 472.8723908, 519.5386103, 546.2717614, 551.0756354, 533.9540233, 498.9107164, 451.949506, 407.0741833,
    376.2885394, 349.5963657, 309.0014533, 250.5075934, 180.1185774, 117.8381963, 79.67024143, 53.61850401, 31.68677525, 1.878846367
]

# 設定particle數、iteration代數
n_p = 150
n_i = 150
alpha_min = 0.000001
alpha_max = 32
beta_min = 0.000001
beta_max = 32
delta_min = 0.000001
delta_max = 40
a_min = 0.000001
a_max = 32
b_min = 0.000001
b_max = 32
w = 0.729
c1 = 1.49445
c2 = 1.49445
# 以2維為例，對於每個particle來說，pbest與velocity記為[pbest_alpha, pbest_beta, v_alpha, v_beta]，再丟到swarm裡面
swarm = []


def initial_random():
    result_alpha = random.uniform(alpha_min, alpha_max)
    result_beta = random.uniform(beta_min, beta_max)
    result_delta = random.uniform(delta_min, delta_max)
    result_a = random.uniform(a_min, a_max)
    result_b = random.uniform(b_min, b_max)
    return result_alpha, result_beta, result_delta, result_a, result_b


# 更新now_alpha, now_beta, now_delta, now_a, now_b, pbest_alpha, pbest_beta, pbest_delta, pbest_a, pbest_b, pbest_value
# v_alpha, v_beta, v_delta, v_a, v_b尚未改動
# swarm的list內有對應每個particle的inner list[now_alpha, now_beta, now_delta, now_a, now_b, v_alpha, v_beta, v_delta, v_a, v_b, pbest_alpha, best_beta, pbest_delta, pbest_a, pbest_b, pbest_value]
def fitness(swarm):
    new_swarm = []
    for i in swarm:
        start_alpha = i[0]
        start_beta = i[1]
        start_delta = i[2]
        start_a = i[3]
        start_b = i[4]
        v_alpha = i[5]
        v_beta = i[6]
        v_delta = i[7]
        v_a = i[8]
        v_b = i[9]

        v_percent = 0.01

        now_alpha = start_alpha
        now_beta = start_beta
        now_delta = start_delta
        now_a = start_a
        now_b = start_b
        pbest_candidate = []
        if v_alpha == 0 and v_beta == 0 and v_delta == 0 and v_a == 0 and v_b == 0:
            new_particle = []
            my_points = []
            for t in range(40):
                if t < now_delta:
                    function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10)))
                else:
                    function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10))) + now_b * ((t - now_delta) ** now_alpha) * (
                        np.exp(-(now_beta * (t - now_delta) / 10)))
                my_points.append(function)
            error = 0
            for j in range(40):
                error += (my_points[j] - F[j]) ** 2
            after = error ** 0.5
            new_particle.append(now_alpha)
            new_particle.append(now_beta)
            new_particle.append(now_delta)
            new_particle.append(now_a)
            new_particle.append(now_b)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(now_alpha)
            new_particle.append(now_beta)
            new_particle.append(now_delta)
            new_particle.append(now_a)
            new_particle.append(now_b)
            new_particle.append(after)
        elif v_alpha > 0:
            for num in range(100):
                value = []
                value.append(now_alpha)
                value.append(now_beta)
                value.append(now_delta)
                value.append(now_a)
                value.append(now_b)
                my_points = []
                for t in range(1, 41):
                    if t < now_delta:
                        function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10)))
                    else:
                        function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10))) + now_b * ((t - now_delta) ** now_alpha) * (
                            np.exp(-(now_beta * (t - now_delta) / 10)))
                    my_points.append(function)
                error = 0
                for j in range(40):
                    error += (my_points[j] - F[j]) ** 2
                after = error ** 0.5
                value.append(after)
                now_alpha += v_percent * v_alpha
                now_beta += v_percent * v_beta
                now_delta += v_percent * v_delta
                now_a += v_percent * v_a
                now_b += v_percent * v_b
                pbest_candidate.append(value)
                if now_alpha < alpha_min or now_alpha > alpha_max or now_beta < beta_min or now_beta > beta_max or now_delta < delta_min or now_delta > delta_max or now_a < a_min or now_a > a_max or now_b < b_min or now_b > b_max:
                    break
            now_alpha = now_alpha - v_percent * v_alpha
            now_beta = now_beta - v_percent * v_beta
            now_delta = now_delta - v_percent * v_delta
            now_a = now_a - v_percent * v_a
            now_b = now_b - v_percent * v_b
            smallest_sixth_item = min(pbest_candidate, key=lambda x: x[5])[5]
            new = [x for x in pbest_candidate if x[5] == smallest_sixth_item]
            pbest_alpha = new[0][0]
            pbest_beta = new[0][1]
            pbest_delta = new[0][2]
            pbest_a = new[0][3]
            pbest_b = new[0][4]
            pbest_value = new[0][5]
            new_particle = []
            if pbest_value < i[15]:
                new_particle.append(now_alpha)
                new_particle.append(now_beta)
                new_particle.append(now_delta)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_alpha)
                new_particle.append(v_beta)
                new_particle.append(v_delta)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(pbest_alpha)
                new_particle.append(pbest_beta)
                new_particle.append(pbest_delta)
                new_particle.append(pbest_a)
                new_particle.append(pbest_b)
                new_particle.append(pbest_value)
            else:
                new_particle.append(now_alpha)
                new_particle.append(now_beta)
                new_particle.append(now_delta)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_alpha)
                new_particle.append(v_beta)
                new_particle.append(v_delta)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(i[10])
                new_particle.append(i[11])
                new_particle.append(i[12])
                new_particle.append(i[13])
                new_particle.append(i[14])
                new_particle.append(i[15])
        else:
            for num in range(100):
                value = []
                value.append(now_alpha)
                value.append(now_beta)
                value.append(now_delta)
                value.append(now_a)
                value.append(now_b)
                my_points = []
                for t in range(1, 41):
                    if t < now_delta:
                        function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10)))
                    else:
                        function = now_a * (t ** now_alpha) * (np.exp(-(now_beta * t / 10))) + now_b * ((t - now_delta) ** now_alpha) * (
                            np.exp(-(now_beta * (t - now_delta) / 10)))
                    my_points.append(function)
                error = 0
                for j in range(40):
                    error += (my_points[j] - F[j]) ** 2
                after = error ** 0.5
                value.append(after)
                now_alpha += v_percent * v_alpha
                now_beta += v_percent * v_beta
                now_delta += v_percent * v_delta
                now_a += v_percent * v_a
                now_b += v_percent * v_b
                pbest_candidate.append(value)
                if now_alpha < alpha_min or now_alpha > alpha_max or now_beta < beta_min or now_beta > beta_max or now_delta < delta_min or now_delta > delta_max or now_a < a_min or now_a > a_max or now_b < b_min or now_b > b_max:
                    break
            now_alpha = now_alpha - v_percent * v_alpha
            now_beta = now_beta - v_percent * v_beta
            now_delta = now_delta - v_percent * v_delta
            now_a = now_a - v_percent * v_a
            now_b = now_b - v_percent * v_b
            smallest_sixth_item = min(pbest_candidate, key=lambda x: x[5])[5]
            new = [x for x in pbest_candidate if x[5] == smallest_sixth_item]
            pbest_alpha = new[0][0]
            pbest_beta = new[0][1]
            pbest_delta = new[0][2]
            pbest_a = new[0][3]
            pbest_b = new[0][4]
            pbest_value = new[0][5]
            new_particle = []
            if pbest_value < i[15]:
                new_particle.append(now_alpha)
                new_particle.append(now_beta)
                new_particle.append(now_delta)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_alpha)
                new_particle.append(v_beta)
                new_particle.append(v_delta)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(pbest_alpha)
                new_particle.append(pbest_beta)
                new_particle.append(pbest_delta)
                new_particle.append(pbest_a)
                new_particle.append(pbest_b)
                new_particle.append(pbest_value)

            else:
                new_particle.append(now_alpha)
                new_particle.append(now_beta)
                new_particle.append(now_delta)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_alpha)
                new_particle.append(v_beta)
                new_particle.append(v_delta)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(i[10])
                new_particle.append(i[11])
                new_particle.append(i[12])
                new_particle.append(i[13])
                new_particle.append(i[14])
                new_particle.append(i[15])
        new_swarm.append(new_particle)
    return new_swarm


# 更新v_alpha, v_beta, v_delta, v_a, v_b
def velo(new_swarm):
    gbest_value = min(new_swarm, key=lambda x: x[15])[15]
    new = [x for x in new_swarm if x[15] == gbest_value]
    gbest_alpha = new[0][10]
    gbest_beta = new[0][11]
    gbest_delta = new[0][12]
    gbest_a = new[0][13]
    gbest_b = new[0][14]
    print('[', gbest_alpha, ',', gbest_beta, ',', gbest_delta, ',', gbest_a, ',', gbest_b, ']:', gbest_value)
    gbest_loc = [gbest_alpha, gbest_beta, gbest_delta, gbest_a, gbest_b]
    for i in new_swarm:
        rand_p = random.random()
        rand_g = random.random()
        v_alpha = i[5] * w + c1 * rand_p * (i[10] - i[0]) + c2 * rand_g * (gbest_alpha - i[0])
        v_beta = i[6] * w + c1 * rand_p * (i[11] - i[1]) + c2 * rand_g * (gbest_beta - i[1])
        v_delta = i[7] * w + c1 * rand_p * (i[12] - i[2]) + c2 * rand_g * (gbest_delta - i[2])
        v_a = i[8] * w + c1 * rand_p * (i[13] - i[3]) + c2 * rand_g * (gbest_a - i[3])
        v_b = i[9] * w + c1 * rand_p * (i[14] - i[4]) + c2 * rand_g * (gbest_b - i[4])
        i[5] = v_alpha
        i[6] = v_beta
        i[7] = v_delta
        i[8] = v_a
        i[9] = v_b
    return new_swarm, gbest_value, gbest_loc


# 初始位置
# swarm的list內有對應每個particle的inner list[now_alpha, now_beta, v_alpha, v_beta]
for i in range(n_p):
    particle = []
    result_alpha, result_beta, result_delta, result_a, result_b = initial_random()
    particle.append(result_alpha)
    particle.append(result_beta)
    particle.append(result_delta)
    particle.append(result_a)
    particle.append(result_b)
    v_alpha_initial = 0
    v_beta_initial = 0
    v_delta_initial = 0
    v_a_initial = 0
    v_b_initial = 0
    particle.append(v_alpha_initial)
    particle.append(v_beta_initial)
    particle.append(v_delta_initial)
    particle.append(v_a_initial)
    particle.append(v_b_initial)
    particle.append(result_alpha)
    particle.append(result_beta)
    particle.append(result_delta)
    particle.append(result_a)
    particle.append(result_b)
    particle.append(0)
    swarm.append(particle)

# iteration
gbest_list = []
gbest_loc_list = []
for i in range(n_i):
    print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for k in swv:
        swarm.append(k)

alpha = gbest_loc_list[n_i-1][0]
beta = gbest_loc_list[n_i-1][1]
delta = gbest_loc_list[n_i-1][2]
a = gbest_loc_list[n_i-1][3]
b = gbest_loc_list[n_i-1][4]
f_points = []
for t in range(1, 41):
    if t < delta:
        function = a * (t ** alpha) * (np.exp(-(beta * t / 10)))
    else:
        function = a * (t ** alpha) * (np.exp(-(beta * t / 10))) + b * ((t - delta) ** alpha) * (np.exp(-(beta * (t - delta) / 10)))
    f_points.append(function)

plt.plot(gbest_list)
plt.title('Global Best Value per Iteration')
plt.xlabel('Iteration')
plt.ylabel('Global Best Value')
plt.show()

plt.plot(f_points, color='orange', label='PSO results')
plt.plot(F, color='purple', label='Original')
plt.title('Comparison of PSO results and the original data')
plt.xlabel('Time')
plt.ylabel('Pulse')
plt.legend()
plt.show()
