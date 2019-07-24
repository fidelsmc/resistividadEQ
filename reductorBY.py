# -*- coding: utf-8 -*-
"""
Permite simplificar el modelo de n capas a 2 capas
Metodo de resistividad equivalente burgsdorf-Yakobs
@author: fmoreno
"""
import numpy as np
import logging
logging.basicConfig(filename='resultados.log',level=logging.DEBUG,format='%(message)s')
logging.info(" ########## INICIO DE CALCULO ##########")

# Configurable por el Usuario
A=10110.3025 #area en m2
b=0.6 # profundudad de malla m
rho=(719,2480,481,41512) #resistividad de las capas ohm-m
d=(3.01,5,50.10,999999) #profundidad de las capas en m

##############################################################################
logging.info("        Area = {} m2".format(A))
logging.info(" Prof. malla = {} m".format(b))
logging.info("         rho = {} ohm-m".format(rho))
logging.info(" Prof. capas = {} m".format(d))

aux=0   
ui=[]
vi=[]
Fi=[0]

r=np.sqrt(A/np.pi)
r0=np.sqrt((r*r)-(b*b))
q0=np.sqrt(2*r*(r+b))

logging.info("           r = {}".format(r))
logging.info("          r0 = {}".format(r0))
logging.info("          q0 = {}".format(q0))

def uii(q0,r0,hi):
    return np.sqrt((q0*q0)+(r0*r0)+(hi*hi))

def vii(ui,q0,r0):
    return np.sqrt(0.5*(np.power(ui,2)-np.sqrt(np.power(ui,4)-4*q0*q0*r0*r0)))

def Fii(vi,r0):
    return np.sqrt(1-np.power(vi/r0,2))

for i in range(0, len(rho)):
    u=uii(q0,r0,d[i])
    ui.append(u)
    
    v=vii(ui[i],q0,r0)
    vi.append(v)
    
    F=Fii(vi[i],r0)
    Fi.append(F)
 
for j in range(2,len(Fi)-1): #cambiar el 2 por 1 para reduc. a 1 capa
    aux=aux+((Fi[j]-Fi[j-1])/rho[j-1])
    
req=round((1-Fi[1])/aux,3)

logging.info("          ui = {}".format(ui))
logging.info("          vi = {}".format(vi))
logging.info("          Fi = {}".format(Fi))
logging.info("  ########## REDUCCION A 2 CAPAS ##########")
logging.info("      Capa 1 = {} ohm-m".format(np.round(rho[0],3)))
logging.info("      Capa 2 = {} ohm-m".format(req))

print("Reduccion a dos capas...")    
print("Capa 1:",np.round(rho[0],3),"ohm-m \tEspesor:",d[0]," m")
print("Capa 2:",req,"ohm-m \tEspesor: inf")
