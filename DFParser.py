class graphParser:
    def __init__(self, path):
        #for filePath in path:
        #   stringPath.append(filePath)
        stringPath = ''.join(path)

        global num_lines
        num_lines = sum(1 for line in open(stringPath, 'r'))

        f = open(stringPath, 'r')
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

            global ACCEL_X, ACCEL_Y, ACCEL_Z, GYRO_X, GYRO_Y, GYRO_Z    
            ACCEL_X.append(parsed_line[0]);
            ACCEL_Y.append(parsed_line[1]);
            ACCEL_Z.append(parsed_line[2]);
            GYRO_X.append(parsed_line[3]);
            GYRO_Y.append(parsed_line[4]);
            GYRO_Z.append(parsed_line[5]);

class viewParser:
    def __init__(self, path):
        global FORMATTED_DATA
        FORMATTED_DATA = []
        graphParser(path)
        for var in range(0, num_lines):
            ax = str(ACCEL_X[var]).zfill(5) + "    |    "
            ay = str(ACCEL_X[var]).zfill(5) + "    |    "
            az = str(ACCEL_X[var]).zfill(5) + "    |    "
            gx = str(ACCEL_X[var]).zfill(5) + "    |    "
            gy = str(ACCEL_X[var]).zfill(5) + "    |    "
            gz = str(ACCEL_X[var]).zfill(5) + "   |"
            newLine = ax + ay + az + gx + gy + gz
            FORMATTED_DATA.append(newLine)
