import requests
import socket
import pickle
import dnslib
import time
import sys

cache = {}
cache_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cache_socket.bind(('localhost', 53))
cache_socket.settimeout(1)
request_socket.settimeout(1)

with open('cache.txt', 'rb') as cache_file:
    try:
        cache = pickle.load(cache_file)
        for i in cache:
            for j in cache[i]:
                _, ttl = cache[i][j]
                if ttl < int(time.time()):
                    del cache[i][j]
    except RuntimeError:
        pass
    except EOFError:
        pass


def get_info_in_cache():
    try:
        data, address = cache_socket.recvfrom(512)
        if data:
            processed_data = dnslib.DNSRecord.parse(data)
            for question in processed_data.questions:
                print(question)
                if (question.qname in cache) and \
                        (question.qtype in cache[question.qname]):
                    info, ttl = cache[question.qname][question.qtype]
                    print('Info from cache')
                    print(info)
                else:
                    google_dns_server = ("8.8.4.4", 53)
                    request_socket.sendto(processed_data.pack(),
                                          google_dns_server)
    except OSError:
        pass


def get_info_in_google_dns():
    try:
        data, address = request_socket.recvfrom(512)
        current_time = int(time.time())
        if data:
            processed_data = dnslib.DNSRecord.parse(data)
            print(processed_data)
            for question in processed_data.rr:
                cache[question.rname] = {question.rtype: (processed_data, current_time + question.ttl)}
        for i in cache:
            for j in cache[i]:
                _, ttl = cache[i][j]
                if ttl < int(time.time()):
                    del cache[i][j]
    except OSError:
        pass


print("Server is running")
try:
    while True:
        get_info_in_cache()
        time.sleep(0.25)
        get_info_in_google_dns()
except Exception as e:
    print(e)
finally:
    cache_socket.close()
    request_socket.close()
    with open('cache.txt', 'wb') as cache_file:
        pickle.dump(cache, cache_file)
