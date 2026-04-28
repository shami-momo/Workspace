import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 14,
    "figure.dpi": 300,
    "axes.labelsize": 16,
    "axes.titlesize": 18
})

# 궤도 및 물리 상수
a, e, mu = 1.0, 0.5, 1.0
omega = np.radians(45) 
i = np.radians(30)  # 경사각
h = np.sqrt(mu * a * (1 - e**2))
p = a * (1 - e**2)

# 변수 범위 (Degree 단위)
f_deg = np.linspace(0, 360, 1000)
phi_deg = np.linspace(0, 360, 1000) # T와 N 사이의 각도
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

# dOmega/dt 계산 (T = cos(PHI), N = sin(PHI))
# r = p / (1 + e*cos(f))
R_dist = p / (1 + e * np.cos(F))
dOmega_dt = (R_dist * np.sin(omega + F) / (h * np.sin(i))) * np.sin(PHI)

# 최대치 기준 정규화
dOmega_dt_max = np.max(np.abs(dOmega_dt))
dOmega_dt_scaled = dOmega_dt / dOmega_dt_max if dOmega_dt_max != 0 else dOmega_dt

u_peak_1 = np.arccos(-e * np.cos(omega))
u_peak_2 = 2 * np.pi - u_peak_1

f_peak_1 = (u_peak_1 - omega) % (2 * np.pi)
f_peak_2 = (u_peak_2 - omega) % (2 * np.pi)

f_peak_1_deg = np.degrees(f_peak_1)
f_peak_2_deg = np.degrees(f_peak_2)

peaks_f = [f_peak_1_deg, f_peak_1_deg, f_peak_2_deg, f_peak_2_deg]
peaks_phi = [90, 270, 90, 270]

# 그래프 생성
plt.figure(figsize=(13, 9))

# 발산형 컬러맵(RdBu_r) 사용
plt.pcolormesh(f_deg, phi_deg, dOmega_dt_scaled, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of Longitude of Ascending Node $\dot{\Omega}/\dot{\Omega}_{\max}$', rotation=270, labelpad=25)

for pf, pphi in zip(peaks_f, peaks_phi):
    val = ( (p / (1 + e * np.cos(np.radians(pf)))) * np.sin(np.radians(pf) + omega) / (h * np.sin(i)) ) * np.sin(np.radians(pphi))
    val_norm = val / np.max(np.abs(dOmega_dt))
    
    label = "Max" if val_norm > 0 else "Min"
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white')
    plt.annotate(f"{label}\n({pf:.1f}, {pphi})", (pf, pphi), 
                 textcoords="offset points", xytext=(0,15), ha='center', 
                 fontsize=12, fontweight='bold', color='black',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))


plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{\Omega}$ for $e=0.5, \omega=45^\circ$, $i=30^\circ$')

# 보조선 추가 (순수 Normal 방향 강조)
plt.axhline(90, color='black', linestyle=':', alpha=0.3)
plt.axhline(270, color='black', linestyle=':', alpha=0.3) 
plt.tight_layout()
plt.savefig('doomega_dt_scaled_heatmap.png')