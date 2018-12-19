#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:50:16 2018

@author: foton
"""
import sys
import numpy as np
import CutoffEnergies as CE

def main(n_digits, idx_filt, comp_name, PSI_v, PSI_m, KS, filt, save_fig):
    
    # Read the data
    data_phys    = np.genfromtxt(phys_name)
    data_comp    = CE.read_file(comp_name)
    data_comp    = np.array([CE.total_seconds(line) for line in data_comp])
    
    # Find energy differences
    Tot_E        = data_phys[:, 2]
    Tot_E_rho    = data_phys[:, 0]
    Tot_E_dif    = [Tot_E[i]-Tot_E[-1] for i in range(len(Tot_E))]
    
    # Calculate rolling median
    filt_info    = [[] for i in range(3)]
    filt_info[0] = KS # kernel size
    filt_info[1] = filt # filtration method - median, mean
    filt_info[2] = CE.roll_filt_signal(data_comp, filt_info[1], filt_info[0]) # filtered signal
    
    # Find place, where differences in total energies starts to be smaler 
    # than n_digits threshold
    edge_prime   = CE.find_nearest(Tot_E_rho, PSI_v*PSI_m)
    Tot_E_dif_tmp= Tot_E_dif[edge_prime:-1]
        
    edge_idx     = CE.find_edge(Tot_E_dif_tmp, n_digits)
    edge_idx     = edge_idx[idx_filt] + edge_prime
    
    # Plotting part
    textstr      = '\n'.join([r"$\delta E^{tot}=|E^{tot}_i-E^{tot}_{last}|$",
                              r"$\delta E^{tot}>$"+str(n_digits),
                              r"$E_\rho=$"+str(int(Tot_E_rho[edge_idx]))+"Ry",
                             ])
    x_label      = r"Cutoff energy for charge densityq $E_\rho$ [Ry]"
    
    CE.plot_E(Tot_E_rho, Tot_E_dif, "E_rho",
              data_comp, filt_info[2], filt_info[1], filt_info[0],
              edge_idx, textstr, 0.85, x_label, save_fig)
    
    return Tot_E_dif
# Initial data
n_digits         = 10**-4  # n-digits threshold - could be the number like e.g. 0.0012
idx_filt         = 10       # n'th index for which energy diff is lower than n_digits

PSI_value        = 46      # Cutoff energy of wavefunction
PSI_multiplicity = 4       # PSI_v * PSI_m is energy, from which program stars to searching for n_digits diff. 4*E_psi is minimum because of theory

phys_name        = "Examples_out/E_rho_RESULTS_phys.txt"
comp_name        = "Examples_out/E_rho_RESULTS_comp.txt"

K                = 5       # Filtration kernel size
filt_method      = "median"# Filtration method - median, mean

save_fig         = True    # Figure saving option

if __name__=="__main__":
    main(n_digits, idx_filt, 
         comp_name, PSI_value, PSI_multiplicity,
         K, filt_method, 
         save_fig)
