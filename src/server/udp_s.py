import socket, cv2, pickle, struct
import pickle
import socket
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 4444))
payload_size = struct.calcsize("Q")
while True:
    data = b""
    while len(data) < payload_size:
        packet, address = server_socket.recvfrom(1024)  # 4K
        # packet, address = server_socket.recvfrom(1024)  # 4K  todo add auth
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    print("msg_size: ", msg_size, "from: ", address)

    while len(data) < msg_size:
        data += server_socket.recv(1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    try:
        frame = pickle.loads(frame_data)
        image = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)
    except:
        print("failed to operate frame")

    server_socket.sendto(str.encode("ok"), address)
    # cv2.imshow("RECEIVING VIDEO", image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

server_socket.close()
cv2.destroyAllWindows()
