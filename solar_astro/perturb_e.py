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
coeff = h / mu

# 변수 범위 (Degree 단위)
f_deg = np.linspace(0, 360, 1000)
phi_deg = np.linspace(0, 360, 1000)
F, PHI = np.meshgrid(np.radians(f_deg), np.radians(phi_deg))

# de/dt 계산 (R = cos(PHI), T = sin(PHI))
term_R = np.sin(F) * np.cos(PHI)
term_T = ((2 * np.cos(F) + e * (1 + np.cos(F)**2)) / (1 + e * np.cos(F))) * np.sin(PHI)
de_dt = coeff * (term_R + term_T)

# 최대치 기준 정규화
de_dt_max = np.max(np.abs(de_dt))
de_dt_scaled = de_dt / de_dt_max if de_dt_max != 0 else de_dt

# 그래프 생성
plt.figure(figsize=(13, 9))

# 발산형 컬러맵(RdBu_r)으로 확장(+)과 축소(-) 시각화
plt.pcolormesh(f_deg, phi_deg, de_dt_scaled, shading='auto', cmap='RdBu_r')
cbar = plt.colorbar()
cbar.set_label(r'Normalized Change Rate of Eccentricity $\dot{e}/\dot{e}_{\max}$', rotation=270, labelpad=25)

plt.xticks([0, 90, 180, 270, 360])
plt.yticks([0, 90, 180, 270, 360])
plt.xlabel(r'True Anomaly $f$ (deg)')
plt.ylabel(r'Perturbation Angle $\phi$ (deg)')
plt.title(r'$\dot{e}$ for $e=0.5$')

# === 여기서부터 추가된 부분: Max / Min 지점 표시 ===
# 이심률의 최대/최소 변화는 근점(0, 360)과 원점(180)에서 횡방향(90, 270)으로 힘을 줄 때 발생해!
peaks_f = [0, 180, 360, 0, 180, 360]
peaks_phi = [90, 270, 90, 270, 90, 270]

for pf, pphi in zip(peaks_f, peaks_phi):
    F_val = np.radians(pf)
    PHI_val = np.radians(pphi)
    
    t_R = np.sin(F_val) * np.cos(PHI_val)
    t_T = ((2 * np.cos(F_val) + e * (1 + np.cos(F_val)**2)) / (1 + e * np.cos(F_val))) * np.sin(PHI_val)
    val = coeff * (t_R + t_T)
    
    # 0보다 크면 Max, 작으면 Min!
    label = "Max" if val > 0 else "Min"
        
    # 별 모양 마커 추가
    plt.scatter(pf, pphi, color='black', marker='*', s=300, edgecolor='white')
    
    # 텍스트 라벨 달아주기
    plt.annotate(f"{label}\n({pf}, {pphi})", (pf, pphi), 
                 textcoords="offset points", xytext=(0, 15), ha='center', 
                 fontsize=12, fontweight='bold', color='black',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))


# 보조선 추가 (순수 Transverse 방향 강조)
plt.axhline(90, color='black', linestyle=':', alpha=0.3)
plt.axhline(270, color='black', linestyle=':', alpha=0.3)
plt.tight_layout()
plt.savefig('de_dt_scaled_heatmap.png')