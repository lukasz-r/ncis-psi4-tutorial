#!/usr/bin/env python3

import pandas as pd
import psi4

pd.options.display.float_format = "{:.4e}".format

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
        Eint_HF = psi4.energy("scf", bsse_type="cp", molecule=dimer)
        Eint_MP2 = psi4.energy("mp2", bsse_type="cp", molecule=dimer)
        Eints.append([Eint_HF, Eint_MP2])

    table = pd.DataFrame(Eints, index=basis_sets, columns=["Eint_HF", "Eint_MP2"])
    table.index.name = "basis_set"
    file_table = dimer.name() + ".txt"
    table.to_csv(file_table, sep="\t")
