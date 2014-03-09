'''
This code is used to access the path of templates 
'''
import os
def getTempPath():
    
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    return PROJECT_ROOT