import pickle
import socket
import struct
import time

import cv2
import imutils
import csv

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
addr = ("127.0.0.1", 4444)

# try:
#     with open('../../conf/server.csv', newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=';')
#         headers = next(reader, None)
#         conf = next(reader, None)
#         addr = (conf[0], int(conf[1]))
# except:
#     print("no conf found, using default")

print(addr)
BUFSIZE = 1024

vid = cv2.VideoCapture(0)

while True:

    ret, frame = vid.read()
    frame = imutils.resize(frame, width=640)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]  # change number for imgencode size
    result, imgencode = cv2.imencode(".jpg", frame, encode_param)

    a = pickle.dumps(imgencode)
    message = struct.pack("Q", len(a)) + a
    length = len(message)
    start = time.time()
    while message:
        bytes_sent = client_socket.sendto(message[:BUFSIZE], addr)
        message = message[bytes_sent:]
    try:
        data, server = client_socket.recvfrom(2)
        end = time.time()
        elapsed = end - start
        dec = data.decode("utf-8")
        print(f'{dec} {elapsed}')
    except socket.timeout:
        print('REQUEST TIMED OUT')

    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
