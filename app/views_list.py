from flask import render_template
from app import app
from udp_scrape import create_connect_packet
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    conn = sqlite3.connect('database/torrents.db')
    c = conn.cursor()
    a=1
    b=3
    details = {}
    tracker = "tracker.openbittorrent.com"
    torrents = {}
    
    for row in c.execute('SELECT rowid,* FROM torrents where rowid between ? and ?',(a,b)):
        print "yesy",row[2]
        rowid = (row[0]%10) - 1
        details[rowid] = create_connect_packet(tracker, row[3])
        torrents[rowid] = {'name': row[1],
                           'seeds': details[rowid]['seeds'],
                           'leechers': details[rowid]['leechers'],  
                           'completed': details[rowid]['completed']}
        

    print torrents
    #details=create_connect_packet(tracker, info_hash1)

    seeds = details[1]['seeds']
    leechers = details[1]['leechers']
    completed = details[1]['completed']

    print seeds,leechers
    s = {'seeds': seeds}
    l = {'leechers': leechers}
    c = {'completed': completed}      
    
    return render_template("index.html",
                           title='TorrentsInfoLeecher',
                           torrents=torrents)
