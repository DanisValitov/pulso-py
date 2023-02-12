import socket, cv2, pickle, struct
import pickle
import socket
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 4444))
# sep = "s->"
while True:
    data = b""
    # header_received = False
    while True:
        packet, address = server_socket.recvfrom(1024)
        if len(packet) == 2:
            pos = packet.decode("utf-8")
            # print(pos)
            if pos == "PT":
                print("stop")
                break
            elif (pos) == "PH":
                # header_received = True
                print("start")
            else:
                data += packet
        else:
            data += packet
    print("data len: ", len(data))
    try:
        frame = pickle.loads(data)
        image = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)
        server_socket.sendto(str.encode("ok"), address)
        # cv2.imshow("RECEIVING VIDEO", image)
    except:
        print("failed to operate frame")
        server_socket.sendto(str.encode("bad"), address)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

server_socket.close()
cv2.destroyAllWindows()
