import random
import math
import matplotlib.pyplot as plt

#設定particle數、iteration代數
n_p = 80
n_i = 100
x_min = -32.768
x_max = 32.768
y_min = -32.768
y_max = 32.768
z_min = -32.768
z_max = 32.768
a_min = -32.768
a_max = 32.768
b_min = -32.768
b_max = 32.768
w = 0.729
c1 = 1.49445
c2 = 1.49445
#以2維為例，對於每個particle來說，pbest與velocity記為[pbest_x, pbest_y, v_x, v_y]，再丟到swarm裡面
swarm = []

def initial_random():
    result_x = random.uniform(x_min, x_max)
    result_y = random.uniform(y_min, y_max)
    result_z = random.uniform(z_min, z_max)
    result_a = random.uniform(a_min, a_max)
    result_b = random.uniform(b_min, b_max)
    return result_x, result_y, result_z, result_a, result_b

#更新now_x, now_y, now_z, now_a, now_b, pbest_x, pbest_y, pbest_z, pbest_a, pbest_b, pbest_value
#v_x, v_y, v_z, v_a, v_b尚未改動
#swarm的list內有對應每個particle的inner list[now_x, now_y, now_z, now_a, now_b, v_x, v_y, v_z, v_a, v_b, pbest_x, best_y, pbest_z, pbest_a, pbest_b, pbest_value]
def fitness(swarm):
    new_swarm = []
    for i in swarm:
        start_x = i[0]
        start_y = i[1]
        start_z = i[2]
        start_a = i[3]
        start_b = i[4]
        v_x = i[5]
        v_y = i[6]
        v_z = i[7]
        v_a = i[8]
        v_b = i[9]
        v_percent = 0.1
        now_x = start_x
        now_y = start_y
        now_z = start_z
        now_a = start_a
        now_b = start_b
        pbest_candidate = []
        if v_x == 0 and v_y == 0 and v_z == 0 and v_a == 0 and v_b == 0:
            new_particle = []
            a = 20
            b = 0.2
            c = 2 * math.pi
            sum1 = now_x ** 2 + now_y ** 2 + now_z ** 2 + now_a ** 2 + now_b ** 2
            sum2 = math.cos(c * now_x) + math.cos(c * now_y) + math.cos(c * now_z) + math.cos(c * now_a) + math.cos(c * now_b)
            after = -a * (math.e ** (-b * ((sum1 / 5) ** 0.5))) - (math.e ** (sum2 / 5)) + a + math.e
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(now_z)
            new_particle.append(now_a)
            new_particle.append(now_b)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(now_z)
            new_particle.append(now_a)
            new_particle.append(now_b)
            new_particle.append(after)
        elif v_x > 0:
            for num in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                value.append(now_z)
                value.append(now_a)
                value.append(now_b)
                a = 20
                b = 0.2
                c = 2 * math.pi
                sum1 = now_x ** 2 + now_y ** 2 + now_z ** 2 + now_a ** 2 + now_b ** 2
                sum2 = math.cos(c * now_x) + math.cos(c * now_y) + math.cos(c * now_z) + math.cos(c * now_a) + math.cos(
                    c * now_b)
                after = -a * (math.e ** (-b * ((sum1 / 5) ** 0.5))) - (math.e ** (sum2 / 5)) + a + math.e
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                now_z += v_percent * v_z
                now_a += v_percent * v_a
                now_b += v_percent * v_b
                pbest_candidate.append(value)
                if now_x < x_min or now_x > x_max or now_y < y_min or now_y > y_max or now_z < z_min or now_z > z_max or now_a < a_min or now_a > a_max or now_b < b_min or now_b > b_max:
                    break
            now_x = now_x - v_percent * v_x
            now_y = now_y - v_percent * v_y
            now_z = now_z - v_percent * v_z
            now_a = now_a - v_percent * v_a
            now_b = now_b - v_percent * v_b
            smallest_sixth_item = min(pbest_candidate, key=lambda x: x[5])[5]
            new = [x for x in pbest_candidate if x[5] == smallest_sixth_item]
            pbest_x = new[0][0]
            pbest_y = new[0][1]
            pbest_z = new[0][2]
            pbest_a = new[0][3]
            pbest_b = new[0][4]
            pbest_value = new[0][5]
            new_particle = []
            if pbest_value < i[15]:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(now_z)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(v_z)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(pbest_x)
                new_particle.append(pbest_y)
                new_particle.append(pbest_z)
                new_particle.append(pbest_a)
                new_particle.append(pbest_b)
                new_particle.append(pbest_value)
            else:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(now_z)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(v_z)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(i[10])
                new_particle.append(i[11])
                new_particle.append(i[12])
                new_particle.append(i[13])
                new_particle.append(i[14])
                new_particle.append(i[15])
        else:
            for num in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                value.append(now_z)
                value.append(now_a)
                value.append(now_b)
                a = 20
                b = 0.2
                c = 2 * math.pi
                sum1 = now_x ** 2 + now_y ** 2 + now_z ** 2 + now_a ** 2 + now_b ** 2
                sum2 = math.cos(c * now_x) + math.cos(c * now_y) + math.cos(c * now_z) + math.cos(c * now_a) + math.cos(
                    c * now_b)
                after = -a * (math.e ** (-b * ((sum1 / 5) ** 0.5))) - (math.e ** (sum2 / 5)) + a + math.e
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                now_z += v_percent * v_z
                now_a += v_percent * v_a
                now_b += v_percent * v_b
                pbest_candidate.append(value)
                if now_x < x_min or now_x > x_max or now_y < y_min or now_y > y_max or now_z < z_min or now_z > z_max or now_a < a_min or now_a > a_max or now_b < b_min or now_b > b_max:
                    break
            now_x = now_x - v_percent * v_x
            now_y = now_y - v_percent * v_y
            now_z = now_z - v_percent * v_z
            now_a = now_a - v_percent * v_a
            now_b = now_b - v_percent * v_b
            smallest_sixth_item = min(pbest_candidate, key=lambda x: x[5])[5]
            new = [x for x in pbest_candidate if x[5] == smallest_sixth_item]
            pbest_x = new[0][0]
            pbest_y = new[0][1]
            pbest_z = new[0][2]
            pbest_a = new[0][3]
            pbest_b = new[0][4]
            pbest_value = new[0][5]
            new_particle = []
            if pbest_value < i[15]:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(now_z)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(v_z)
                new_particle.append(v_a)
                new_particle.append(v_b)
                new_particle.append(pbest_x)
                new_particle.append(pbest_y)
                new_particle.append(pbest_z)
                new_particle.append(pbest_a)
                new_particle.append(pbest_b)
                new_particle.append(pbest_value)

            else:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(now_z)
                new_particle.append(now_a)
                new_particle.append(now_b)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(v_z)
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

