import random
import math
import matplotlib.pyplot as plt

#設定particle數、iteration代數
n_p = 200
i_p = 100
x_min = 0.5
x_max = 50
y_min = 10
y_max = 200
w = 0.729
c1 = 1.49445
c2 = 1.49445
s_a = 14000
P = 50000
L = 500
l = 100


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
            after = now_x * now_y * l
            s = 6 * P * (L - n * l) / ((now_y ** 2) * now_x)
            if s > s_a:
                now_x = 50
                now_y = 200
                after = now_x * now_y * l
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(0)
            new_particle.append(0)
            new_particle.append(now_x)
            new_particle.append(now_y)
            new_particle.append(after)
        elif v_x > 0:
            for b in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                after = now_x * now_y * l
                s = 6 * P * (L - n * l) / ((now_y ** 2) * now_x)
                if s > s_a:
                    now_x = 50
                    now_y = 200
                    after = now_x * now_y * l
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                pbest_candidate.append(value)
                if now_x < x_min or now_y < y_min:
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
            for c in range(10):
                value = []
                value.append(now_x)
                value.append(now_y)
                after = now_x * now_y * l
                s = 6 * P * (L - n * l) / ((now_y ** 2) * now_x)
                if s > s_a:
                    now_x = 50
                    now_y = 200
                    after = now_x * now_y * l
                value.append(after)
                now_x += v_percent * v_x
                now_y += v_percent * v_y
                pbest_candidate.append(value)
                if now_x < x_min or now_y < y_min:
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
    # print('[', gbest_x, ',', gbest_y, ']:', gbest_value)
    gbest_loc = []
    gbest_loc.append(gbest_x)
    gbest_loc.append(gbest_y)
    gbest_loc.append(gbest_value)
    for i in new_swarm:
        rand_p = random.random()
        rand_g = random.random()
        v_x = i[2] * w + c1 * rand_p * (i[4] - i[0]) + c2 * rand_g * (gbest_x - i[0])
        v_y = i[3] * w + c1 * rand_p * (i[5] - i[1]) + c2 * rand_g * (gbest_y - i[1])
        i[2] = v_x
        i[3] = v_y
    return new_swarm, gbest_value, gbest_loc

v = 0
n = 0
v_total = []
for number in range(0, 100):
    v_total.append(0)

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
gbest_loc_list = []
gbest_list = []
for i in range(i_p):
    # print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for i in swv:
        swarm.append(i)
total_best = min(gbest_loc_list, key=lambda x: x[2])[2]
total_best_loc = [x for x in gbest_loc_list if x[2] == total_best]
print('b1:', total_best_loc[0][0], ', h1:', total_best_loc[0][1], ', volume1:', total_best_loc[0][2])

v += total_best_loc[0][2]

for number in range(0, 100):
    v_total[number] += gbest_list[number]

# plt.plot(gbest_list)
# plt.title('Global Best Value per Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Global Best Value')
# plt.show()

n = 1
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
gbest_loc_list = []
gbest_list = []
for i in range(i_p):
    # print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for i in swv:
        swarm.append(i)
total_best = min(gbest_loc_list, key=lambda x: x[2])[2]
total_best_loc = [x for x in gbest_loc_list if x[2] == total_best]
print('b2:', total_best_loc[0][0], ', h2:', total_best_loc[0][1], ', volume2:', total_best_loc[0][2])

v += total_best_loc[0][2]

for number in range(0, 100):
    v_total[number] += gbest_list[number]

# plt.plot(gbest_list)
# plt.title('Global Best Value per Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Global Best Value')
# plt.show()

n = 2
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
gbest_loc_list = []
gbest_list = []
for i in range(i_p):
    # print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for i in swv:
        swarm.append(i)
total_best = min(gbest_loc_list, key=lambda x: x[2])[2]
total_best_loc = [x for x in gbest_loc_list if x[2] == total_best]
print('b3:', total_best_loc[0][0], ', h3:', total_best_loc[0][1], ', volume3:', total_best_loc[0][2])

v += total_best_loc[0][2]

for number in range(0, 100):
    v_total[number] += gbest_list[number]

# plt.plot(gbest_list)
# plt.title('Global Best Value per Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Global Best Value')
# plt.show()

n = 3
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
gbest_loc_list = []
gbest_list = []
for i in range(i_p):
    # print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for i in swv:
        swarm.append(i)
total_best = min(gbest_loc_list, key=lambda x: x[2])[2]
total_best_loc = [x for x in gbest_loc_list if x[2] == total_best]
print('b4:', total_best_loc[0][0], ', h4:', total_best_loc[0][1], ', volume4:', total_best_loc[0][2])

v += total_best_loc[0][2]

for number in range(0, 100):
    v_total[number] += gbest_list[number]

# plt.plot(gbest_list)
# plt.title('Global Best Value per Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Global Best Value')
# plt.show()

n = 4
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
gbest_loc_list = []
gbest_list = []
for i in range(i_p):
    # print(i + 1)
    swf = fitness(swarm)
    swv, gbest, gbest_loc = velo(swf)
    gbest_list.append(gbest)
    gbest_loc_list.append(gbest_loc)
    swarm.clear()
    for i in swv:
        swarm.append(i)
total_best = min(gbest_loc_list, key=lambda x: x[2])[2]
total_best_loc = [x for x in gbest_loc_list if x[2] == total_best]
print('b5:', total_best_loc[0][0], ', h5:', total_best_loc[0][1], ', volume5:', total_best_loc[0][2])

v += total_best_loc[0][2]

for number in range(0, 100):
    v_total[number] += gbest_list[number]

# plt.plot(gbest_list)
# plt.title('Global Best Value per Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Global Best Value')
# plt.show()

print('volume:', v)

plt.plot(v_total)
plt.title('Global Best Value per Iteration')
plt.xlabel('Iteration')
plt.ylabel('Global Best Value')
plt.show()