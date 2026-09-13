import numpy as np
import matplotlib.pyplot as plt
#plt.rcParams['text.usetex'] = True

def f(M, e, E):
    return E - e * np.sin(E) - M

def df(e, E):
    return 1 - e * np.cos(E)

def solve_kepler(M, e, E0):
    E=E0
    E_list = [E] 

    for i in range(100):
        f_E = f(M, e, E)
        df_E = df(e, E)

        E_new = E - f_E / df_E 
        E_list.append(E_new)

        if abs(E_new - E) < 1e-5:
            E = E_new
            break

        E = E_new
    else:
        print("Not converged after 100 iterations.")
        return np.nan, E_list

    return E, E_list

def plot_kepler(M, e, E_list):
    E_range = np.linspace(min(E_list) - 0.5, max(E_list) + 0.5, 100)
    f_E = f(M, e, E_range)

    plt.plot(E_range, f_E, '--', color='c')
    plt.axhline(y=0, color='k')

    for i in range(len(E_list) - 1):
        plt.plot([E_list[i], E_list[i]], [0, f(M, e, E_list[i])], color='r')
        plt.plot([E_list[i], E_list[i+1]], [f(M, e, E_list[i]), 0], color='r')

    plt.xlabel("$E$")
    plt.ylabel("$f(E)$")
    plt.grid()
    plt.title(f"Newton-Raphson Method ($E_0={E_list[0]:.2f}$)")
    plt.show()

M = 2 * np.pi / 523.6 * (-145)
e = 0.88990
a = 1.2714
E0 = M

#final_E, E_list = solve_kepler(M, e, E0)

#print("--- Iteration process ---")
#for i, val in enumerate(E_list):
#    print(f"Step {i}: {val:.4f} rad")
#print(f"Numerical solution: {final_E:.4f} rad")

#plot_kepler(M, e, E_list)

t_list = np.linspace(0, 523.6, 100)
x_list = []
y_list = []

for t in t_list:
    M = (2 * np.pi / 523.6) * t
    E, _ = solve_kepler(M, e, E0=M) 
    
    cos_f = (np.cos(E) - e) / (1 - e * np.cos(E))
    ff = np.arccos(cos_f)
    
    if M > np.pi: 
        ff = ff * (-1)
        
    r_H = a * (1 - e * np.cos(E))
    
    x = r_H * np.cos(ff)
    y = r_H * np.sin(ff)
    
    x_list.append(x)
    y_list.append(y)

q = a * (1 - e) 

plt.annotate('Perihelion', 
             xy=(q, 0),            
             xytext=(q + 0.5, 0.5), 
             arrowprops=dict(arrowstyle='->', color='black'))
plt.plot(0, 0, 'o', color='orange', markersize=7, label='Sun')
plt.scatter(x_list, y_list, color='red', marker='+', label='3200 Phaethon')
plt.xlabel("X [AU]")
plt.ylabel("Y [AU]")
plt.axis('equal')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.show()