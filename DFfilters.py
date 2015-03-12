from scipy.signal import lfilter, firwin
class filters:
	LPF_cut_off_freq = 200
	LPF_numtaps = 40
	SMA_n = 5
	EMA_a = 0.5
	MA_x_prev = 0.5
	MA_x_cur = 0.5

	def LPF_Default_Cut_Off(self):
		return 2
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

	def LPF_Get_Freq_Limit(self):
		return 500

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
		output_data = []

		while(i<length):
			if(i<n):
				val = dataset.pop(0)
				total+=val
				output_data.append(float(val))
				queue_n.append(val)
			elif(i==n):
				val = dataset.pop(0)
				total+=val
				output_data.append(float(total/(n+1)))
			else:
				val = dataset.pop(0)
				total+=val
				total-=queue_n.pop(0)
				output_data.append(float(total/(n+1)))
				queue_n.append(val)
			i+=1

		return output_data

	def Simple_Moving_Average(self, data, n):
		output_data = []

		if(type(data[0])==list):
			ACCEL_X = data[0]
			ACCEL_Y = data[1]
			ACCEL_Z = data[2]
			GYRO_X = data[3]
			GYRO_Y = data[4]
			GYRO_Z = data[5]
		else:
			ACCEL_X = data[0].tolist()
			ACCEL_Y = data[1].tolist()
			ACCEL_Z = data[2].tolist()
			GYRO_X = data[3].tolist()
			GYRO_Y = data[4].tolist()
			GYRO_Z = data[5].tolist()

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

	def EMA_Default_A(self):
		return 0.5;

	def EMA_Get_A(self):
		global EMA_a
		return self.EMA_a

	def EMA_Set_A(self, a):
		global EMA_a
		EMA_a = a

	def EMA_Algo(self, dataset, a):
		length = len(dataset)
		pre_val = None
		cur_val = None
		output_data = []

		cur_val = dataset.pop(0)
		pre_val = cur_val

		output_data.append(cur_val)
		i = 1

		while(i<length):
			val = dataset.pop(0)
			cur_val = (a*val) + (1-a)*(pre_val)
			output_data.append(float(cur_val))
			pre_val = cur_val
			i+=1

		return output_data

	def Exponential_Moving_Average(self, data, a):
		output_data = []

		if(type(data[0])==list):
			ACCEL_X = data[0]
			ACCEL_Y = data[1]
			ACCEL_Z = data[2]
			GYRO_X = data[3]
			GYRO_Y = data[4]
			GYRO_Z = data[5]

		else:
			ACCEL_X = data[0].tolist()
			ACCEL_Y = data[1].tolist()
			ACCEL_Z = data[2].tolist()
			GYRO_X = data[3].tolist()
			GYRO_Y = data[4].tolist()
			GYRO_Z = data[5].tolist()

		ACCEL_X_filtered_signal = self.EMA_Algo(ACCEL_X, a)
		ACCEL_Y_filtered_signal = self.EMA_Algo(ACCEL_Y, a)
		ACCEL_Z_filtered_signal = self.EMA_Algo(ACCEL_Z, a)
		GYRO_X_filtered_signal = self.EMA_Algo(GYRO_X, a)
		GYRO_Y_filtered_signal = self.EMA_Algo(GYRO_Y, a)
		GYRO_Z_filtered_signal = self.EMA_Algo(GYRO_Z, a)

		output_data.append(ACCEL_X_filtered_signal)
		output_data.append(ACCEL_Y_filtered_signal)
		output_data.append(ACCEL_Z_filtered_signal)
		output_data.append(GYRO_X_filtered_signal)
		output_data.append(GYRO_Y_filtered_signal)
		output_data.append(GYRO_Z_filtered_signal)

		return output_data

	def MA_Default_Prev(self):
		return 0.5

	def MA_Default_Cur(self):
		return 0.5

	def MA_Get_Prev(self):
		global MA_x_prev
		return self.MA_x_prev

	def MA_Get_Cur(self):
		global MA_x_cur
		return self.MA_x_cur

	def MA_Set_Prev(self, value):
		global MA_x_prev
		MA_x_prev = value

	def MA_Set_Cur(self, value):
		global MA_x_cur
		MA_x_cur = value

	def Moving_Average(self, data, x):
		output_data = []
		if(type(data[0])==list):
			ACCEL_X = data[0]
			ACCEL_Y = data[1]
			ACCEL_Z = data[2]
			GYRO_X = data[3]
			GYRO_Y = data[4]
			GYRO_Z = data[5]
		else:
			ACCEL_X = data[0].tolist()
			ACCEL_Y = data[1].tolist()
			ACCEL_Z = data[2].tolist()
			GYRO_X = data[3].tolist()
			GYRO_Y = data[4].tolist()
			GYRO_Z = data[5].tolist()

		ACCEL_X_filtered_signal = self.EMA_Algo(ACCEL_X, x)
		ACCEL_Y_filtered_signal = self.EMA_Algo(ACCEL_Y, x)
		ACCEL_Z_filtered_signal = self.EMA_Algo(ACCEL_Z, x)
		GYRO_X_filtered_signal = self.EMA_Algo(GYRO_X, x)
		GYRO_Y_filtered_signal = self.EMA_Algo(GYRO_Y, x)
		GYRO_Z_filtered_signal = self.EMA_Algo(GYRO_Z, x)

		output_data.append(ACCEL_X_filtered_signal)
		output_data.append(ACCEL_Y_filtered_signal)
		output_data.append(ACCEL_Z_filtered_signal)
		output_data.append(GYRO_X_filtered_signal)
		output_data.append(GYRO_Y_filtered_signal)
		output_data.append(GYRO_Z_filtered_signal)

		return output_data