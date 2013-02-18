from scipy.signal import lfilter, firwin
class filters:
	LPF_cut_off_freq = 200
	LPF_numtaps = 40
	SMA_n = 5
	
	def LPF_Default_Cut_Off(self):
		return 200

	def LPF_Default_NumTaps(self):
		return 40

	def LPF_Get_Cut_Off(self):
		global LPF_cut_off_freq
		return self.LPF_cut_off_freq

	def LPF_Get_NumTaps(self):
		global LPF_numtaps
		return self.LPF_numtaps

	def LPF_Set_Cut_Off(self, value):
		global LPF_cut_off_freq
		LPF_cut_off_freq = value

	def LPF_Set_NumTaps(self, value):
		global LPF_numtaps
		LPF_numtaps = value

	def	LPF(self, data, cut_off_freq, numtaps):
		global LPF_cut_off_freq, LPF_numtaps
		LPF_cut_off_freq = int(cut_off_freq)
		LPF_numtaps = int(numtaps)

		output_data = []
		sampling_rate = 1000.0

		ACCEL_X = data[0]
		ACCEL_Y = data[1]
		ACCEL_Z = data[2]
		GYRO_X = data[3]
		GYRO_Y = data[4]
		GYRO_Z = data[5]
		fir_coeff = firwin(LPF_numtaps, LPF_cut_off_freq/(sampling_rate/2))
		
		ACCEL_X_filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_X)
		ACCEL_Y_filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_Y)
		ACCEL_Z_filtered_signal = lfilter(fir_coeff, 1.0, ACCEL_Z)
		GYRO_X_filtered_signal = lfilter(fir_coeff, 1.0, GYRO_X)
		GYRO_Y_filtered_signal = lfilter(fir_coeff, 1.0, GYRO_Y)
		GYRO_Z_filtered_signal = lfilter(fir_coeff, 1.0, GYRO_Z)

		output_data.append(ACCEL_X_filtered_signal)
		output_data.append(ACCEL_Y_filtered_signal)
		output_data.append(ACCEL_Z_filtered_signal)
		output_data.append(GYRO_X_filtered_signal)
		output_data.append(GYRO_Y_filtered_signal)
		output_data.append(GYRO_Z_filtered_signal)
		return output_data

	def SMA_Default_N(self):
		return 5

	def SMA_Get_N(self):
		global SMA_n
		return self.SMA_n

	def SMA_Set_N(self, value):
		global SMA_n
		SMA_n = value

	def SMA_Algo(self, dataset, n):
		length = len(dataset)
		i = 0
		val = None
		total = 0
		queue_n = []
		output_algodata = []

		while(i<length):
			if(i<=n):
				val = dataset.pop(0)
				total+=val
				output_algodata.append(float(val))
				queue_n.append(val)
			else:	
				val = dataset.pop(0)
				total+=val
				total-=queue_n.pop(0)
				output_algodata.append(float(total/n))
				queue_n.append(val)
			i+=1

		return output_algodata

	def Simple_Moving_Average(self, data, n):
		output_data = []

		ACCEL_X = data[0]
		ACCEL_Y = data[1]
		ACCEL_Z = data[2]
		GYRO_X = data[3]
		GYRO_Y = data[4]
		GYRO_Z = data[5]

		ACCEL_X_filtered_signal = self.SMA_Algo(ACCEL_X, n)
		ACCEL_Y_filtered_signal = self.SMA_Algo(ACCEL_Y, n)
		ACCEL_Z_filtered_signal = self.SMA_Algo(ACCEL_Z, n)
		GYRO_X_filtered_signal = self.SMA_Algo(GYRO_X, n)
		GYRO_Y_filtered_signal = self.SMA_Algo(GYRO_Y, n)
		GYRO_Z_filtered_signal = self.SMA_Algo(GYRO_Z, n)

		output_data.append(ACCEL_X_filtered_signal)
		output_data.append(ACCEL_Y_filtered_signal)
		output_data.append(ACCEL_Z_filtered_signal)
		output_data.append(GYRO_X_filtered_signal)
		output_data.append(GYRO_Y_filtered_signal)
		output_data.append(GYRO_Z_filtered_signal)

		return output_data

	def Exponential_Moving_Average(self):
		print "EMA"

	def Weighted_Mean(self):
		print "Weighted Mean"