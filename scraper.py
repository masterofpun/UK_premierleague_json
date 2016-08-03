import requests, requests_cache, json, dateutil.parser, sqlite3

requests_cache.install_cache('premierleague')
req = requests.Session()

bLink = 'http://www.premierleague.com/match/'
m = 5946

headers = {'User-Agent':'Python script gathering some data for research, will poll once a day after an initial dump; contact at: reddit.com/u/hypd09', 'Accept-Encoding': 'gzip', 'Content-Encoding': 'gzip'}

#attendance,duration,events,season,week,level,ground_city,ground_name,teamA_halftimeScore,teamB_halftimeScore,kickoff_time,official,outcome,teamA_team_score,teamA_team_name,teamA_team_abbr,teamB_team_score,teamB_team_name,teamB_team_abbr

DB_FILE = 'data.sqlite'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS data (matchData)")

while(m<12495):
    m += 1
    link = bLink+str(m)
    print(m)

    siteData = req.get(link,headers=headers).text
    
    data = None
    try:
        data = siteData.split("data-fixture='")[1].split("'>")[0]
        jdata = json.loads(data)
    except IndexError:
        jdata = {}

        
    if len(jdata.keys())>0 and len(jdata.keys())<17:
        print('doh',m)
        break;
    
    c.execute('INSERT INTO data VALUES (?)',[json.dumps(jdata,sort_keys=True)])


conn.commit()
c.close()
