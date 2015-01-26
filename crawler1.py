import requests
import time
from BeautifulSoup import BeautifulSoup
import re
import pickle
from time import sleep
datafile=open("PlayerFile.txt","r+b")
playerdata=[dict() for x in range(1190)]
for i in xrange(1185):
	x=pickle.load(datafile)
	print x
	if(x):
		playerdata[i]=x
	i+=1

l=["Steven Gerrard","Luis Suarez", "Lazar Markovic"]#List of Players!

goalie_stat_dict={"App":0,"Perf":0,"CS":0,"GC":0,"SqA":0,"SPGame":0,"SPGoal":0,"ACS":0,"AP":0,"DS":0,"DL":0,"Y":0,"R":0}
goalie_stat_dict_ref={1:"App",2:"Perf",3:"CS",4:"GC",5:"SqA",6:"SPGame",7:"SPGoal",8:"ACS",9:"AP",10:"DS",11:"DL",12:"YR"}

def crawl(url):
    while True:
	try:
	    print "trying to get URL... ",
	    r=requests.get(url)
	    print "Got URL!"
	    return r.content
	    break
	except Exception as e:
	    print e
	    sleep(2)
	    print "Retrying!!"

base_url = 'http://www.squawka.com/players/'

def urlify(player,base_url):
    print "Parsing URL..",
    return base_url+player+'/stats'

with open ("path.txt", "r") as myfile:
    data=myfile.read()

check=open("players_done.txt","r")
donelist=check.readlines()
check.close()
#print "Done players are:"
#print donelist

    
for i in xrange(len(playerdata)):
    stat_dict={"App":0,"Perf":0,"GS":0,"ShtA":0,"SqA":0,"CC":0,"APA":0,"APL":0,"DW":0,"ADA":0,"DE":0,"Y":0,"R":0}
    stat_dict_ref={1:"App",2:"Perf",3:"GS",4:"ShtA",5:"SqA",6:"CC",7:"APA",8:"APL",9:"DW",10:"ADA",11:"DE",12:"YR"}
    player=playerdata[i]["slug"]
    playername=playerdata[i]["name"]
    player=player.replace(" ","-")
    #print i
    print "Fetching information for %s "%playerdata[i]['name']+"from  "+str(urlify(player,base_url))
    if(len(donelist)>i):
		if(donelist[i].strip()==player):
			print "Statistics for this player has already been fetched. Moving on.."
			continue
    print "waiting..."
    sleep(4)
    print "Sleep over!"
    html = crawl(urlify(player,base_url))
    print "Page crawled."
    parsed_html = BeautifulSoup(html)
    #print parsed_html.select(data)
    print ""
    position=parsed_html.find("h2", { "class" : "team-league" })
    start=">"
    end="</h2>"
    position=re.search('%s(.*)%s' % (start, end),str(position)).group(1)
    if (position=="Goalkeeper"):
		goalie_stat_dict={"App":0,"Perf":0,"CS":0,"GC":0,"SqA":0,"SPGame":0,"SPGoal":0,"ACS":0,"AP":0,"DS":0,"DL":0,"Y":0,"R":0}
		goalie_stat_dict_ref={1:"App",2:"Perf",3:"CS",4:"GC",5:"SqA",6:"SPGame",7:"SPGoal",8:"ACS",9:"AP",10:"DS",11:"DL",12:"YR"}
		for i in xrange(1,13):
			#print str(i)+":"
			value = parsed_html.body.find(id='stat-'+str(i)).find('span',attrs={'class':'stat'}).text
			heading = parsed_html.body.find(id='stat-'+str(i)).find('span',attrs={'class':'heading'}).text
			#print heading+' '+value
			if(i==12 or i==5 or i==4 or i==6 or i==7):
				#print int(value.split('/')[0])
				#print int(value.split('/')[1])
				if(i==12):
					goalie_stat_dict["Y"]=int(value.split('/')[0])
					stat_dict["R"]=int(value.split('/')[1])
				if(i==4 or i==6 or i==7):
					goalie_stat_dict[goalie_stat_dict_ref[i]]=float(value)
					#print goalie_stat_dict[goalie_stat_dict_ref[i]]
			else:
				value=re.sub('[^0-9]','', value)
				goalie_stat_dict[goalie_stat_dict_ref[i]]=int(value)
				#print goalie_stat_dict[goalie_stat_dict_ref[i]]
			#print goalie_stat_dict
			points=goalie_stat_dict["App"]*2+goalie_stat_dict["SPGame"]*20+goalie_stat_dict["CS"]-goalie_stat_dict["Y"]-goalie_stat_dict["R"]*3
		print playername+" %.2f"%points
		file1=open("statfile.txt","a")
		file1.write(str(playername+": %.2f"%points+"\n"))
		file1.close()
		file1=open("players_done.txt","a")
		file1.write(str(player+"\n"))
		file1.close()
		continue
    for i in xrange(1,13):
		value = parsed_html.body.find(id='stat-'+str(i)).find('span',attrs={'class':'stat'}).text
		heading = parsed_html.body.find(id='stat-'+str(i)).find('span',attrs={'class':'heading'}).text
		#print heading+' '+value
		if(i==12 or i==5):
			#print int(value.split('/')[0])
			#print int(value.split('/')[1])
			if(i==12):
				stat_dict["Y"]=int(value.split('/')[0])
				stat_dict["R"]=int(value.split('/')[1])
		else:
			value=re.sub('[^0-9]','', value)
			stat_dict[stat_dict_ref[i]]=int(value)
			#print stat_dict[stat_dict_ref[i]]
		
    if(position=="Defender"):
		points=stat_dict["App"]*2+stat_dict["GS"]*6+stat_dict["CC"]*1.75+(stat_dict["DW"]*stat_dict["App"])/15+stat_dict["ADA"]*5-stat_dict["R"]*3-stat_dict["Y"]
		print playername+": %.2f"%points

    if(position=="Midfielder"):
		points=stat_dict["App"]*2+stat_dict["GS"]*5+stat_dict["CC"]+((stat_dict["DW"]+stat_dict["APA"])*stat_dict["App"])/40+stat_dict["ADA"]*3-stat_dict["R"]*3-stat_dict["Y"]
		print playername+": %.2f"%points
		
    if(position=="Forward"):
		points=stat_dict["App"]*2+stat_dict["GS"]*4+stat_dict["CC"]+((stat_dict["ShtA"]+stat_dict["APA"]*0.9)*stat_dict["App"])/40-stat_dict["R"]*3-stat_dict["Y"]
		print playername+": %.2f"%points
    file1=open("statfile.txt","a")
    file1.write(str(playername+": %.2f"%points+"\n"))
    file1.close()
    file1=open("players_done.txt","a")
    file1.write(str(player+"\n"))
    file1.close()
print ""
print ""
    #print stat_dict
