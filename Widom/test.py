import numpy as np


R = 8.31446261815324 #J / (K mol)
T = 300 # K

S = 2.51 * 10**(-6) * np.exp(-6700/(R*T)) #mol L^-1 Pa^-1

# S = 10**(-7)

# 1 mole ideal gas = 22.414 L at STP

S = 22.414*S # L (STP) L^-1 Pa^-1 == cm^3 (STP) cm^(-3) Pa^(-1)

K = S*T*101325/273.15

print(K) # 0.326

# S = 22.414 * 2.51 * 10**(-6) * np.exp(-6700/(R*T)) * 101325/275.15 * T

dE = -3720 #J/mol; R is in J / K / mol
