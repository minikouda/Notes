from random import uniform


T = 100000

res = []

for _ in range(T):
    a, b = uniform(0,1), uniform(0,1)
    if max(a,b) > 1 / 2:
        res.append(max(a,b))
    else:
        res.append(0.5)

print(sum(res) / len(res))
print(2 / 3 + 1 / 12)
