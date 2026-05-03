import control as ct
import matplotlib.pyplot as plt

# zpk(zeros, poles, gain)
#zeros = [-1]
#poles = [0, 0, -9]
#gain = 1
#sys = ct.zpk(zeros, poles, gain)

num = [1, 1]
den = [1, 3, 12, -16, 0]
sys = ct.TransferFunction(num, den)

fig = plt.figure(figsize=(15, 8))

# Root Locus
ax_rl = fig.add_subplot(1, 2, 1)
ct.root_locus(sys, ax=ax_rl)
ax_rl.grid(True)
ax_rl.set_title("Root Locus")

# Bode plot
ax_mag = fig.add_subplot(2, 2, 2)
ax_phase = fig.add_subplot(2, 2, 4)
ct.bode_plot(sys, ax=[ax_mag, ax_phase], dB=True, deg=True)
ax_mag.grid(True, which='both')
ax_phase.grid(True, which='both')
ax_mag.set_title("Bode Plot")

plt.tight_layout()
plt.show()