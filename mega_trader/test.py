import socket
import quickfix as fix


def logon_msg():
    logon = fix.Message()
    logon.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
    logon.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
    logon.setField(fix.Username("AP"))
    logon.setField(fix.EncryptMethod(0))
    logon = logon.toString()
    logon = bytes(logon, encoding="utf-8")
    return logon


TCP_IP = '192.168.6.107'
TCP_PORT = 2002
BUFFER_SIZE = 1024

msg = logon_msg()
print("send %s" % msg)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendto(msg, (TCP_IP, TCP_PORT))
data, addr = s.recvfrom(BUFFER_SIZE)
print("received %s" % data)
# s.close()

# print("received data: %s" % data)
# 8=FIXT.1.1\x019=50\x0135=A\x0149=BM\x0156=MT\x0134=1\x01924=1\x01108=1\x011137=FIX.5.0SP2\x0110=041\x01
import socket
#
# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
# MESSAGE = "Hello, World!"
#
# print("UDP target IP:", UDP_IP)
# print("UDP target port:", UDP_PORT)
# print("message:", MESSAGE)
#
# sock = socket.socket(socket.AF_INET,  # Internet
#                      socket.SOCK_DGRAM)  # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
import sys

# UDP_IP_ADDRESS = "192.168.6.107"
# UDP_PORT_NO = 2002
# Message = "8=FIXT.1.1DSOH 9=6935=A34=19949=ap52=20180907-06:49:00.00056=mtm98=0108=201137=910=036"
# address = (UDP_IP_ADDRESS, UDP_PORT_NO)
#
#
# def receive():
#     sock = socket.socket(socket.AF_INET,  # Internet
#                          socket.SOCK_DGRAM)  # UDP
#     sock.bind(("127.0.0.1", 9990))
#
#     while True:
#         data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#         print("received message:", data)
#
#
# def send():
#     clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     clientSock.send(bytes(Message, encoding="utf-8"),)
#     clientSock.close()
#
#
# # receive()
# send()
