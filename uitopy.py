# -*- coding: utf-8 -*-
"""
Created on Sun May  3 03:58:06 2020

@author: anlka
"""


#from PyQt4 import uic

from PyQt5 import uic 

with open('library.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('library.ui', fout)