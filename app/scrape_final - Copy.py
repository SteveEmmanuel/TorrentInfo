import socket
import struct
from random import randrange 
from urllib import urlopen
from urlparse import urlparse, urlunsplit





def scrape(tracker,info_hash):
    tracker = tracker.lower()
    parsed_tracker = urlparse(tracker)
    if parsed_tracker.scheme == "udp":
	    return scrape_udp(parsed_tracker ,info_hash)

    if parsed_tracker.scheme in ["http", "https"]:
	    if "announce" not in tracker:
		    raise RuntimeError("%s doesnt support scrape" % tracker)
	    parsed_tracker = urlparse(tracker.replace("announce", "scrape"))		 
	    return scrape_http(parsed_tracker, hashes)

    raise RuntimeError("Unknown tracker scheme: %s" % parsed.scheme)

def scrape_http(parsed_tracker, info_hash):
    pass

def scrape_udp(parsed_tracker, info_hash):
    connection_id = 0x41727101980
    transaction_id = randrange(1,65535)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(8)
    
    connection = (socket.gethostbyname(parsed_tracker.hostname), parsed_tracker.port)

    connect_packet = create_connect_packet(connection_id,transaction_id)
    client_socket.sendto(connect_packet, connection)
    connect_response_packet = client_socket.recvfrom(2048)[0]

    connection_id = connect_response(connect_response_packet, transaction_id)

    scrape_packet = create_scrape_packet(connection_id,transaction_id, info_hash)
    client_socket.sendto(scrape_packet, connection)
    scrape_response_packet = client_socket.recvfrom(2048)[0]

    return scrape_response(scrape_response_packet, transaction_id)



def create_connect_packet(connection_id,transaction_id):
    connect_packet = struct.pack("!QLL",connection_id, 0, transaction_id)
    return connect_packet




def connect_response(connect_response_packet, transaction_id):
    if len(connect_response_packet) < 8:
        raise RuntimeError("Wrong response length getting connection id: %s " % len(connect_response_packet))
    
    else:
        action,res_transaction_id,connection_id = struct.unpack("!LLQ",connect_response_packet)
        if res_transaction_id != transaction_id:
		raise RuntimeError("Transaction ID doesnt match in connection response! Expected %s, got %s" % (transaction_id, res_transaction_id))
	    
	if action == 0x0:
		connection_id = struct.unpack_from("!Q", connect_response_packet, 8)[0]
		return connection_id
	    
	elif action == 0x3:		
		error = struct.unpack_from("!s", connect_response_packet, 8)
		raise RuntimeError("Error while trying to get a connection response: %s" % error)


def create_scrape_packet(connection_id,transaction_id, info_hash):
    scrape_packet = struct.pack("!QLL",connection_id, 2, transaction_id) +info_hash.decode('hex')
    return scrape_packet

def scrape_response(scrape_response_packet, transaction_id):
    if len(scrape_response_packet)<8:
        raise RuntimeError("Wrong response length getting connection id: %s " % len(scrape_response_packet))
    
    else:
        action,res_transaction_id = struct.unpack("!LL",scrape_response_packet[0:8])
        if res_transaction_id != transaction_id:
		raise RuntimeError("Transaction ID doesnt match in connection response! Expected %s, got %s" % (transaction_id, res_transaction_id))
	    
        if action == 0x2:
            seeds, completed, leechers = struct.unpack(">LLL", scrape_response_packet[8:20])
            return {'seeds':seeds, 'leechers':leechers, 'completed':completed }
        
        elif action == 0x3:
            error = struct.unpack_from("!s", buf, 8)
	    raise RuntimeError("Error while scraping: %s" % error)
