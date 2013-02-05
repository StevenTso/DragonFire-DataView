#Program to store the arrays and print them

from pylab import *
from scipy import signal
import math, numpy
from matplotlib import pyplot

from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin

import binascii

num_lines = 0;
ACCEL_X = []
ACCEL_Y = []
ACCEL_Z = []
GYRO_X = []
GYRO_Y = []
GYRO_Z = []

# some constants
samp_rate = 20
sim_time = 60
nsamps = samp_rate*sim_time
cuttoff_freq = 0.1



def parser():
    global num_lines
    num_lines= sum(1 for line in open('data.txt'))
    f = open('data.txt', 'r')
    for var0 in range(0, num_lines):
        line = f.readline();
        #removes last comma and new line
        parsed_line = line[:-2];
        
        parsed_line = parsed_line.split(',');
        
        for var1 in range(0, 6):
            #removes white spaces
            if parsed_line[var1][-1:] == ' ':
                parsed_line[var1] = parsed_line[var1].rstrip();
            #remove escape character
            if parsed_line[var1][-1:] == '\x00':
                parsed_line[var1] = parsed_line[var1].rstrip('\x00');
            #parsed_line from string ---> int format
            parsed_line[var1] = int(parsed_line[var1])

        ACCEL_X.append(parsed_line[0]);
        ACCEL_Y.append(parsed_line[1]);
        ACCEL_Z.append(parsed_line[2]);
        GYRO_X.append(parsed_line[3]);
        GYRO_Y.append(parsed_line[4]);
        GYRO_Z.append(parsed_line[5]);

        #print parsed_line;
	
    #print ACCEL_X;
    #print ACCEL_Y;
    #print ACCEL_Z;
    #print GYRO_X;
    #print GYRO_Y;
    #print GYRO_Z;
    return

def grapher():
    #GRAPHS
    t1 = arange(0, num_lines, 1)

    #ACCEL_X
    subplot(231)
    plot(t1, ACCEL_X,'k--', markerfacecolor='green')
    title('ACCEL_X')
    ylabel('Value')

    #ACCEL_Y
    subplot(232)
    plot(t1, ACCEL_Y,'k--', markerfacecolor='green')
    title('ACCEL_Y')
    ylabel('Value')


    #ACCEL_Z
    subplot(233)
    plot(t1, ACCEL_Z,'k--', markerfacecolor='green')
    title('ACCEL_Z')
    ylabel('Value')

    #GYRO_X
    subplot(234)
    plot(t1, GYRO_X,'k--', markerfacecolor='green')
    title('GYRO_X')
    ylabel('Value')

    #GRYO_Y
    subplot(235)
    plot(t1, GYRO_Y,'k--', markerfacecolor='green')
    title('GYRO_Y')
    ylabel('Value')
    
    #GRYO_Z
    subplot(236)
    plot(t1, GYRO_Z,'k--', markerfacecolor='green')
    title('GYRO_Z')
    ylabel('Value')
    
    #show()
    return

def LPF():
    #FIR filter
    sample_rate = 40000
    nyq_rate = sample_rate/2
    global cuttoff_hz
    cutoff_hz= 1000.0
    numtaps = 40
    t2 = arange(0, num_lines, 1)
    
        
    #ACCEL_X
    subplot(231)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_X)
    plot(t2, filtered_signal)
    title('ACCEL_X')
    ylabel('Value')
    

    #ACCEL_Y
    subplot(232)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_Y)
    plot(t2, filtered_signal)
    title('ACCEL_Y')
    ylabel('Value')
    
    
    #ACCEL_Z
    subplot(233)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_Z)
    plot(t2, filtered_signal)
    title('ACCEL_Z')
    ylabel('Value')
    
    #GYRO_X
    subplot(234)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, GYRO_X)
    plot(t2, filtered_signal)
    title('GYRO_X')
    ylabel('Value')
    
    #GRYO_Y
    subplot(235)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, GYRO_Y)
    plot(t2, filtered_signal)
    title('GYRO_Y')
    ylabel('Value')
    
    #GRYO_Z
    subplot(236)
    fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
    filtered_signal = lfilter(fir_coeff, 1.0, GYRO_Y)
    plot(t2, filtered_signal)
    title('GYRO_Z')
    ylabel('Value')
    
    show()

def main():
    parser()
    grapher()
    LPF()
if __name__ == "__main__":
    main()

