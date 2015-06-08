# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:26:38 2015

@author: medina
"""
import random 

#Parametros de entrada
INTERVALO_CHEGADA = 24.0 # intervalo (h) médio entre chegadas sucessivas de navios
TEMPO_OPERACAO_MODA = 10.0 # moda da taxa de operacao no berco (tph)
TEMPO_OPERACAO_MAX = 12.0 # maior valor da taxa de operacao no berco (tph)
TEMPO_OPERACAO_MIN = 5.0 # maior valor da taxa de operacao no berco (tph)

def defineSeed(seed):
    random.seed(seed)
    
def chegadas():
    return random.expovariate(1.0/INTERVALO_CHEGADA)

def carregamento():
    return random.triangular(TEMPO_OPERACAO_MIN, TEMPO_OPERACAO_MODA, TEMPO_OPERACAO_MAX)

 