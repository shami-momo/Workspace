import numpy as np
import pandas as pd
from pyparsing import col

df = pd.read_csv('cp_re15e4_alfa_minus4.csv', sep=',', skiprows=1)
df.columns = ["xc", "yc", "Cp"]

df["surface"] = "Upper"
df.loc[df["yc"] < -1e-5, "surface"] = "Lower"
df.loc[np.abs(df["yc"]) <= 1e-5, "surface"] = "LE"

df_lower = df[df["surface"] == "Lower"].sort_values(by="xc", ascending=False)
df_le = df[df["surface"] == "LE"]
df_upper = df[df["surface"] == "Upper"].sort_values(by="xc", ascending=True)

df_seq = pd.concat([df_lower, df_le, df_upper]).reset_index(drop=True)

Q = 14367
CORDLENGTH = 0.15

aoa_deg = -4.0
aoa_rad = np.radians(aoa_deg)

c_a = 0.0
c_n = 0.0

for i in range(len(df_seq) - 1):
    cp_avg = (df_seq.loc[i, "Cp"] + df_seq.loc[i + 1, "Cp"]) / 2.0
    dxc = df_seq.loc[i + 1, "xc"] - df_seq.loc[i, "xc"]
    dyc = df_seq.loc[i + 1, "yc"] - df_seq.loc[i, "yc"]

    c_a += cp_avg * dyc
    c_n += -cp_avg * dxc

c_l = c_n * np.cos(aoa_rad) - c_a * np.sin(aoa_rad)
c_d = c_n * np.sin(aoa_rad) + c_a * np.cos(aoa_rad)

F_x = c_a * Q * CORDLENGTH
F_y = c_n * Q * CORDLENGTH
L_prime = c_l * Q * CORDLENGTH
D_prime = c_d * Q * CORDLENGTH

print(f"AOA = {aoa_deg} deg :")
print(f"  c_l = {c_l:.4f}")
print(f"  c_d = {c_d:.4f}")
print(f"  F_x = {F_x:.4f}")
print(f"  F_y = {F_y:.4f}")
print(f"  L'  = {L_prime:.4f}")
print(f"  D'  = {D_prime:.4f}")