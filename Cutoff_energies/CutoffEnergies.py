#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:47:35 2018

@author: foton
"""
import sys
import numpy as np
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
        elif used_replacements[i] == "h":
            PWSCF_line[i] = float(PWSCF_line[i])
            PWSCF_line[i] = 60*60*PWSCF_line[i]
        elif used_replacements[i] == "m":
            PWSCF_line[i] = float(PWSCF_line[i])
            PWSCF_line[i] = 60*PWSCF_line[i]
        elif used_replacements[i] == "s":
            PWSCF_line_tmp = PWSCF_line[i].split(".")
            s_1 = float(PWSCF_line_tmp[0])
            try:
                s_2 = float(PWSCF_line_tmp[1])/100
            except IndexError:
                s_2 = 0
            PWSCF_line[i]  = s_1 + s_2

    return sum(PWSCF_line)

def read_file(file_name):
    
    with open(file_name, "r") as file:
        data_comp = []
        for line in file:
            line_list = line.split()
            line = " ".join(line_list)
            data_comp.append(line)
    
    return data_comp

def half_kernel_size(KS,signal):
    ### Check the size of rolling mean/median kernel
    # Any error will change the exit_status to 1
    # value 1 will close the program at the end
    exit_status = 0 
    
    # Check the kernel size - it must be the odd number
    if KS % 2 == 0:
        print("Kernel size must be an odd number.\n")
        exit_status = 1
    
    # Calculate the lower half value of the kernel
    # int() function for odd number is perfect for this
    h_KS = int(KS/2)    
    
    # Check the kernel size - its half value must be smaller than half size of signal
    if KS > int(signal.shape[0]/2):
        print("Half-size of signal is: " + str(signal.shape[0]/2))
        print("and the half-size of the kernel is: " + str(h_KS) + "\n")
        print("half-size of the kernel must be smaller than Half-size of signal.\n")
        exit_status = 1
    
    if exit_status == 1:
        sys.exit()
    
    if exit_status == 0:
        return h_KS

def roll_filt_signal(signal, method, KS):
    
    h_KS      = half_kernel_size(KS, signal)
    roll_sig  = []
    for i in range(h_KS, len(signal)-h_KS):
        roll_kernel_tmp = np.linspace(0,0,KS)
        
        j = 0
        for j in range(KS):
            i_tmp_mask = i + h_KS - j
            roll_kernel_tmp[j] = signal[i_tmp_mask]
        
        if method=="median":
            roll_sig.append(np.median(roll_kernel_tmp))
        elif method=="mean":
            roll_sig.append(np.mean(roll_kernel_tmp))
        else:
            print("Non-defined method. Median or mean are allowed.")
            
    roll_sig = np.array(roll_sig)
    
    return roll_sig

def find_nearest(signal, value):
    
    signal = np.asarray(signal)
    idx = (np.abs(signal - value)).argmin()
    
    return int(signal[idx])

def find_edge(Tot_E_diff, n_digits):
    
    edge_idx  = [] 
    for i in range(len(Tot_E_diff)):
        if Tot_E_diff[i] < n_digits:
            edge_idx.append(i)
    
    return edge_idx

def plot_E(Tot_E_psi, Tot_E_diff, 
           data_comp, data_comp_filt, filt_method, kernel_size,
           edge_idx, text_str, y_text_pos, X_label, save_fig=False):
    
    props    = dict(boxstyle='round', facecolor='white', alpha=0.5)
    filt_len = len(data_comp_filt)
    norm_len = len(data_comp)
    len_diff = int((norm_len - filt_len)/2)
    Tot_E_psi_filt = Tot_E_psi[len_diff:-(len_diff)]
    
    fig, (ax1, ax2) = plt.subplots(2, 1,sharex=True)
    
    ax1.plot(Tot_E_psi, Tot_E_diff)
    ax1.axvline(Tot_E_psi[edge_idx], color="r")
    ax1.set_ylabel(r"$\delta E^{tot}$ [Ry]")
    ax1.text(0.66, y_text_pos, text_str, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    ax2.plot(Tot_E_psi, data_comp, label="Main signal")
    ax2.plot(Tot_E_psi_filt, data_comp_filt, label=filt_method.capitalize()+" filtration, K="+str(kernel_size))
    ax2.set_ylabel("Calculation time [s]")
    ax2.set_xlabel(X_label)
    ax2.axvline(Tot_E_psi[edge_idx], color="r")
    ax2.legend()
    fig.subplots_adjust(hspace=0)
    
    if save_fig==True:
        plt.savefig('E_psi.png', bbox_inches='tight', format='png', dpi=300)