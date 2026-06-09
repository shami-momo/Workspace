import control
import matplotlib.pyplot as plt
import numpy as np

s = control.TransferFunction.s
H1 = (1 + 2.37*s) / (1 + 43.06*s) * 100 / (s * (s/5+1) * (s/50+1))

control.bode_plot(H1, dB=True)
#control.root_locus(H1)
plt.show()