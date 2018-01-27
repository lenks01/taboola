#!/usr/bin/python

import json 
import sys
import urllib2
import base64

user = 'Admin'
password = 'admin'
jenkinsUrl = 'http://localhost:9080/job/'


def urlopen(url, data=None):
    '''Open a URL using the urllib2 opener.'''
    request = urllib2.Request(url, data)
    base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    return response



if len( sys.argv ) > 1 :
    jobName = sys.argv[1]
else :
    sys.exit(1)

try:
    jenkinsStream   = urlopen(jenkinsUrl + jobName + "/lastBuild/api/json")
except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code) 
    print "      (job name [" + jobName + "] probably wrong)"
    sys.exit(2)

try:
    buildStatusJson = json.load( jenkinsStream )
except:
    print "Failed to parse json"
    sys.exit(3)

if buildStatusJson.has_key( "result" ):      
    print "[" + jobName + " #" + str(buildStatusJson["number"]) + "]: " + buildStatusJson["result"] 
    if buildStatusJson["result"] != "SUCCESS" :
		exit(4)
else:
	sys.exit(5)

sys.exit(0)