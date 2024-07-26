import csv
import serial
import time

ser = serial.serial_for_url('COM4', baudrate=115200, timeout=1)

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print("Start gesture in", i)
        time.sleep(1)
    print("Start gesture now!")

def log_gesture(duration):
    start_time = time.time()
    gesture_data = []
    while time.time() - start_time < duration:
        line = ser.readline().decode().strip()
        if line:
            data = line.split(',')
            if len(data) == 11:  # Ensure correct number of values received
                flex_data = [int(value) for value in data[:5]]
                imu_data = [int(value) for value in data[5:]]
                gesture_data.append(flex_data + imu_data)
        time.sleep(0.5)
    return gesture_data

gesture_id = input('Enter the id of the gesture: ')
gesture_name = input("Enter the name of this gesture: ")  
countdown(3)
gesture_data = log_gesture(5)  
i = 0
with open('gesture_data_test_extra.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    if csvfile.tell() == 0:  # Check if the file is empty
        csv_writer.writerow(['id', 'flex0', 'flex1', 'flex2', 'flex3', 'flex4', 'ax', 'ay', 'az', 'gx', 'gy', 'gz','gesture'])
    i+=1
    for data_row in gesture_data:
        csv_writer.writerow([gesture_id] + data_row + [gesture_name] )

ser.close()

print("Gesture data logged successfully.")


