import numpy as np
import matplotlib.pyplot as plt
import control as ct

# Transfer function:
# L(s) = (s^2 + 2s + 1) / [s (s+20)^2 (s^2 - 2s + 2)]

s = ct.TransferFunction.s

L = 10 / (s*(s+2))

print("L(s) =")
print(L)

# Frequency range
w = np.logspace(-3, 3, 3000)

# -------------------------
# Bode plot
# -------------------------
mag, phase, omega = ct.bode(L, w, dB=True, deg=True, plot=False)

plt.figure(figsize=(8, 6))

plt.subplot(2, 1, 1)
plt.semilogx(omega, 20 * np.log10(mag))
plt.grid(True, which="both")
plt.ylabel("Magnitude (dB)")
plt.title("Bode Plot of L(s)")

plt.subplot(2, 1, 2)
plt.semilogx(omega, phase * 180 / np.pi)
plt.grid(True, which="both")
plt.ylabel("Phase (deg)")
plt.xlabel("Frequency (rad/s)")

plt.tight_layout()
plt.show()

# -------------------------
# Nyquist plot
# -------------------------
plt.figure(figsize=(6, 6))

# control built-in nyquist
ct.nyquist_plot(L, omega=w)

plt.grid(True)
plt.axis("equal")
plt.title("Nyquist Plot of L(s)")
plt.legend()
plt.show()