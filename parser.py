class parse:
	num_lines = 0
	OriginalData = []
	ModifiedData = []

	def GetLineCount(self, path):
		stringPath = ''.join(path)
		return 	sum(1 for line in open(stringPath, 'r'))

	#Parses file and puts it into OriginalData in the form 	ACCEL_X[0], ACCEL_Y[0], ACCEL_Z[0], GYRO_X[0], GYRO_Y[0], GYRO_Z[0]

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

			ACCEL_X.append(int(parsed_line[0]));
			ACCEL_Y.append(int(parsed_line[1]));
			ACCEL_Z.append(int(parsed_line[2]));
			GYRO_X.append(int(parsed_line[3]));
			GYRO_Y.append(int(parsed_line[4]));
			GYRO_Z.append(int(parsed_line[5]));

		self.OriginalData.append(ACCEL_X)
		self.OriginalData.append(ACCEL_Y)
	
		Iterator = []
		Formatted_Data = []
		ACCEL_X = data[0]
		ACCEL_Y = data[1]
		ACCEL_Z = data[2]
		GYRO_X = data[3]
		GYRO_Y = data[4]
		GYRO_Z = data[5]

		length = len(data[0])
		for i in range(0, length):
			Iterator.append(i)

		Formatted_Data.append("ACCEL_X |  ACCEL_Y  |  ACCEL_Z   |   GYRO_X  |   GYRO_Y   |   GYRO_Z  |\n")
		for var in Iterator:
			ax = str(ACCEL_X[var]).zfill(5) + "    |    "
			ay = str(ACCEL_Y[var]).zfill(5) + "    |    "
			az = str(ACCEL_Z[var]).zfill(5) + "    |    "
			gx = str(GYRO_X[var]).zfill(5) + "    |    "
			gy = str(GYRO_Y[var]).zfill(5) + "    |    "
			gz = str(GYRO_Z[var]).zfill(5) + "   |"
			newLine = ax + ay + az + gx + gy + gz
			Formatted_Data.append(newLine)

		return Formatted_Data