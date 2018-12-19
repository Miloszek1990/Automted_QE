**1. CUTOFF ENERGIES FOR WAVEFUNCTIONS.**<br>
<br>**E_psi_cut.sh** and **E_rho_cut.sh** is a bash script, which runs series of QE SCF calculations and save the main data in to two files: 
- E_psi/rho_RESULTS_1_phys.txt - physical results of E_psi, E_rho, total energy, HOMO, LOMO, band gap.
- E_psi/rho_RESULTS_2_comp.txt - list of lines with SCF calculation times.

You should have compiled QE on your machine and define the path to it and to pseudopotentials etc. Main part to change is a cat part where you should put yours input file, with customized proper lines: $PSI, $RHO, etc. At the begging of the scripts you should set limits and step size between the SCF calculations. you can also set MPI parallel computing parameters (if you don't want to use it then you should put *false*). Generated data output files will be used by Python scripts. Example outputs are attached in the *Examples_out* folder.<br>
<br>**E_psi_cut_analyse.py** is a script, which uses generated main data files from previous step (or from example dir) and import the **CutoffEnergies.py** library. In this script you should define only the comp and phys names (main data files), saving option and the threshold for difference in the total energy in Rydbergs. Additionally you can set the idx_filt parameter, which takes the  later energies than the threshold shows - it is helpfull for noisy data. Data will be pressented like in the plot below:
<p align="center">
  <img src="https://github.com/Miloszek1990/Automted_QE/blob/master/Cutoff_energies/Examples_out/E_psi.png" width="350" title="hover text">
</p>
<br>**E_psi_cut_analyse.py** is a script, which uses generated main data files from shell step (or from example dir) and import the **CutoffEnergies.py** library. In this script you should define only the comp and phys names (main data files), saving option and the threshold for difference in the total energy in Rydbergs. You can set starting energy for obtaining the E_rho. It is defined in multiplicity o E_psi domain - definetley it should starts minimum from 4*E_psi. 
<p align="center">
  <img src="https://github.com/Miloszek1990/Automted_QE/blob/master/Cutoff_energies/Examples_out/E_rho.png" width="350" title="hover text">
</p>
