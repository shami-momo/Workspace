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
h = np.sqrt(mu * a * (1 - e**2))
p = a * (1 - e**2)

# 변수 범위 (Degree 단위)
f_deg = np.linspace(0, 360, 1000)
phi_deg = np.linspace(0, 360, 1000) # T와 N 사이의 각도
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

# di/dt 계산 (T = cos(PHI), N = sin(PHI))
# r = p / (1 + e*cos(f))
R_dist = p / (1 + e * np.cos(F))
di_dt = (R_dist * np.cos(omega + F) / h) * np.sin(PHI)

# 최대치 기준 정규화
di_dt_max = np.max(np.abs(di_dt))
di_dt_scaled = di_dt / di_dt_max if di_dt_max != 0 else di_dt

# 그래프 생성
plt.figure(figsize=(13, 9))

# 발산형 컬러맵(RdBu_r) 사용
plt.pcolormesh(f_deg, phi_deg, di_dt_scaled, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of Inclination $\dot{i}/\dot{i}_{\max}$', rotation=270, labelpad=25)

plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{i}$ for $e=0.5, \omega=45^\circ$')

# === 여기서부터 추가된 부분: Max / Min 지점 표시 ===
# 궤도 경사각 변화율의 극값 조건: sin(w+f) = -e * sin(w)
sin_u = -e * np.sin(omega)
u1 = np.arcsin(sin_u)
u2 = np.pi - u1

# 진근점 이각 f로 변환
f1 = (u1 - omega) % (2 * np.pi)
f2 = (u2 - omega) % (2 * np.pi)

# 섭동력 각도는 순수 수직 방향인 90도, 270도
peaks_f = [np.degrees(f1), np.degrees(f1), np.degrees(f2), np.degrees(f2)]
peaks_phi = [90, 270, 90, 270]

for pf, pphi in zip(peaks_f, peaks_phi):
    F_val = np.radians(pf)
    PHI_val = np.radians(pphi)
    
    r_val = p / (1 + e * np.cos(F_val))
    val = (r_val * np.cos(omega + F_val) / h) * np.sin(PHI_val)
    
    # 0보다 크면 Max, 작으면 Min!
    label = "Max" if val > 0 else "Min"
    
    # 별 모양 마커 추가
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white', zorder=5)
    
    # 텍스트 라벨 달아주기 (소수점 첫째 자리까지)
    plt.annotate(f"{label}\n({pf:.1f}, {pphi})", (pf, pphi), 
                 textcoords="offset points", xytext=(0, 15), ha='center', 
                 fontsize=12, fontweight='bold', color='black', zorder=6,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 보조선 추가 (순수 Normal 방향 강조)
plt.axhline(90, color='black', linestyle=':', alpha=0.3) 
plt.axhline(270, color='black', linestyle=':', alpha=0.3)
plt.tight_layout()
plt.savefig('di_dt_scaled_heatmap.png')
plt.show()