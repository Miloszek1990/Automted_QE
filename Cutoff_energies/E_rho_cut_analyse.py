#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:50:16 2018

@author: foton
"""

import numpy as np
import CutoffEnergies as CE

def main(n_digits, idx_filt, comp_name, KS, filt, save):
    
    # Read the data
    data_phys    = np.genfromtxt(phys_name)
    data_comp    = CE.read_file(comp_name)
    data_comp    = np.array([CE.total_seconds(line) for line in data_comp])
    
    # Find energy differences
    Tot_E        = data_phys[:, 2]
    Tot_E_psi    = data_phys[:, 0]
    Tot_E_dif    = [Tot_E[i]-min(Tot_E) for i in range(len(Tot_E))]
    
    # Calculate rolling median
    filt_info    = [[] for i in range(3)]
    filt_info[0] = KS # kernel size
    filt_info[1] = filt # filtration method - median, mean
    filt_info[2] = CE.roll_filt_signal(data_comp, filt_info[1], filt_info[0]) # filtered signal
    
    # Find place, where differences in total energies starts to be smaler 
    # than n_digits threshold
    edge_idx     = CE.find_edge(Tot_E_dif, n_digits)
    edge_idx     = edge_idx[idx_filt]
    
    textstr      = '\n'.join([r"$\delta E^{tot}=|E^{tot}_i-\min(E^{tot})|$",
                              r"$\delta E^{tot}>$"+str(n_digits),
                              
                              r"$E_\Psi=$"+str(int(Tot_E_psi[edge_idx]))+"Ry",
                             ])
    x_label      = r"Cutoff energy for wavefunction $E_\Psi$ [Ry]"
    
    CE.plot_E(Tot_E_psi, Tot_E_dif, 
              data_comp, filt_info[2], filt_info[1], filt_info[0],
              edge_idx, textstr, x_label, save)

# Initial data
n_digits         = 10**-4  # n-digits threshold - could be the number like e.g. 0.0012
idx_filt         = 150       # n'th index for which energy diff is lower than n_digits

phys_name        = "E_rho_RESULTS_phys.txt"
comp_name        = "E_rho_RESULTS_comp.txt"

K                = 5       # Filtration kernel size
filt_method      = "median"# Filtration method - median, mean

save_fig         = False    # Figure saving option

if __name__=="__main__":
    main(n_digits, idx_filt, comp_name, K, filt_method, save_fig)

