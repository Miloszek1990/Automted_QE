**1. CUTOFF ENERGIES FOR WAVEFUNCTIONS.**<br>
<br>**E_psi_cut.sh** is a bash script which runs series of QE SCF calculations and save main data in to two files: 
- E_psi_RESULTS_1_phys.txt - physical results E_psi, E_rho, total energy, HOMO, LOMO, band gap.
- E_psi_RESULTS_2_comp.txt - list of lines with SCF calculation times.

You should have compiled QE on your machine and define the path to it and to pseudopotentials etc. at the begging of the script. You should set MPI parallel parameters (if you don't want to use it then you put *false*). You can also set limits and step between the SCF calculations. Generated data output files will be used by Python script. Example outputs are attached in the *Examples_out* folder.<br>
<br>**E_psi_cut_analyse.py** is a script, which uses generated main data files from previous step (or from example dir) and import the **CutoffEnergies.py** library. In this script you should define only the comp and phys names (main data files), saving option and the threshold for total energy in Rydbergs. Additionally you can set the idx_filt parameter, which set later energies than the threshold shows - it is helpfull for noisy data.
<p align="center">
  <img src="https://github.com/Miloszek1990/Automted_QE/blob/master/Cutoff_energies/Examples_out/E_psi.png" width="350" title="hover text">
</p>
