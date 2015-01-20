import socket
import struct
from random import randrange 
from urllib import urlopen

port = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def create_connect_packet(tracker ,info_hash):
    connection_id = 0x41727101980
    transaction_id = randrange(1,65535)
    connect_packet = struct.pack("!QLL",connection_id, 0, transaction_id)
    
    tracker1 = tracker
    connection_details = connect_response(connect_packet, transaction_id,tracker1)

    connection_id = connection_details['connection_id']
    transaction_id = connection_details['transaction_id']
    #print "connection_id:",connection_id,"transaction_id:",transaction_id
    return create_scrape_packet(connection_id, transaction_id,info_hash)




def connect_response(connect_packet, transaction_id, tracker):
    client_socket.connect((tracker, port))
    client_socket.send(connect_packet)
    connect_response_packet = client_socket.recv(2048)
    if len(connect_response_packet) < 8:
        raise RuntimeError("Wrong response length getting connection id: %s " % len(connect_response_packet))
    else:
        res_action,res_transaction_id,connection_id = struct.unpack("!LLQ",connect_response_packet)
        if res_transaction_id != transaction_id:
		raise RuntimeError("Transaction ID doesnt match in connection response! Expected %s, got %s"
			% (transaction_id, res_transaction_id))

	if res_action == 0x0:
		connection_id = struct.unpack_from("!Q", connect_response_packet, 8)[0]
		return {'connection_id':connection_id, 'transaction_id':transaction_id }
	elif res_action == 0x3:		
		error = struct.unpack_from("!s", connect_response_packet, 8)
		raise RuntimeError("Error while trying to get a connection response: %s" % error)


def create_scrape_packet(connection_id, transaction_id, info_hash):
    #print "connection_id:",connection_id,"info_hash",info_hash
    scrape_packet = struct.pack("!QLL",connection_id, 2, transaction_id) +info_hash.decode('hex')
    return scrape_response(scrape_packet, transaction_id)

def scrape_response(scrape_packet, transaction_id):
    client_socket.send(scrape_packet)
    scrape_response_packet = client_socket.recv(2048)
    #print "scrape_response entered"
    if len(scrape_response_packet)<8:
        #print "scrape_response :error1"
        raise RuntimeError("Wrong response length getting connection id: %s " % len(scrape_response_packet))
    else:
        #print "scrape_response :else"
        action = struct.unpack_from("!i", scrape_response_packet)[0]
        if action == 0x2:
            #print "scrape_response :else:if",len(scrape_response_packet)
            #action,transaction_id,seeds,complete,leeches = struct.unpack("!LLLLL",scrape_response_packet)
            index = 8
            seeds, completed, leechers = struct.unpack(">LLL", scrape_response_packet[8:20])
	    #print "action:",action,"transaction_id:",transaction_id
            #print "seeds:",seeds,"leechers:",leechers,"completed",completed
            #print "seeds:",seeds1,"leeches:",leeches1
            return {'seeds':seeds, 'leechers':leechers, 'completed':completed }
        elif action == 0x3:
            #print "scrape_response :else:elif"
            error = struct.unpack_from("!s", buf, 8)
	    raise RuntimeError("Error while scraping: %s" % error)
