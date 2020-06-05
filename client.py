import socket
import dnslib

domain = input("Введите доменное имя \n")
t = input("Введите тип записи \n")
address = dnslib.DNSRecord(q=dnslib.DNSQuestion(domain, dnslib.QTYPE.reverse[t]))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(address.pack(), ("localhost", 53))
client_socket.close()
