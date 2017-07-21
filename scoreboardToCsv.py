#! /usr/bin/python

import requests
import sys
import re

COJ_URL = "http://coj.uci.cu/contest/cscoreboard.xhtml?cid={}&ungroup"
COJ_URL_UPSOLVING = "http://coj.uci.cu/tables/cscoreboard3.xhtml?cid={}"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, "El script toma como parametro el contestId (cid=X en la URL del scoreboard de COJ)"
	else:
		contestId = sys.argv[1]
		r = requests.get(COJ_URL.format(contestId))
		nothing = True
		for position, (team, problems, penalty) in enumerate(re.findall('<tr>.*?class="team".*?title="(8camparg..).*?".*?</td>.*?<td><a.*?>(.*?)</a>.*?<td>(.*?)</td>.*?</tr>', r.text, re.DOTALL)):
			if nothing:
				sys.stdout.write(",".join(["Posicion" ,"Equipo", "Problemas", "Penalidad"]))
				sys.stdout.write("\n")					
				nothing = False
			sys.stdout.write(",".join([str(position+1) ,team, problems, penalty]))
			sys.stdout.write("\n")
			
		if nothing:
			# Assume upsolving
			r = requests.get(COJ_URL_UPSOLVING.format(contestId))
			sys.stdout.write(",".join(["Posicion" ,"Equipo", "Problemas"]))
			sys.stdout.write("\n")					
			for position, (team, problems) in enumerate(re.findall('<tr class=".*?">.*?<a title="(8camparg..).*?".*?</td>.*?<td>.*?</td>.*?<td>.*?<a.*?>(.*?)</a></td>.*?</tr>', r.text, re.DOTALL)):
				sys.stdout.write(",".join([str(position+1) ,team, problems]))
				sys.stdout.write("\n")
		
