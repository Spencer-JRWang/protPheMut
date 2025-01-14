# -*- coding: utf-8 -*-

"""

@ author: Jingran Wang

@ Email: jrwangspencer@stu.suda.edu.cn

@ Address: Center for Systems Biology, Department of Bioinformatics, School of Biology and Basic Medical Sciences, Soochow University, Suzhou 215123, China.

@ GitHub: https://github.com/Spencer-JRWang/APMA

"""

#############################################
### Introduction of prody_cal module
#
# @ This module is to calculate dynamic network features on protein(based on prody)
#
#############################################



import pandas as pd
from prody import *
from pylab import *
ion()
import numpy as np
from sklearn.preprocessing import scale

def cal_dynamics(path,name):
    ampar_ca = parsePDB(path, subset='ca')
    anm_ampar = ANM('AMPAR MT')
    anm_ampar.buildHessian(ampar_ca)
    anm_ampar.calcModes('all')
    prs_mat, effectiveness, sensitivity = calcPerturbResponse(anm_ampar)
    # dfi=calcDynamicFlexibilityIndex(anm_ampar,ampar_ca,"all",norm="True")
    gnm_ampar = GNM(name)
    gnm_ampar.buildKirchhoff(ampar_ca)
    gnm_ampar.calcModes('all')
    msf=calcSqFlucts(gnm_ampar)
    dfi=calcDynamicFlexibilityIndex(gnm_ampar,ampar_ca,"all",norm="True")
    stiff=calcMechStiff(anm_ampar,ampar_ca)
    newstiff=np.mean(stiff,1)
    dyn_data = np.vstack((effectiveness,
                         sensitivity,
                         msf,
                         dfi,
                         newstiff))
    
    all_dyn_data = np.transpose(dyn_data)
    num_rows = all_dyn_data.shape[0]
    sequence_dyn = np.arange(1, num_rows + 1).reshape(-1, 1)
    header = 'Site\tEffectiveness\tSensitivity\tMSF\tDFI\tStiffness'
    all_dyn_data = np.hstack((sequence_dyn, all_dyn_data))

    np.savetxt('/home/wangjingran/APMA/data/all_dyn_data.txt', all_dyn_data, delimiter='\t', 
            header=header, 
            comments='', 
            fmt='%d' + '\t%.10f' * (all_dyn_data.shape[1] - 1))
    return dyn_data

def dynamics_dat(name,position,WT_PDB):
    '''
    calculate dynamics using prody package, including five features:
    Effectiveness, sensitivity, stiffness, DFI and MSF
    you should prepare your protein name fot this function
    :return: a list with all dynamics calculated for the given position based on your wild type PDB
    '''
    dyn_data = cal_dynamics(WT_PDB,name)
    print("...Calculating kinetic features...")
    dyn_data = np.transpose(dyn_data)
    new_dyn = dyn_data[[x - 1 for x in position]]
    print("Success")
    return new_dyn
    