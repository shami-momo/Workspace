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
p = a * (1 - e**2)

# 변수 범위 (Degree 단위)
f_deg = np.linspace(0, 360, 1000)
phi_deg = np.linspace(0, 360, 1000) # T와 N 사이의 각도
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

# domega/dt 계산 (T = cos(PHI), N = sin(PHI))
# r = p / (1 + e*cos(f))
R_dist = p / (1 + e * np.cos(F))
domega_dt = (1 / (e * h)) * (-p * np.cos(F) * np.cos(PHI) + (p + R_dist) * np.sin(F) * np.sin(PHI))
domega_dt_norm = domega_dt / np.max(np.abs(domega_dt))

# 그래프 생성
plt.figure(figsize=(13, 9))

# 발산형 컬러맵(RdBu_r) 사용
plt.pcolormesh(f_deg, phi_deg, domega_dt_norm, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of Argument of Periapsis $\dot{\omega}/\dot{\omega}_{\max}$', rotation=270, labelpad=25)

plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{\omega}$ for $e=0.5$')

# === 여기서부터 추가된 부분: Max / Min 지점 표시 (Pure Numpy) ===
# domega/dt의 크기를 결정하는 함수를 최대화하는 f 정밀 탐색
f_search = np.linspace(0, 2 * np.pi, 100000)
r_search = p / (1 + e * np.cos(f_search))
M2 = (p * np.cos(f_search))**2 + ((p + r_search) * np.sin(f_search))**2

# 궤도 대칭성을 이용해 0~180도, 180~360도 구간에서 각각 최대점 도출
mid_idx = len(f_search) // 2
f_peak1 = f_search[np.argmax(M2[:mid_idx])]
f_peak2 = f_search[mid_idx + np.argmax(M2[mid_idx:])]

peaks_f = []
peaks_phi = []

for f_val in [f_peak1, f_peak2]:
    r_val = p / (1 + e * np.cos(f_val))
    # 해당 f에서 변화율을 최대로 만드는 최적의 힘 방향 phi 계산
    phi_max = np.arctan2((p + r_val) * np.sin(f_val), -p * np.cos(f_val))
    
    # Max 포인트 (phi_max)와 Min 포인트 (phi_max + 180도) 저장
    peaks_f.extend([np.degrees(f_val), np.degrees(f_val)])
    peaks_phi.extend([np.degrees(phi_max % (2 * np.pi)), np.degrees((phi_max + np.pi) % (2 * np.pi))])

for pf, pphi in zip(peaks_f, peaks_phi):
    F_val = np.radians(pf)
    PHI_val = np.radians(pphi)
    
    R_val = p / (1 + e * np.cos(F_val))
    val = (1 / (e * h)) * (-p * np.cos(F_val) * np.cos(PHI_val) + (p + R_val) * np.sin(F_val) * np.sin(PHI_val))
    
    # 0보다 크면 Max, 작으면 Min!
    label = "Max" if val > 0 else "Min"
    
    # 별 마커 표시
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white', zorder=5)
    
    # 텍스트 라벨 추가 (소수점 첫째 자리까지 깔끔하게)
    plt.annotate(f"{label}\n({pf:.1f}, {pphi:.1f})", (pf, pphi), 
                 textcoords="offset points", xytext=(0, 15), ha='center', 
                 fontsize=12, fontweight='bold', color='black', zorder=6,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('domega_dt_scaled_heatmap.png')