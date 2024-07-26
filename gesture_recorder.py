import csv
import serial
import time

def log_gesture(duration, serial_port):
    start_time = time.time()
    gesture_data = []
    while time.time() - start_time < duration:
        line = serial_port.readline().decode().strip()
        if line:
            data = line.split(',')
            if len(data) == 11:  # Ensure correct number of values received
                flex_data = [int(value) for value in data[:5]]
                imu_data = [int(value) for value in data[5:]]
                gesture_data.append(flex_data + imu_data)
        time.sleep(0.1)  # Reduced sleep time to capture data more frequently
    return gesture_data

def save_gesture(gesture_data):
    while len(gesture_data) != 10:
        gesture_data.append(gesture_data[-1])
    with open('gesture_data_test.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if the file is empty
            csv_writer.writerow(['flex0', 'flex1', 'flex2', 'flex3', 'flex4', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
        for data_row in gesture_data:
            csv_writer.writerow(data_row)

    
    



# trying this just to see the if the flow is as it should be (since i dont have the glove, cant use COM4)


# import csv
# import time
# import random

# def log_gesture(duration):
#     start_time = time.time()
#     gesture_data = []
#     count = 0
#     max_count = 10  # Set the maximum number of rows
#     while time.time() - start_time < duration and count < max_count:
#         # Simulate data generation for testing without hardware
#         data = [random.randint(0, 1023) for _ in range(11)]
#         if len(data) == 11:
#             flex_data = [int(value) for value in data[:5]]
#             imu_data = [int(value) for value in data[5:]]
#             gesture_data.append(flex_data + imu_data)
#             count += 1
#         time.sleep(0.5)  # Adjust sleep time if needed
#     return gesture_data


# def save_gesture(gesture_id, gesture_data):
#     with open('gesture_data_test.csv', 'a', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         if csvfile.tell() == 0:  # Check if the file is empty
#             csv_writer.writerow(['id', 'flex0', 'flex1', 'flex2', 'flex3', 'flex4', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
#         for data_row in gesture_data:
#             csv_writer.writerow([gesture_id] + data_row)
