#! /usr/bin/python

import requests
import sys
import re

COJ_URL = "http://coj.uci.cu/contest/cscoreboard.xhtml?cid={}&ungroup"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, "El script toma como parametro el contestId (cid=X en la URL del scoreboard de COJ)"
	else:
		contestId = sys.argv[1]
		r = requests.get(COJ_URL.format(contestId))
		for position, (team, problems, penalty) in enumerate(re.findall('<tr>.*?class="team".*?title="(8camparg..).*?".*?</td>.*?<td><a.*?>(.*?)</a>.*?<td>(.*?)</td>.*?</tr>', r.text, re.DOTALL)):
			sys.stdout.write(",".join([str(position+1) ,team, problems, penalty]))
			sys.stdout.write("\n")
		
