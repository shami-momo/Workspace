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
h = np.sqrt(mu * a * (1 - e**2))
coeff = (2 * a**2) / h

# 변수 범위 (Degree 단위)
f_deg = np.linspace(0, 360, 1000)
phi_deg = np.linspace(0, 360, 1000)
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

# da/dt 계산
da_dt = coeff * (e * np.sin(F) * np.cos(PHI) + (1 + e * np.cos(F)) * np.sin(PHI))
da_dt_max = np.max(np.abs(da_dt))
da_dt_scaled = da_dt / da_dt_max if da_dt_max != 0 else da_dt

# 그래프
plt.figure(figsize=(13, 9))
plt.pcolormesh(f_deg, phi_deg, da_dt_scaled, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of Semi-major Axis $\dot{a}/\dot{a}_{\max}$', rotation=270, labelpad=25)

plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{a}$ for $e=0.5$')

# 보조선 추가 (최대 효율 지점 강조)
plt.axhline(90, color='black', linestyle=':', alpha=0.3)
plt.axhline(270, color='black', linestyle=':', alpha=0.3)

# Max / Min 지점 표시
peaks_f = [0, 360, 0, 360]
peaks_phi = [90, 90, 270, 270]

for pf, pphi in zip(peaks_f, peaks_phi):
    val = coeff * (e * np.sin(np.radians(pf)) * np.cos(np.radians(pphi)) + 
                   (1 + e * np.cos(np.radians(pf))) * np.sin(np.radians(pphi)))
    
    label = "Max" if val > 0 else "Min"
    
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white')
    
    # 텍스트 라벨 추가
    plt.annotate(f"{label}\n({pf}, {pphi})", (pf, pphi), 
                 textcoords="offset points", xytext=(0, 15), ha='center', 
                 fontsize=12, fontweight='bold', color='black',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('da_dt_scaled_heatmap.png')