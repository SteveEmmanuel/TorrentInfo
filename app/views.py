import os
from flask import Flask
from flask import render_template
from flask import request
from scrape_final import scrape
from sqlalchemy import *

app = Flask(__name__)


 """
@app.before_request
def before_request():
    g.db = sqlite3.connect('database/torrents_small.db')

@app.teardown_request
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
"""

 
@app.route('/',methods=['GET', 'POST'])
@app.route('/index')
def index():
    """
    c = g.db.cursor()
    """
    engine = create_engine(os.path.join(os.environ["OPENSHIFT_MYSQL_DB_URL"], 'tinfo'))
    conn = engine.connect()
    metadata = MetaData(engine)
    t = Table('torrents_small', metadata, autoload=True)
    details = {}
    tracker = "tracker.openbittorrent.com"
    torrents = {}
    a=0
    b=10
    
    
    if request.args.get('submit') is not None:
            arg = request.args.get('submit').split('&',3)

            mode = arg[0].split('=',2)
            value1 = arg[1].split('=',2)
            a = int(value1[1])
            value2 = arg[2].split('=',2)
            b = int(value2[1])
            m = int(mode[1])
            if m == 0:#prev button
                a = a-10
                b = b-10
                if a < 0:
                    a = 0
                    b = 10
            elif m == 1:#next button
                a = a+10
                b = b+10
                    

    
    """
    for row in c.execute('SELECT rowid,* FROM torrents_small where rowid between ? and ?',(a,b)):
        rowid = (row[0]%10)-1
        torrents[rowid]  = {'name': row[1],
                            'info_hash' :row[2],
                            'start' : a,
                            'end' : b
                           }
   """
    
    s = select([t]).where(and_(t.c.row >= a,t.c.row <= b))
    result = conn.execute(s)
    for row in result:
        print row
        rowid = (row[0]%10)-1
        torrents[rowid]  = {'name': row[1],
                            'info_hash' :row[2],
                            'start' : a,
                            'end' : b
                           }
        
    
        
    if a == 0:
        a=10
        b=20
        
    #print torrents
    return render_template("index.html",
                           title='TorrentsInfoLeecher',
                           torrents=torrents)        
                
    if __name__ == "__main__":
    app.run(debug = "True")            
                
                
       
        
@app.route('/info', methods=['GET', 'POST'])
def click():
    if request.method == 'GET':
        #tracker = "udp://tracker.openbittorrent.com:80"
        tracker = "http://bttracker.crunchbanglinux.org:6969/announce"
        details = scrape(tracker, request.args.get('id'))
        return render_template('result.html', details= details)



      
        
    
