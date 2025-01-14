# -*- coding: utf-8 -*-

"""

@ author: Jingran Wang

@ Email: jrwangspencer@stu.suda.edu.cn

@ Address: Center for Systems Biology, Department of Bioinformatics, School of Biology and Basic Medical Sciences, Soochow University, Suzhou 215123, China.

@ GitHub: https://github.com/Spencer-JRWang/APMA

"""


#############################################
### Introduction of AAWeb module
#
# @ This module is to construct network of proteins
#
#############################################


import subprocess
# import rpy2.robjects as robjects
# from rpy2.robjects.packages import importr
# bio3d = importr("bio3d")
# NACEN = importr("NACEN")
# igraph = importr("igraph", robject_translations={'.env':'__env'})
def AAWEB(route,t, category, Mut_PDB,WT_PDB,data_rote):
    '''
    Function to calculate the Amino Acids Web Features for several given mutation type pdb files
    The Features are:
    - delta Betweenness -> Mutation Type integrated global - Wild Type
    - delta Closeness -> Mutation Type integrated global - Wild Type
    - delta Eigenvector -> Mutation Type integrated global - Wild Type
    - delta Hydrophobilicity -> Mutation Type single global - Wild Type
    - delta Polarity -> Mutation Type single global - Wild Type
    the NACEN package is base on R, so you should prepare it before calling this function.
    The NACEN Website is: http://sysbio.suda.edu.cn/NACEN
    
    Parameters:
    - route: route to mkdssp or dssp
    - t: the number of mutations of the current category
    - category: the category of mutation type
    - Mut_PDB: the prefix of the name of the phenotypte
    - WT_PDB: the route to wildtype PDB file
    '''
    element_count = category.count(t)
    r_code = f'''#!/usr/bin/Rscript

############################
library('bio3d')
library('NACEN')
library('igraph')
############################

############################
dsspfile <- "{route}"
MT_betweeness <- c()
MT_closeness <- c()
MT_eigenvector <- c()
# Polarity <- c()
Hydrophobicity <- c()

# MT_degree <- c()
MT_cc <- c()
# MT_pagerank <- c()
############################

############################
# Wild Type
data <- "{WT_PDB}"
# Net <- suppressMessages(NACENConstructor(PDBFile=data,WeightType = "Polarity",exefile = dsspfile,plotflag=F))
Net <- suppressMessages(NACENConstructor(PDBFile=data,WeightType = "Hydrophobicity",exefile = dsspfile,plotflag=F))
NetP <- suppressMessages(NACENAnalyzer(Net$AM,Net$NodeWeights))
# WT_polarity <- Net$NodeWeights
WT_hydrophobicity <- Net$NodeWeights
# WT_polarity <- as.vector(WT_polarity)
WT_hydrophobicity <- as.vector(WT_hydrophobicity)

net <- NetP$Edgelist
network <- c(net[,1],net[,2])
network <- graph(network)
result <- NetP$NetP

WT_betweeness <- result$B
WT_closeness <- result$C
WT_eigenvector <- suppressWarnings(evcent(network,scale=F)$vector)
# WT_degree <- result$K

WT_cc <- suppressWarnings(transitivity(network,type="localundirected"))
WT_cc[is.na(WT_cc)] <- 0
# WT_pagerank <- suppressWarnings(page_rank(network, damping = 0.999)$vector)
############################

############################
for(i in 1:{element_count}){{
	data <- paste(c("{Mut_PDB}/{t}_",i,".pdb"),collapse="")

    # Use NACEN to calculate nodewights based on Polarity and Hydrophobicity
	# Net <- suppressMessages(NACENConstructor(PDBFile=data,WeightType = "Polarity",exefile = dsspfile,plotflag=F))
    Net <- suppressMessages(NACENConstructor(PDBFile=data,WeightType = "Hydrophobicity",exefile = dsspfile,plotflag=F))

    # Fetch NodeWeights
    # polarity <- Net$NodeWeights
    hydrophobicity <- Net$NodeWeights

    # Change into vectors
    # polarity <- as.vector(polarity)
    hydrophobicity <- as.vector(hydrophobicity)

    # Calculate the difference value of MT and WT
    # polarity <- polarity - WT_polarity
    hydrophobicity <- hydrophobicity - WT_hydrophobicity

    # Use global polarity and hydrophobicity change
    # polarity <- sum(polarity)
    hydrophobicity <- sum(hydrophobicity)

    # Record
    # Polarity <- c(Polarity, polarity)
    Hydrophobicity <- c(Hydrophobicity, hydrophobicity)

    # Calculate graph centrality
	NetP <- suppressMessages(NACENAnalyzer(Net$AM,Net$NodeWeights))
	net <- NetP$Edgelist
	result <- NetP$NetP
    
    # Degree
	# degree <- result$K
    # MT_degree <- cbind(MT_degree,degree)

    # Calculate betweenness
	betweeness <- result$B
    MT_betweeness <- cbind(MT_betweeness,betweeness)

    # Calculate closeness
	closeness <- result$C
	MT_closeness <- cbind(MT_closeness,closeness)
	
    # Calculate eigenvetor
	network <- c(net[,1],net[,2])
    network <- graph(network)
    ev <- suppressWarnings(evcent(network,scale=F)$vector)
    MT_eigenvector <- cbind(MT_eigenvector,ev)

    tr <- suppressWarnings(transitivity(network,type="localundirected"))
    tr[is.nan(tr)] <- 0
    # pg <- suppressWarnings(page_rank(g, damping = 0.999)$vector)
    MT_cc <- cbind(MT_cc, tr)
    # MT_pagerank <- cbind(MT_pagerank, pg)
}}
############################

############################
# Mean graph centrality
MT_betweeness <- rowMeans(MT_betweeness)
MT_closeness <- rowMeans(MT_closeness)
MT_eigenvector <- rowMeans(MT_eigenvector)
# MT_degree <- rowMeans(MT_degree)
MT_cc <- rowMeans(MT_cc)
# MT_pagerank <- rowMeans(MT_pagerank)


Betweeness <- MT_betweeness - WT_betweeness
Closeness <- MT_closeness - WT_closeness
Eigenvector <- MT_eigenvector - WT_eigenvector
# Degree <- MT_degree - WT_degree
CC <- MT_cc - WT_cc
# PageRank <- MT_pagerank - WT_pagerank

AA_web_1 <- cbind(Betweeness, Closeness)
AA_web_1 <- cbind(AA_web_1, Eigenvector)
AA_web_1 <- cbind(AA_web_1, CC)
# AA_web_2 <- cbind(Polarity, Hydrophobicity)
AA_web_2 <- Hydrophobicity
# AA_web <- cbind(AA_web, Degree)
# AA_web <- cbind(AA_web, Clustering_coefficient)
# AA_web <- cbind(AA_web, PageRank)

write.table(AA_web_1,"{data_rote}/{t}.txt",sep="\\t",row.names = FALSE)
dNW_file_path <- "{data_rote}/dNodeWeight.txt"
if (!file.exists(dNW_file_path)) {{
    write.table(AA_web_2, file=dNW_file_path, sep="\\t", row.names=FALSE, col.names=FALSE, append=FALSE)
}} else {{
    write.table(AA_web_2, file=dNW_file_path, sep="\\t", row.names=FALSE, col.names=FALSE, append=TRUE)
}}
############################
'''
    # write to .R file
    with open('/home/wangjingran/APMA/Feature_Cal/AANetwork.R', 'w') as file:
        file.write(r_code)
    # robjects.r(str(r_code))
    # excute the .R file
    AANetworkCommand = 'Rscript /home/wangjingran/APMA/Feature_Cal/AANetwork.R'
    subprocess.run(AANetworkCommand, shell=True)
    print(f"[INFO] NACEN category {t} is done")
    return None


