#!/usr/bin/env python3

import pandas as pd
import psi4

file_out = "SAPT_basis_sets.out"

pd.options.display.float_format = "{:.4e}".format

psi4.set_output_file(file_out)
psi4.set_memory("2 GB")

dimer_names = ["He-Ne", "He-Li+"]

HeNe = psi4.geometry("""
    He
    --
    Ne 1 3.0
""")
HeNe.set_name(dimer_names[0])

HeLiplus = psi4.geometry("""
    He
    --
    1 1
    Li 1 5.5
""")
HeLiplus.set_name(dimer_names[1])

dimers = [HeNe, HeLiplus]
for dimer in dimers:
    Eints = []
    basis_sets = ["aug-cc-pVDZ", "aug-cc-pVTZ", "aug-cc-pVQZ"]
    for basis_set in basis_sets:
        psi4.set_options({"basis": basis_set})
        ESAPT = psi4.energy("sapt0", molecule=dimer)
