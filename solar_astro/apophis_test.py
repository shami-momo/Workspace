import rebound
import numpy as np 
import matplotlib.pyplot as plt

sim = rebound.Simulation()
sim.units = ('days', 'AU', 'Msun')
sim.add(["Sun", "Earth", "NAME = Apophis"], date="2029-04-12 00:00")

sim.move_to_com()

total_time = 3 
times = np.linspace(0, total_time, 1000)

x_rel, y_rel = [], []

for t in times:
    sim.integrate(t)

    earth = sim.particles[1]
    apophis = sim.particles[2]

    theta = np.arctan2(earth.y, earth.x)
    
    dx = apophis.x - earth.x
    dy = apophis.y - earth.y
    
    x_rot = dx * np.cos(theta) + dy * np.sin(theta)
    y_rot = -dx * np.sin(theta) + dy * np.cos(theta)
    
    x_rel.append(x_rot)
    y_rel.append(y_rot)

plt.figure(figsize=(8, 8))

plt.plot(x_rel, y_rel, label='Apophis', color='orange', lw=1.5, alpha=0.8)
plt.scatter([0], [0], color='red', s=100, label='Earth', marker='*')  # Earth at the origin

plt.xlabel("x (AU)")
plt.ylabel("y (AU)")
plt.title("Orbit of Apophis Relative to Earth")
plt.legend(loc='upper right')
plt.axis("equal")

plt.show()
