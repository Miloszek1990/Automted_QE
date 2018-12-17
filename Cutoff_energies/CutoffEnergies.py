#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:47:35 2018

@author: foton
"""
import matplotlib.pyplot as plt

def total_seconds(PWSCF_line):
    
    # Possible time stamps
    replacements = ("d","h","m","s")
    
    # Take the info betwen ":" and "CPU"
    PWSCF_line = PWSCF_line.split()
    idx_beg = PWSCF_line.index(":")
    idx_end = PWSCF_line.index("CPU")
    PWSCF_line = PWSCF_line[idx_beg+1:idx_end]
    PWSCF_line = "".join(PWSCF_line)
    
    # Find time stamps, and their values
    used_replacements = []
    for r in replacements:
        if r in PWSCF_line:
            used_replacements.append(r)
        PWSCF_line = PWSCF_line.replace(r," ")
    PWSCF_line = PWSCF_line.split()
    
    # Convert to total seconds
    for i in range(len(PWSCF_line)):
        if used_replacements[i] == "d":
            PWSCF_line[i] = float(PWSCF_line[i])
            PWSCF_line[i] = 24*60*60*PWSCF_line[i]
        if used_replacements[i] == "h":
            PWSCF_line[i] = float(PWSCF_line[i])
            PWSCF_line[i] = 60*60*PWSCF_line[i]
        if used_replacements[i] == "m":
            PWSCF_line[i] = float(PWSCF_line[i])
            PWSCF_line[i] = 60*PWSCF_line[i]
        if used_replacements[i] == "s":
            PWSCF_line_tmp = PWSCF_line[i].split(".")
            minutes = float(PWSCF_line_tmp[0])*60
            try:
                seconds = float(PWSCF_line_tmp[1])
            except IndexError:
                seconds = 0
            PWSCF_line[i]  = minutes + seconds
    
    return int(sum(PWSCF_line))

def read_file(file_name):
    
    with open(file_name, "r") as file:
        data_comp = []
        for line in file:
            line_list = line.split()
            line = " ".join(line_list)
            data_comp.append(line)
    
    return data_comp

def find_edge(Tot_E_diff, n_digits):
    
    edge_idx  = [] 
    for i in range(len(Tot_E_diff)):
        if Tot_E_diff[i] < n_digits:
            edge_idx.append(i)
    
    return edge_idx

def plot_E_psi(Tot_E_psi, Tot_E_diff, data_comp, edge_idx, text_str, save=False):
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    
    fig, (ax1, ax2) = plt.subplots(2, 1,sharex=True)
    
    ax1.plot(Tot_E_psi, Tot_E_diff)
    ax1.axvline(Tot_E_psi[edge_idx], color="r")
    ax1.set_ylabel(r"$\delta E^{tot}$ [Ry]")
    ax1.text(0.66, 0.95, text_str, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    ax2.plot(Tot_E_psi, data_comp)
    ax2.set_ylabel("Calculation time [s]")
    ax2.set_xlabel(r"Cutoff energy for wavefunction $E_\Psi$ [Ry]")
    ax2.axvline(Tot_E_psi[edge_idx], color="r")
    fig.subplots_adjust(hspace=0)
    
    if save==True:
        plt.savefig('E_psi.png', bbox_inches='tight', format='png', dpi=300)
