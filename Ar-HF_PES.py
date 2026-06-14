#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import psi4
import matplotlib.pyplot as plt

file_out = "Ar-HF_PES.out"
file_results = "Ar-HF_PES.txt"
file_plot = "Ar-HF_PES.pdf"

psi4.set_output_file(file_out)
psi4.set_options({
    "basis": "aug-cc-pVTZ",
    "e_convergence": 1e-10,
    "d_convergence": 1e-10
    })

HF_masses = psi4.geometry("""
  H
  F 1 1.0
""")
mH = HF_masses.mass(0)
mF = HF_masses.mass(1)

ArHF_template = r"""
    X
    Ar 1 {R}
    --
    H 1 {rH} 2 {theta}
    F 1 {rF} 3 180.0 2 180.0
"""

r = 0.917 # Å
R = 3.435 # Å
rH = mH * r / (mH + mF)
rF = r - rH
thetas = np.linspace(0, 180, 11)

Eints = []
for theta in thetas:
    ArHF = psi4.geometry(ArHF_template.format(R=R, rH=rH, rF=rF, theta=theta))
    Eint_HF = psi4.energy("scf", bsse_type="cp", molecule=ArHF)
    Eint_MP2 = psi4.energy("mp2", bsse_type="cp", molecule=ArHF)
    Eints.append([Eint_HF, Eint_MP2])

col_name_angles = "theta / °"
col_name_HF = "Eint_HF/ au"
col_name_MP2 = "Eint_MP2 / au"
ArHF_PES = pd.DataFrame(Eints, index=thetas)
ArHF_PES.reset_index(inplace=True)
ArHF_PES.columns = [col_name_angles, col_name_HF, col_name_MP2]
ArHF_PES.to_csv(file_results, sep="\t")

angles = ArHF_PES[col_name_angles]
Eints_MP2 = ArHF_PES[col_name_MP2]
angle_min = angles.min()
angle_max = angles.max()
Eint_MP2_min = Eints_MP2.min()
angle_min_plot = angle_min
angle_max_plot = 120
Eint_min_plot = 1.2 * Eint_MP2_min
Eint_max_plot = -2 * Eint_MP2_min
ax = ArHF_PES.plot.scatter(x=col_name_angles, y=col_name_MP2)
ax.set_xlim(angle_min_plot, angle_max_plot)
ax.set_ylim(Eint_min_plot, Eint_max_plot)
plt.rcParams["text.usetex"] = True
ax.set_xlabel(r"$\theta/\circ$")
ax.set_ylabel(r"$E_\mathrm{int}^\mathrm{MP2}/\mathrm{au}$")
cs = CubicSpline(angles, Eints_MP2)
angles_cs = np.linspace(angle_min, angle_max, 100)
ax.plot(angles_cs, cs(angles_cs))
plt.savefig(file_plot)