#更新v_x, v_y, v_z, v_a, v_b
def velo(new_swarm):
    gbest_value = min(new_swarm, key=lambda x: x[15])[15]
    new = [x for x in new_swarm if x[15] == gbest_value]
    gbest_x = new[0][10]
    gbest_y = new[0][11]
    gbest_z = new[0][12]
    gbest_a = new[0][13]
    gbest_b = new[0][14]
    print('[', gbest_x, ',', gbest_y, ',', gbest_z, ',', gbest_a, ',', gbest_b, ']: ', gbest_value)
    for i in new_swarm:
        rand_p = random.random()
        rand_g = random.random()
        v_x = i[5] * w + c1 * rand_p * (i[10] - i[0]) + c2 * rand_g * (gbest_x - i[0])
        v_y = i[6] * w + c1 * rand_p * (i[11] - i[1]) + c2 * rand_g * (gbest_y - i[1])
        v_z = i[7] * w + c1 * rand_p * (i[12] - i[2]) + c2 * rand_g * (gbest_z - i[2])
        v_a = i[8] * w + c1 * rand_p * (i[13] - i[3]) + c2 * rand_g * (gbest_a - i[3])
        v_b = i[9] * w + c1 * rand_p * (i[14] - i[4]) + c2 * rand_g * (gbest_b - i[4])
        i[5] = v_x
        i[6] = v_y
        i[7] = v_z
        i[8] = v_a
        i[9] = v_b
    return new_swarm, gbest_value

#初始位置
#swarm的list內有對應每個particle的inner list[now_x, now_y, v_x, v_y]
for i in range(n_p):
    particle = []
    result_x, result_y, result_z, result_a, result_b = initial_random()
    particle.append(result_x)
    particle.append(result_y)
    particle.append(result_z)
    particle.append(result_a)
    particle.append(result_b)
    v_x_initial = 0
    v_y_initial = 0
    v_z_initial = 0
    v_a_initial = 0
    v_b_initial = 0
    particle.append(v_x_initial)
    particle.append(v_y_initial)
    particle.append(v_z_initial)
    particle.append(v_a_initial)
    particle.append(v_b_initial)
    particle.append(result_x)
    particle.append(result_y)
    particle.append(result_z)
    particle.append(result_a)
    particle.append(result_b)
    particle.append(0)
    swarm.append(particle)
#print("original")
#print(swarm)

#iteration
gbest_list = []
for i in range(n_i):
    print(i + 1)
    swf = fitness(swarm)
    #print(swf)
    swv, gbest = velo(swf)
    gbest_list.append(gbest)
    #print(swv)
    swarm.clear()
    for i in swv:
        swarm.append(i)

plt.plot(gbest_list)
plt.title('Global Best Value per Iteration')
plt.xlabel('Iteration')
plt.ylabel('Global Best Value')
plt.show()