def data_AAW_gener(position, category):
    """
    Generate AAWeb data based on positions and categories.

    This function reads data from files in the AAWeb directory based on the given
    positions and categories, and compiles the data into a list.

    Args:
        position (list of int): A list of positions to select data from each file.
        category (list of str): A list of category names corresponding to the files to read.

    Returns:
        list: A list of data entries corresponding to the specified positions and categories.
    """
    AAW_data = []
    for i in range(len(position)):
        current_cate = category[i]
        current_data = []
        with open(f"/home/wangjingran/APMA/data/AAWeb/{current_cate}.txt", 'r') as file:
            for line in file:
                columns = line.strip().split('\t')
                current_data.append(columns)
        current_data_features = current_data[position[i]]
        AAW_data.append(current_data_features)
    return AAW_data


def dNW_gener():
    """
    Generate delta NodeWeights data excluding headers.

    This function reads data from the dNodeWeight.txt file in the AAWeb directory,
    filters out lines containing 'Polarity' or 'Hydrophobicity', and compiles the 
    remaining data into a list.

    Returns:
        list: A list of data entries excluding those containing 'Polarity' or 'Hydrophobicity'.
    """
    dNW_data = []
    with open("/home/wangjingran/APMA/data/AAWeb/dNodeWeight.txt", "r") as file:
        for line in file:
            columns = line.strip().split('\t')
            if ('"Polarity"' in columns) or ('"Hydrophobicity"' in columns):
                pass
            else:
                dNW_data.append(columns)
    return dNW_data
      
