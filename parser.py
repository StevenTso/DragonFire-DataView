#Program to store the arrays and print them

from pylab import *

import binascii

ACCEL_X = []
ACCEL_Y = []
ACCEL_Z = []
GYRO_X = []
GYRO_Y = []
GYRO_Z = []

num_lines = sum(1 for line in open('data.txt'))
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
show()

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

show()