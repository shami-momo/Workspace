import rebound
import matplotlib.pyplot as plt
import numpy as np

# 1. 시뮬레이션 초기화 (단위: 일, AU, 태양 질량)
sim = rebound.Simulation()
sim.units = ('days', 'AU', 'Msun')

# NASA Horizons에서 1977년 발사 직후의 데이터를 불러와
# -32는 보이저 2호의 고유 번호야
print("데이터를 불러오는 중... 시간이 조금 걸릴 수 있어!")
bodies = ["Sun", "Jupiter", "Saturn", "Uranus", "Neptune", "Voyager 2"]
sim.add(bodies, date="1977-08-21 00:00")

# 질량 중심 보정 및 보이저호를 테스트 입자로 설정
sim.move_to_com()
sim.particles[-1].m = 0 # 보이저호는 행성에 영향을 주지 않음

# 2. 시뮬레이션 설정 (약 12년, 4500일)
total_days = 10000
times = np.linspace(0, total_days, 2000)

distances = []
velocities = []
trajectories = [[] for _ in range(len(bodies))]

# 3. 적분 수행
print("시뮬레이션 시작!")
for t in times:
    sim.integrate(t)
    
    # 태양 중심 속도와 위치 저장
    sun = sim.particles[0]
    v2 = sim.particles[-1]
    
    # 태양 중심 거리 r과 속도 v 계산
    r = np.sqrt((v2.x-sun.x)**2 + (v2.y-sun.y)**2 + (v2.z-sun.z)**2)
    v = np.sqrt((v2.vx-sun.vx)**2 + (v2.vy-sun.vy)**2 + (v2.vz-sun.vz)**2)
    
    distances.append(r)
    velocities.append(v)
    
    for i, p in enumerate(sim.particles):
        trajectories[i].append([p.x, p.y])

# 4. 결과 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# 왼쪽: 전체 궤적 평면도
for i, name in enumerate(bodies):
    traj = np.array(trajectories[i])
    if name == "-32":
        ax1.plot(traj[:,0], traj[:,1], label='Voyager 2', color='black', lw=2, zorder=10)
    else:
        ax1.plot(traj[:,0], traj[:,1], label=name, alpha=0.5)

ax1.set_title("Voyager 2 Trajectory")
ax1.set_xlabel("x [AU]")
ax1.set_ylabel("y [AU]")
ax1.legend()
ax1.axis('equal')
ax1.grid(True)

# 오른쪽: 시간에 따른 태양 중심 속도 변화 (중력 도움 확인)
# 속도 단위를 AU/day에서 km/s로 변환 (1 AU/day ≈ 1731.46 km/s)
v_kms = np.array(velocities) * 1731.46
ax2.plot(times / 365.25, v_kms, color='blue', lw=1.5)
ax2.set_title("Voyager 2 Velocity Profile (Heliocentric)")
ax2.set_xlabel("Years since launch")
ax2.set_ylabel("Velocity [km/s]")
ax2.grid(True)

plt.tight_layout()
plt.show()