import pickle
import socket
import struct
import time

import cv2
import imutils
import csv
import math


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
addr = ("127.0.0.1", 4444)

#
try:
    with open('../../conf/server.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader, None)
        conf = next(reader, None)
        addr = (conf[0], int(conf[1]))
except:
    print("no conf found, using default")

print(addr)
BUFSIZE = 1024

vid = cv2.VideoCapture(0)

while True:

    ret, frame = vid.read()
    frame = imutils.resize(frame, width=640)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]  # change number for imgencode size
    result, imgencode = cv2.imencode(".jpg", frame, encode_param)

    start = time.time()
    message = pickle.dumps(imgencode)

    client_socket.sendto(str.encode("PH"), addr)
    while message:
        bytes_sent = client_socket.sendto(message[:BUFSIZE], addr)
        message = message[bytes_sent:]
    client_socket.sendto(str.encode("PT"), addr)

    try:
        data, server = client_socket.recvfrom(3)
        end = time.time()
        elapsed = end - start
        dec = data.decode("utf-8")
        print(f'{dec} {elapsed}')
        cv2.imshow('frame', frame)
    except socket.timeout:
        print('REQUEST TIMED OUT')

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
