import socket
import dnslib

address = input('Enter address' + '\n')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(dnslib.DNSRecord.question(address).pack(), ("localhost", 53))
client_socket.close()
