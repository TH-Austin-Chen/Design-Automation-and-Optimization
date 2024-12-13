import random
import math
import matplotlib.pyplot as plt

#設定particle數、iteration代數
n_p = 20
i_p = 50
x_min = -10
x_max = 10
y_min = -10
y_max = 10
w = 0.729
c1 = 1.49445
c2 = 1.49445

swarm = []

def initial_random():
    result_x = random.uniform(x_min, x_max)
    result_y = random.uniform(y_min, y_max)
    return result_x, result_y

#更新now_x, now_y, pbest_x, pbest_y, pbest_value
#v_x, v_y尚未改動
#swarm的list內有對應每個particle的inner list[now_x, now_y, v_x, v_y, pbest_x, best_y, pbest_value]
def fitness(swarm):
    new_swarm = []
    for i in swarm:
        start_x = i[0]
        start_y = i[1]
        v_x = i[2]
        v_y = i[3]
        v_percent = 0.1
        now_x = start_x
        now_y = start_y
        pbest_candidate = []
        if v_x == 0 and v_y == 0:
            new_particle = []
            sum1 = 0
            sum2 = 0
            for n in range(1, 6):
                sum1 += n * math.cos((n + 1) * now_x + n)
                # print(sum1)
                sum2 += n * math.cos((n + 1) * now_y + n)
                # print(sum2)
            after = sum1 * sum2
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(after)
        elif v_x > 0:
            for n in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                sum1 = 0
                sum2 = 0
                for n in range(1, 6):
                    sum1 += n * math.cos((n + 1) * now_x + n)
                    sum2 += n * math.cos((n + 1) * now_y + n)
                after = sum1 * sum2
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                pbest_candidate.append(value)
                if now_x < x_min or now_x > x_max or now_y < y_min or now_y > y_max:
                    break
            now_x = now_x - v_percent * v_x
            now_y = now_y - v_percent * v_y
            smallest_third_item = min(pbest_candidate, key=lambda x: x[2])[2]
            new = [x for x in pbest_candidate if x[2] == smallest_third_item]
            pbest_x = new[0][0]
            pbest_y = new[0][1]
            pbest_value = new[0][2]
            new_particle = []
            if pbest_value < i[6]:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(pbest_x)
                new_particle.append(pbest_y)
                new_particle.append(pbest_value)
            else:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(i[4])
                new_particle.append(i[5])
                new_particle.append(i[6])
        else:
            for num in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                sum1 = 0
                sum2 = 0
                for n in range(1, 6):
                    sum1 += n * math.cos((n + 1) * now_x + n)
                    sum2 += n * math.cos((n + 1) * now_y + n)
                after = sum1 * sum2
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                pbest_candidate.append(value)
                if now_x < x_min or now_x > x_max or now_y < y_min or now_y > y_max:
                    break
            now_x = now_x - v_percent * v_x
            now_y = now_y - v_percent * v_y
            smallest_third_item = min(pbest_candidate, key=lambda x: x[2])[2]
            new = [x for x in pbest_candidate if x[2] == smallest_third_item]
            pbest_x = new[0][0]
            pbest_y = new[0][1]
            pbest_value = new[0][2]
            new_particle = []
            if pbest_value < i[6]:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(pbest_x)
                new_particle.append(pbest_y)
                new_particle.append(pbest_value)

            else:
                new_particle.append(now_x)
                new_particle.append(now_y)
                new_particle.append(v_x)
                new_particle.append(v_y)
                new_particle.append(i[4])
                new_particle.append(i[5])
                new_particle.append(i[6])
        new_swarm.append(new_particle)
    return new_swarm

#更新v_x, v_y
def velo(new_swarm):
    gbest_value = min(new_swarm, key=lambda x: x[6])[6]
    new = [x for x in new_swarm if x[6] == gbest_value]
    gbest_x = new[0][4]
    gbest_y = new[0][5]
    print('[', gbest_x, ',', gbest_y, ']:', gbest_value)
    for i in new_swarm:
        rand_p = random.random()
        rand_g = random.random()
        v_x = i[2] * w + c1 * rand_p * (i[4] - i[0]) + c2 * rand_g * (gbest_x - i[0])
        v_y = i[3] * w + c1 * rand_p * (i[5] - i[1]) + c2 * rand_g * (gbest_y - i[1])
        i[2] = v_x
        i[3] = v_y
    return new_swarm, gbest_value

#初始位置
for i in range(n_p):
    particle = []
    result_x, result_y = initial_random()
    particle.append(result_x)
    particle.append(result_y)
    v_x_initial = 0
    v_y_initial = 0
    particle.append(v_x_initial)
    particle.append(v_y_initial)
    particle.append(result_x)
    particle.append(result_y)
    particle.append(0)
    swarm.append(particle)
#print("original")
#print(swarm)

#iteration
gbest_list = []
for i in range(i_p):
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