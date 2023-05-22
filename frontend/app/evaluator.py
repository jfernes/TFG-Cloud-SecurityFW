import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sys

lw = 0.05
mw = 0.15
hw = 0.30
cw = 0.5
#apikey = '8d10e22cb16454217a4f6fb5f7036618' #Joaquin
apikey = 'cfe941edfc9a1663c0071715fb9dbf8d' #Julian

def evaluate(cvss):
    #todos los cvss encontrados de todas las vulnerabilidades
    low = 0.0
    nlow = 0
    med = 0.0
    nmed = 0
    high = 0.0
    nhigh = 0
    crit = 0.0
    ncrit = 0
    for i in cvss:
        if 0.0 <= float(i) <= 3.9:
            nlow += 1
            low += float(i)
        elif 4.0 <= float(i) <= 6.9:
            nmed += 1
            med += float(i)
        elif 7.0 <= float(i) <= 8.9:
            nhigh += 1
            high += float(i)
        elif 9.0 <= float(i) <= 10:
            ncrit += 1
            crit += float(i)
    low = ((low/nlow) - 0)/(3.9 - 0) if nlow != 0 else 0
    med = ((med/nmed) - 4.0)/(6.9 - 4.0) if nmed != 0 else 0
    high = ((high/nhigh) - 7.0)/(8.9 - 7.0) if nhigh != 0 else 0
    crit = ((crit/ncrit) - 9.0)/(10.0 - 9.0) if ncrit != 0 else 0

    trustv = low * lw + med * mw + high * hw + crit * cw

    #si queremos sumar un extra por numero de vulnerabilidades y que saturen si llegan al tope de su peso
    #para las low sumamos 0.05 por cada 3 vulnerabilidades
    trustv += ((nlow) // 3) * 0.05
    # para cada las med 0.1 por cada 3 vuln
    trustv += ((nmed) // 3) * 0.1
    # para las high 0,1 por cada 2
    trustv += ((nhigh) // 2) * 0.1
    # para crit 0.1 por cada 1
    trustv += (ncrit) * 0.2
    if trustv > 1:
        trustv = 1

    trustv = 1 - trustv
    return trustv


def getCVSS(techs):
    cvss = []
    for tech in techs:
        ids = []
        
        url = 'https://vuldb.com/?api'  # url endpoint
        post_fields = {'apikey': apikey, 'search': tech}  # request

        request = Request(url, urlencode(post_fields).encode())
        json_string = urlopen(request).read().decode()
        data = json.loads(json_string)
        for i in data['result']:
            ids.append(i['entry']['id'])
        print(ids)

        for id in ids:
            post_fields = {'apikey': apikey, 'id': id, 'fields': 'vulnerability_cvss2_vuldb_basescore'}
            request = Request(url, urlencode(post_fields).encode())
            json_string = urlopen(request).read().decode()
            data = json.loads(json_string)
            for i in data['result']:
                v = i['vulnerability']['cvss2']['vuldb']['basescore']
                cvss.append(v)
                
    if 0.0 in cvss:
        cvss.remove('0.0')
    return evaluate(cvss)
