from scipy.signal import lfilter, firwin
class filters:
	LPF_cut_off_freq = 200
	LPF_numtaps = 40
	
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

	def Simple_Moving_Average(self):
		print "SMA"

	def Exponential_Moving_Average(self):
		print "EMA"

	def Weighted_Mean(self):
		print "Weighted Mean"