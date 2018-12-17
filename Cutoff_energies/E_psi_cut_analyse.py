#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 17:59:00 2018

@author: foton
"""
import numpy as np
import CutoffEnergies as CE

def main(n_digits, idx_filt, comp_name, save_fig):
    
    # Read the data
    data_phys = np.genfromtxt("E_psi_RESULTS_1_phys.txt")
    data_comp = CE.read_file(comp_name)
    data_comp = np.array([CE.total_seconds(line) for line in data_comp])
    
    # Find energy differences
    Tot_E     = data_phys[:, 2]
    Tot_E_psi = data_phys[:, 0]
    Tot_E_dif = [Tot_E[i]-min(Tot_E) for i in range(len(Tot_E))]
    
    # Find place, where differences in total energies starts to be smaler 
    # than n_digits threshold
    edge_idx  = CE.find_edge(Tot_E_dif, n_digits)
    edge_idx  = edge_idx[idx_filt]
    
    textstr   = '\n'.join([r"$\delta E^{tot}=|E^{tot}_i-\min(E^{tot})|$",
                           r"$\delta E^{tot}>$"+str(n_digits),
                           r"$E_\Psi=$"+str(int(Tot_E_psi[edge_idx]))+"Ry",
                          ])
    
    CE.plot_E_psi(Tot_E_psi, Tot_E_dif, data_comp, edge_idx, textstr, save=False)

# Initial data
n_digits  = 10**-4  # n-digits threshold - could be the number like e.g. 0.0012
idx_filt  = 3       # n'th index for which energy diff is lower than n_digits
comp_name = "E_psi_RESULTS_2_comp.txt"
save_fig  = False   # Figure saving option

if __name__=="__main__":
    main(n_digits, idx_filt, comp_name, save_fig)



