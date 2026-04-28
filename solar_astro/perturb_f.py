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
phi_deg = np.linspace(0, 360, 1000)
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

R_dist = p / (1 + e * np.cos(F))
df_dt = (1 / (e * h)) * (p * np.cos(F) * np.cos(PHI) - (p + R_dist) * np.sin(F) * np.sin(PHI))

df_dt_max = np.max(np.abs(df_dt))
df_dt_scaled = df_dt / df_dt_max if df_dt_max != 0 else df_dt

# 그래프 생성
plt.figure(figsize=(13, 9))

# 발산형 컬러맵(RdBu_r)으로 확장(+)과 축소(-) 시각화
plt.pcolormesh(f_deg, phi_deg, df_dt_scaled, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of True Anomaly $\dot{f}/\dot{f}_{\max}$', rotation=270, labelpad=25)

plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{f}$ for $e=0.5$')

# === 여기서부터 추가된 부분: Max / Min 지점 표시 (Pure Numpy) ===
# df/dt의 크기를 결정하는 함수를 최대화하는 f 정밀 탐색 (domega/dt와 극점 위치 동일!)
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
    
    # df/dt는 domega/dt와 R, T 성분 부호가 반대!
    # A*cos(phi) + B*sin(phi) 꼴에서 B성분에 마이너스가 붙음
    phi_max = np.arctan2(-(p + r_val) * np.sin(f_val), p * np.cos(f_val))
    
    # Max 포인트 (phi_max)와 Min 포인트 (phi_max + 180도) 저장
    peaks_f.extend([np.degrees(f_val), np.degrees(f_val)])
    peaks_phi.extend([np.degrees(phi_max % (2 * np.pi)), np.degrees((phi_max + np.pi) % (2 * np.pi))])

for pf, pphi in zip(peaks_f, peaks_phi):
    F_val = np.radians(pf)
    PHI_val = np.radians(pphi)
    
    R_val = p / (1 + e * np.cos(F_val))
    val = (1 / (e * h)) * (p * np.cos(F_val) * np.cos(PHI_val) - (p + R_val) * np.sin(F_val) * np.sin(PHI_val))
    
    # 0보다 크면 Max, 작으면 Min!
    label = "Max" if val > 0 else "Min"
    
    # 별 마커 표시 (zorder로 제일 위로 끌어올림)
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white', zorder=5)
    
    # 텍스트 라벨 추가
    plt.annotate(f"{label}\n({pf:.1f}, {pphi:.1f})", (pf, pphi), 
                 textcoords="offset points", xytext=(0, 15), ha='center', 
                 fontsize=12, fontweight='bold', color='black', zorder=6,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 보조선 추가 (순수 Transverse 방향 강조)
plt.axhline(90, color='black', linestyle=':', alpha=0.3)
plt.axhline(270, color='black', linestyle=':', alpha=0.3)
plt.tight_layout()
plt.savefig('df_dt_scaled_heatmap.png')