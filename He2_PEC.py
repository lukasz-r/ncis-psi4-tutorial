#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import psi4
import matplotlib.pyplot as plt

file_out = "He2_PEC.out"
file_results = "He2_PEC.txt"
file_plot = "He2_PEC.pdf"

psi4.set_output_file(file_out)
distances = np.arange(2, 8, .2)

psi4.set_options({
    "basis": "aug-cc-pVDZ",
    "e_convergence": 1e-10,
    "d_convergence": 1e-10
    })

Eints = []
for R in distances:
    He2 = psi4.geometry(f"""
        He
        --
        He 1 {R}
    """)
    Eint_HF = psi4.energy("scf", bsse_type="cp", molecule=He2)
    Eint_MP2 = psi4.energy("mp2", bsse_type="cp", molecule=He2)
    Eints.append([Eint_HF, Eint_MP2])

col_name_distances = "R / angstrom"
col_name_HF = "Eint_HF/ au"
col_name_MP2 = "Eint_MP2 / au"
He2_PEC = pd.DataFrame(Eints, index=distances)
He2_PEC.reset_index(inplace=True)
He2_PEC.columns = [col_name_distances, col_name_HF, col_name_MP2]
He2_PEC.to_csv(file_results, sep="\t")

distances = He2_PEC[col_name_distances]
Eints_MP2 = He2_PEC[col_name_MP2]
distance_min = distances.min()
distance_max = distances.max()
Eint_MP2_min = Eints_MP2.min()
distance_min_plot = 2
distance_max_plot = 8
Eint_min_plot = 1.2 * Eint_MP2_min
Eint_max_plot = -2 * Eint_MP2_min
ax = He2_PEC.plot.scatter(x=col_name_distances, y=col_name_MP2)
ax.set_xlim(distance_min_plot, distance_max_plot)
ax.set_ylim(Eint_min_plot, Eint_max_plot)
plt.rcParams["text.usetex"] = True
ax.set_xlabel(r"$R/\mathrm{\AA}$")
ax.set_ylabel(r"$E_\mathrm{int}^\mathrm{MP2}/\mathrm{au}$")
cs = CubicSpline(distances, Eints_MP2)
distances_cs = np.linspace(distance_min, distance_max, 100)
ax.plot(distances_cs, cs(distances_cs))
plt.savefig(file_plot)
