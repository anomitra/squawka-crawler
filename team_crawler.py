import requests
import time
from BeautifulSoup import BeautifulSoup
import re
import pickle
from time import sleep

prog_start=time.time()

checklist_file=open("TeamsCompleted.txt","r+")
checklist=checklist_file.readlines()
num_teams_checked=len(checklist)
checklist.extend(["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""])

team_list=["Manchester United","Chelsea","Liverpool","Valencia CF","Arsenal","Tottenham Hotspur","Southampton","Manchester City","Real Madrid","Barcelona","West Ham United","Ajax","PSV","Feyenoord","Borussia Dortmund","Borussia Monchengladbach","FC Bayern Munchen","VfL Wolfsburg","Bayer 04 Leverkusen","FC Schalke 04","Atletico de Madrid","Sevilla","Valencia","Lyon","Marseille","St Etienne","Paris Saint Germain","Monaco","Juventus","Roma","Lazio","Napoli","Fiorentina","Milan","Internazionale"]
def crawl(url):
    while True:
	try:
	    r=requests.get(url)
	    return r.content
	    break
	except Exception as e:
	    print e
	    sleep(2)
	    print "Retrying!!"
base_url = "http://www.squawka.com/teams/"

all_players=[dict() for x in range(10000)]

def makeMyURL(teamname):
	teamname=teamname.lower()
	teamname=teamname.replace(" ","-")
	return base_url+teamname+"/squad"

max_time=0.0
min_time=1000.0
max_time_team=""
min_time_team=""
i=0
player_ctr=0

for team in team_list:
	cf=open("TeamsCompleted.txt","a")
	print i,num_teams_checked
	if(i<=num_teams_checked-1):
		if(team==checklist[i].strip()):
			print team+" is already crawled! Moving on.."
			i+=1
			continue
	fetch_team=time.time()
	url=makeMyURL(team)
	print "Starting to crawl "+team+" from "+url
	html = crawl(url)
	print "Crawled page!"
	soup=BeautifulSoup(html)
	player_names=soup.findAll("td", { "class" : "squad_playerphoto" })
	player_links=soup.findAll("a", { "class" : "teamstatinfo" })
	print "-----------------------------------------------"
	print "         PLAYERS   FROM    "+team
	print "-----------------------------------------------" 
	j=0
	for player in player_links:
		playerfile=open("PlayerFile.txt","a")
		namefile=open("NameFile.txt","a")
		start="<div>"
		end="</div>"
		p_name=re.search('%s(.*)%s' % (start, end),str(player_names[j])).group(1)
		start="players/"
		end="/stats/../stats\">"
		p_slug=re.search('%s(.*)%s' % (start, end),str(player)).group(1)
		namefile.write(p_name+" --- "+p_slug+"\n"	)
		j+=1
		all_players[player_ctr]['name']=p_name
		all_players[player_ctr]['slug']=p_slug
		all_players[player_ctr]['crawled']=0
		print all_players[player_ctr]['name']+" --- ",
		print all_players[player_ctr]['slug']
		pickle.dump(all_players[player_ctr],playerfile)
		playerfile.close()
		namefile.close()
		player_ctr+=1
	print ""
	time_taken=float(str(time.time()-fetch_team))
	if(time_taken>max_time):
		max_time=time_taken
		max_time_team=team
	if(time_taken<min_time):
		min_time=time_taken
		min_time_team=team
	print "Time taken: "+"%.2f"%time_taken,
	print "s"
	checklist[i-1]=team
	cf.write(team+"\n")
	cf.close()	
	i+=1
tottime=float(str(time.time()-prog_start))
print "Total time taken: "+"%.2f"%tottime,
print "s"
print "Maximum time was taken for "+max_time_team+" %.2f"%max_time,
print "s"
print "Minimum time was taken for "+min_time_team+" %.2f"%min_time,
print "s"
print all_players
all_players=[var for var in all_players if var]
print all_players
print len(all_players)
