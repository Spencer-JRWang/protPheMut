# -*- coding: utf-8 -*-

"""

@ author: Jingran Wang

@ Email: jrwangspencer@stu.suda.edu.cn

@ Address: Center for Systems Biology, Department of Bioinformatics, School of Biology and Basic Medical Sciences, Soochow University, Suzhou 215123, China.

@ GitHub: https://github.com/Spencer-JRWang/deePheMut

"""

#############################################
### Introduction of mutation module
#
# @ This module is to run foldx in python
#
#############################################



import os
import subprocess
import shutil

def run_FoldX(path_to_foldx,WT_PDB,mutant_file):
    '''
    Function to operate foldx in python
    '''
    # move pdb file to folder
    print("...FoldX mutation PDB generating...")
    shutil.copy(WT_PDB, path_to_foldx)
    FoldX_WT_PDB = WT_PDB.split("/")[-1]
    # handle mutation file
    mutant_data = []
    type = []
    with open(mutant_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            mutant_data.append(columns[1] + ";")
            type.append(columns[0])
    f = open(path_to_foldx+"/individual_list.txt", "w")
    for item in mutant_data:
        f.write(item + "\n")
    f.close()
    # print(type)
    # change to file
    original_directory = os.getcwd()
    folder_path = path_to_foldx
    os.chdir(folder_path)
    # run FoldX
    foldx_command = f"./foldx5 --command=BuildModel --pdb={FoldX_WT_PDB} --mutant-file=individual_list.txt"
    subprocess.run(foldx_command, shell=True)
    for filename in os.listdir(folder_path):
        # check file name
        if filename.startswith("WT_"):
            file_path = os.path.join(folder_path, filename)
            # delete WT files
            if os.path.isfile(file_path):
                os.remove(file_path)

    result_list = []
    counter = 1
    prev_item = None
    for item in type:
        if item != prev_item:
            counter = 1
        result_list.append(counter)
        counter += 1
        prev_item = item
    #print(result_list)
    
    for i in range(len(result_list)):
        old_name = folder_path + f'/{FoldX_WT_PDB.removesuffix(".pdb")}_{i+1}.pdb'
        new_name = folder_path + f'/{type[i]}_{result_list[i]}.pdb'
        os.rename(old_name, new_name)

    print("Done")
    os.chdir(original_directory)
    return 0

def get_total_energy(path_to_foldx, WT_PDB):
    print("Fetching Total Energy...", end = " ")
    total_energy = []
    FoldX_WT_PDB = WT_PDB.split("/")[-1].removesuffix(".pdb")
    f = open(path_to_foldx + f"/Dif_{FoldX_WT_PDB}.fxout","r")
    all = f.readlines()
    for i in range(len(all)):
        if i in [0,1,2,3,4,5,6,7,8]:
            pass
        else:
            te = all[i].split("\t")[1]
            total_energy.append(float(te))
    f.close()
    print("Done")
    return total_energy







if __name__ == "__main__":
    run_FoldX("C:/Users/33385/Desktop/FoldX",
              "C:/Users/33385/Desktop/data/alphafoldpten.pdb",
              "C:/Users/33385/Desktop/data/position.txt")
