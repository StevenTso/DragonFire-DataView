#Program to store the arrays and print them

import binascii

ACCEL_X = []
ACCEL_Y = []
ACCEL_Z = []
GYRO_X = []
GYRO_Y = []
GYRO_Z = []

num_lines = sum(1 for line in open('data.csv'))
f = open('data.csv', 'r')
for var0 in range(0, num_lines):
	line = f.readline();

	parsed_line = line.split(',');	
	parsed_line[5] = parsed_line[5].rstrip();

	ACCEL_X.append(binascii.hexlify(parsed_line[0]));
	ACCEL_Y.append(binascii.hexlify(parsed_line[1]));
	ACCEL_Z.append(binascii.hexlify(parsed_line[2]));
	GYRO_X.append(binascii.hexlify(parsed_line[3]));
	GYRO_Y.append(binascii.hexlify(parsed_line[4]));
	GYRO_Z.append(binascii.hexlify(parsed_line[5]));
	
print ACCEL_X;
print ACCEL_Y;
print ACCEL_Z;
print GYRO_X;
print GYRO_Y;
print GYRO_Z;

