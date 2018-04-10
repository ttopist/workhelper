#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import hashlib   
import time
from datetime import datetime
from datetime import timedelta
import urllib.request
import urllib.parse
headers={'content-type':'application/xml'}
param = urllib.parse.urlencode({'beginDate':'2017-11-06','endDate':'2017-11-07'})
param = urllib.parse.urlencode({'starttime':'2017-12-16','apptype':'ios','datatype':'pv','timestep':'hour'})
resparam = '{"beginDate":"2017-11-06 00:00:00","endDate":"2017-11-09 00:00:00"}'
resparam = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:q0="http://test.demo1/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchem-instance">  
<soapenv:Body>  
	<querySale>  
		<userInterFace>
  			<enciphertype>md5</enciphertype>
  			<id>15</id>
  			<password>223321</password>
  			<sign>%s</sign>
  			<timestamp>%s</timestamp>
  			<username>mobileteam</username>
		</userInterFace>   
		<date>2017-12-30</date>
	</querySale>  
</soapenv:Body>  
</soapenv:Envelope>  
'''
timestamps=int(time.time())*1000;
m2 = hashlib.md5() 
m2.update(('2017-12-30mobileteam223321998055654ii'+str(timestamps)).encode('utf-8'))
signs=m2.hexdigest()
print(resparam%(signs,timestamps))

req = urllib.request.Request(url='http://10.101.173.66:8585/webInterface5/services/saleService?wsdl'
	,method='POST'
	#,data=param.encode('utf-8')
	,data=(resparam%(signs,timestamps)).encode('utf-8')
	,headers=headers)
proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
try:
	#resp = urllib.request.urlopen(req,timeout=1).read()
	resp = opener.open(req,timeout=30).read()
	print(resp.decode('utf-8'))
except urllib.error.HTTPError as e:  
	str = e.read();
	print('web error',e.code , e.reason, e.geturl(),sep='\n' )
	print(str.decode('utf-8'))
