#!/usr/bin/python2.6

import sys
sys.path.append("/afs/cern.ch/eng/sl/lintrack/Python_Classes4MAD/")
import pylab
import numpy as np
import math,cmath
from matplotlib.font_manager import FontProperties
from string import split, replace
from optparse import OptionParser
from plot_lib import set_fontsize,init_figure,end_figure
from io_lib import list_files
from string_lib import takeout_common


def parsse():
    parser = OptionParser()
    parser.add_option("-f", "--file",action="append",
                      help="Specify the file name (longitudinal impedance, flat case). Several files are possible - either with regular expression (using *, [], etc. and BETWEEN QUOTES \"\") or with several -f options.",
                      metavar="FILE", default=None,dest="FILE")
    parser.add_option("-g", "--legend",action="append",
                      help="Specify the legend for each file",
                      metavar="LEG", default=None,dest="LEG")
    parser.add_option("-m", "--meter",action="store_true",
                      help="Specify if the impedance are per meter length",
                      metavar="METER", default=False,dest="METER")
    parser.add_option("-c", "--constant",action="store_true",
                      help="Specify if we should plot the constant term Zycst",
                      metavar="CST", default=False,dest="CST")
    parser.add_option("-l", "--loglog",action="store_true",
                      help="Specify if loglog plot (semilogx by default)",
                      metavar="LOG", default=False,dest="LOG")
    (opt, args) = parser.parse_args()
    #print "Selected Files:", opt.FILE
    return opt, args

def logplot(freq,Z,lab,leg1,leg2,col):
    # plot two impedances (real and imag parts) and put legend and label
    legr="|Re["+leg1+"]|"
    legi="|Im["+leg1+"]|"
    Zr=np.array([math.fabs(j) for j in Z.real]);
    Zi=np.array([math.fabs(j) for j in Z.imag]);
    pylab.loglog(freq,Zr,col+'-',label=legr+leg2,lw=2.5,ms=10.,mew=2.5)
    pylab.loglog(freq,Zi,col+'--',label=legi+leg2,lw=2.5,ms=10.,mew=2.5)
    pylab.xlabel("Frequency [Hz]")
    pylab.ylabel("Z "+lab);

def semilogplot(freq,Z,lab,leg1,leg2,col):
    # plot impedance (real and imag parts) with labels, legend and color
    legr="Re["+leg1+"]"
    legi="Im["+leg1+"]"
    pylab.semilogx(freq,Z.real,col+'-',label=legr+leg2,lw=2.5,ms=10.,mew=2.5)
    pylab.semilogx(freq,Z.imag,col+'--',label=legi+leg2,lw=2.5,ms=10.,mew=2.5)
    pylab.xlabel("Frequency [Hz]")
    pylab.ylabel("Z "+lab);


def read(filename):
    # read impedance file (3 columns: frequency, real and imag. parts)
    freq=[];Z1=[];Z2=[]
    fh=open(filename,"r")
    for l in fh.readlines():
    	if not l.startswith('Freq'):
		ll=l.strip().split();
		freq.append(ll[0]);
		Z1.append(ll[1]);
		Z2.append(ll[2]);
    fh.close()
    f=np.array([float(j) for j in freq])
    Z=np.array([float(j) for j in Z1])+1j*np.array([float(j) for j in Z2])
    return f,Z
    
                  
