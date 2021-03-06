#!/usr/bin/python

# library to emulate the standard complex C type (C99)

import sys
import commands
pymod=commands.getoutput("echo $PYMOD");
if pymod.startswith('local'):
    py_numpy=commands.getoutput("echo $PY_NUMPY");sys.path.insert(1,py_numpy);
import numpy as np
from ctypes import *

class Complex(Structure):

    '''class to emulate std::complex<double> C type'''
    _fields_ = [("real", c_double), ("imag", c_double)];
    

def complex_to_Complex(z):

    ''' conversion from a python complex z to a C Complex '''
    
    return Complex(z.real,z.imag);


def Complex_to_complex(z):

    ''' conversion from a C Complex z to a python complex '''
    
    return z.real+1j*z.imag;

