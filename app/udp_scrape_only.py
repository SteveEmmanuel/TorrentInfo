import socket
import struct
from random import randrange 
from urllib import urlopen

port = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def create_connect_packet(tracker,info_hash):
    connection_id = 0x41727101980
    transaction_id = randrange(1,65535)
    print "connection_id:",connection_id,"info_hash",info_hash
    scrape_packet = struct.pack("!QLL",connection_id, 2, transaction_id) +info_hash.decode('hex')
    return scrape_response(scrape_packet, transaction_id ,tracker)

def scrape_response(scrape_packet, transaction_id,tracker):
    client_socket.connect((tracker, port))
    client_socket.send(scrape_packet)
    scrape_response_packet = client_socket.recv(2048)
    print "scrape_response entered"
    if len(scrape_response_packet)<8:
        print "scrape_response :error1"
        raise RuntimeError("Wrong response length getting connection id: %s " % len(scrape_response_packet))
    else:
        print "scrape_response :else"
        action = struct.unpack_from("!i", scrape_response_packet)[0]
        if action == 0x2:
            print "scrape_response :else:if",len(scrape_response_packet)
            #action,transaction_id,seeds,complete,leeches = struct.unpack("!LLLLL",scrape_response_packet)
            index = 8
            seeds, completed, leechers = struct.unpack(">LLL", scrape_response_packet[8:20])
	    #print "action:",action,"transaction_id:",transaction_id
            print "seeds:",seeds,"leechers:",leechers,"completed",completed
            #print "seeds:",seeds1,"leeches:",leeches1
            return {'seeds':seeds, 'leechers':leechers, 'completed':completed }
        elif action == 0x3:
            print "scrape_response :else:elif"
            error = struct.unpack_from("!s", buf, 8)
	    raise RuntimeError("Error while scraping: %s" % error)
	else:
            print "scrape_response :else:else ",action
