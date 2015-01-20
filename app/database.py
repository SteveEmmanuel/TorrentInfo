import sqlite3

conn = sqlite3.connect('database/torrents.db')
c = conn.cursor()
details = {}
tracker = "tracker.openbittorrent.com"
torrents = {}

def database_query(a,b):
        print "database query"
        for row in c.execute('SELECT rowid,* FROM torrents where rowid between ? and ?',(a,b)):
            #print "----",row[0]
            rowid = (row[0]%10)-1
            torrents[rowid]  = {'name': row[1],
                                'info_hash' :row[3]
                               }  
        print torrents
        return render_template("index.html",
                           title='TorrentsInfoLeecher',
                           torrents=torrents)