if __name__ == "__main__":
    opt,args=parsse();
    
    # create list of filenames to analyse
    listname=list_files(opt.FILE);

    # create list of associated legends (either with opt.LEG or 
    # the list of file names taking out all the common parameters
    # in the names)
    if (opt.LEG!=None):
        listleg=opt.LEG;
    else:
        listleg=takeout_common(listname);
	
    

    if (opt.CST): nfig=6;
    else: nfig=5;
 
    for i in range(nfig): init_figure();
    
    color=['b','r','g','m','c','y','k'];

    for j,fil in enumerate(listname):

	# string for legend
	leg=listleg[j].replace(".dat","");
	#if opt.LEG==None: leg=fil.replace("ZlongW","",1).replace("_"," ");
	#else: leg=opt.LEG[j];
	
	# constructs all the files names (flat chamber impedances)
	filefxdip=fil.replace("Zlong","Zxdip",1);
	filefxquad=fil.replace("Zlong","Zxquad",1);
	filefydip=fil.replace("Zlong","Zydip",1);
	filefyquad=fil.replace("Zlong","Zyquad",1);
	filefycst=fil.replace("Zlong","Zycst",1);

	# read longitudinal impedance and plot
	freq,Z=read(fil)
	if not opt.METER: lab=" [$\Omega$]"
	else: lab=" [$\Omega$ /m]"
	pylab.figure(1);
	if opt.LOG: logplot(freq,Z,lab,"$Z_{\|\|}$",", "+leg,color[j]);
	else: semilogplot(freq,Z,lab,"$Z_{\|\|}$",", "+leg,color[j]);

	# thin wall
	#pylab.figure(1);
	#logplot(freq,1j*4e-7*np.pi*freq*500e-9/(49e-3),lab,"$Z_{\|\|}$",", thin wall, aC 500nm",'g');
	#logplot(freq,1j*4e-7*np.pi*freq*2e-6/(49e-3),lab,"$Z_{\|\|}$",", thin wall, aC $ 2\mu $ m",'m');

	if opt.CST:
    	    # read constant vertical impedance and plot
    	    pylab.figure(6);
    	    freq,Z=read(filefycst)
    	    if opt.LOG: logplot(freq,Z,lab,"$Z_y^{cst}$",", "+leg,color[j]);
    	    else: semilogplot(freq,Z,lab,"$Z_y^{cst}$",", "+leg,color[j]);


	if not opt.METER: lab=" [$\Omega$ /m]"
	else: lab=" [$\Omega$ /m$^2$]"
	# read transverse dipolar impedances and plot them    
	freq1,Z1=read(filefxdip)
	freq2,Z2=read(filefydip)
	pylab.figure(2);
	
	if opt.LOG:
    	    logplot(freq1,Z1,lab,"$Z_x^{dip}$",", "+leg,color[j]);
    	    pylab.figure(3);logplot(freq2,Z2,lab,"$Z_y^{dip}$",", "+leg,color[j]);
	else:
    	    semilogplot(freq1,Z1,lab,"$Z_x^{dip}$",", "+leg,color[j]);
    	    pylab.figure(3);semilogplot(freq2,Z2,lab,"$Z_y^{dip}$",", "+leg,color[j]);

	# read transverse quadrupolar impedances and plot them
	freq1,Z1=read(filefxquad)
	freq2,Z2=read(filefyquad)
	pylab.figure(4);
	if opt.LOG:
    	    logplot(freq1,Z1,lab,"$Z_x^{quad}$",", "+leg,color[j]);
    	    pylab.figure(5);logplot(freq2,Z2,lab,"$Z_y^{quad}$",", "+leg,color[j]);
	else:
    	    semilogplot(freq1,Z1,lab,"$Z_x^{quad}$",", "+leg,color[j]);
    	    pylab.figure(5);semilogplot(freq2,Z2,lab,"$Z_y^{quad}$",", "+leg,color[j]);
    
	
    # thin wall
    #pylab.figure(2);
    #logplot(freq1,1j*4e-7*299792458*500e-9/(49e-3**3)*np.ones(len(freq1)),lab,"$Z_x^{dip}$",", thin wall, aC 500nm",'g');
    #logplot(freq1,1j*4e-7*299792458*2e-6/(49e-3**3)*np.ones(len(freq1)),lab,"$Z_x^{dip}$",", thin wall, aC $ 2\mu $ m",'m');
	
    for i in range(nfig):
    	pylab.figure(i+1);
    	pylab.legend(loc=0);
	set_fontsize(pylab.figure(i+1),'xx-large');

    pylab.show();sys.exit()

