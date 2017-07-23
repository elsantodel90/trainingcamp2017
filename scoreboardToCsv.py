#! /usr/bin/python

import requests
import sys
import re

COJ_URL = "http://coj.uci.cu/contest/cscoreboard.xhtml?cid={}&ungroup"
COJ_URL_UPSOLVING = "http://coj.uci.cu/tables/cscoreboard3.xhtml?cid={}"

identityFormatter = (lambda x : x)

def select(elements, l):
    return [l[i] for i in elements]

def contestToCSV(contestId, url, headers, teamnameProcessor, teamNameIndex, regex = None, jsonField = None, columns = None):
    r = requests.get(url.format(contestId))
    assert (regex is None) != (jsonField is None)
    if regex:
        rows = re.findall(regex, r.text, re.DOTALL)
        rows = map(list, rows)
    else:
        assert columns is not None
        rows = ( select(columns, map(str, r)) for r in r.json()[jsonField] )
        
    nothing = True
    for position, row in enumerate(rows):
        if nothing:
            sys.stdout.write(",".join(headers))
            sys.stdout.write("\n")                  
            nothing = False
        row[teamNameIndex] = teamnameProcessor(row[teamNameIndex])
        sys.stdout.write(",".join([str(position+1)] + row))
        sys.stdout.write("\n")
    return not nothing

def a2ojProcessor(teamHtml):
    m1 = re.search(">(8camparg..)",teamHtml)
    m2 = re.search(">(8argcamp..)",teamHtml)
    special1 = re.search(r">Galactofocas",teamHtml)
    special2 = re.search(r">man\.hernandez",teamHtml)
    if m1:
        return m1.group(1)
    elif m2:
        return "8camparg" + m2.group(1)[-2:]
    elif special1:
        return "8camparg07"
    elif special2:
        return "8camparg50"
    else:
        print teamHtml
        assert False

def ahmedAly(contestId):
    A2OJ_URL = "https://a2oj.com/get?ID={}&type=contestRows"
    contestToCSV(contestId = contestId,
                 url       = A2OJ_URL, 
                 headers   = ("Posicion" ,"Equipo", "Problemas", "Penalidad"),
                 jsonField = 'ScoreboardRows',
                 columns   = (1, 3, 4),
                 teamnameProcessor = a2ojProcessor,
                 teamNameIndex = 0,
                )
    
def coj(contestId):
    ok = contestToCSV(contestId = contestId,
                      url       = COJ_URL, 
                      headers   = ("Posicion" ,"Equipo", "Problemas", "Penalidad"),
                      regex     = '<tr>.*?class="team".*?title="(8camparg..).*?".*?</td>.*?<td><a.*?>(.*?)</a>.*?<td>(.*?)</td>.*?</tr>',
                      teamnameProcessor = identityFormatter,
                      teamNameIndex = 0,
                     )
    if not ok:
         contestToCSV(contestId = contestId,
                      url       = COJ_URL_UPSOLVING,
                      headers   = ("Posicion" ,"Equipo", "Problemas"),
                      regex     = '<tr class=".*?">.*?<a title="(8camparg..).*?".*?</td>.*?<td>.*?</td>.*?<td>.*?<a.*?>(.*?)</a></td>.*?</tr>',
                      teamnameProcessor = identityFormatter,
                      teamNameIndex = 0,
                     )

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "El script toma como parametro el judge (COJ o A2OJ) y el contestId (cid=X en la URL del scoreboard de COJ)"
        print >> sys.stderr, "Ejemplos:"
        print >> sys.stderr, sys.argv[0], "COJ", "1605"
        print >> sys.stderr, sys.argv[0], "A2OJ", "32630"
    else:
        judge = sys.argv[1]
        contestId = sys.argv[2]
        if judge == "COJ":
            coj(contestId)
        elif judge == "A2OJ":
            ahmedAly(contestId)
        else:
            print >> sys.stderr, "Juez invalido:", judge
