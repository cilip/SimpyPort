# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:48:47 2015

@author: simpy
"""
import simpy

env = simpy.Environment()

guindaste1 = 1
guindaste2 = 2
guindaste3 = 3

guindastesStore = simpy.Store(env, capacity=3)
guindastesStore.items = [guindaste1, guindaste2, guindaste3]


item = guindastesStore.get()
