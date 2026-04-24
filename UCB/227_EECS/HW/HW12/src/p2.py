import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# Problem data (Table 1)
x = np.array([0, 4, 8, 12, 16, 20, 24])
y = np.array([4, 5, 4, 6, 8, 7, 4])
c = np.array([None, 3, 2, 1, 2, 2, None], dtype=object)

n = 5  # number of gates

# Decision variables (crossing heights)
z = cp.Variable(n)

# Segment lengths
t = cp.Variable(n+1)

constraints = []

# Gate constraints
for i in range(1, n+1):
    constraints += [
        z[i-1] >= y[i] - c[i]/2,
        z[i-1] <= y[i] + c[i]/2
    ]

# Full vector including start/end
z_full = cp.hstack([y[0], z, y[-1]])

# SOCP constraints for path segments
for i in range(n+1):
    dx = x[i+1] - x[i]
    dy = z_full[i+1] - z_full[i]
    constraints.append(cp.norm(cp.hstack([dx, dy]), 2) <= t[i])

# Objective: minimize total path length
objective = cp.Minimize(cp.sum(t))

problem = cp.Problem(objective, constraints)
problem.solve()

print("Optimal path length:", problem.value)
print("Optimal crossing heights:", z.value)

# Build full path
z_opt = np.hstack([y[0], z.value, y[-1]])

# Plot
plt.figure(figsize=(8,4))

# Plot gates
for i in range(1, n+1):
    plt.plot([x[i], x[i]], [y[i]-c[i]/2, y[i]+c[i]/2], 'k', linewidth=4)

# Plot path
plt.plot(x, z_opt, '-o', label="Optimal path")

# Plot gate centers
plt.plot(x, y, '--', label="Gate centers")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Optimal Slalom Path")
# save to the 'figs' directory
plt.savefig("figs/slalom_path.png")
plt.show()