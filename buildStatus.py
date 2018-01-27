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

def convertToTime(milliseconds):
    milliseconds = int(milliseconds)
    seconds=(milliseconds/1000)%60
    seconds = int(seconds)
    minutes=(milliseconds/(1000*60))%60
    minutes = int(minutes)
    hours=(milliseconds/(1000*60*60))%24
    return "%02d:%02d:%02d" % (hours, minutes, seconds)



if len( sys.argv ) > 2 :
    jobName = sys.argv[1]
    buildNumber = sys.argv[2]
else :
    print "One of the parameters is missing. Run: 'python buildStatus.py jobName buildNumber'"
    sys.exit(1)

# Distnguish between pipeline and other jobs
try:
    jenkinsStream   = urlopen(jenkinsUrl + jobName + "/api/json")
except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code) 
    print "      (job name [" + jobName + "] probably wrong)"
    sys.exit(2)

try:
    jobJson = json.load( jenkinsStream )
except:
    print "Failed to parse json"
    sys.exit(3)

if "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" in jobJson["_class"]:
    pipeline = True
else:
    pipeline = False


try:
    if pipeline:
        jenkinsStream   = urlopen(jenkinsUrl + jobName + "/job/master/"+ buildNumber + "/api/json")
    else:
        jenkinsStream   = urlopen(jenkinsUrl + jobName + "/"+ buildNumber + "/api/json")
except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code) 
    print "      (job name [" + jobName + "] probably wrong)"
    sys.exit(2)

try:
    buildStatusJson = json.load( jenkinsStream )
except:
    print "Failed to parse json"
    sys.exit(3)

print "Job \"" + jobName + "\" build #" + buildNumber + ":"
for s in buildStatusJson["actions"]:
    if s.has_key("causes"):
        for cause in s["causes"]:
            print ("Started by " + cause["shortDescription"] if pipeline else cause["shortDescription"])

if buildStatusJson.has_key("result"):      
    print "Job Status: " + buildStatusJson["result"] 
else:
    print "No status found"

if buildStatusJson.has_key("duration"):      
    print "Duration: " + convertToTime(buildStatusJson["duration"])
else: 
    print "No duration found"

if buildStatusJson.has_key("builtOn"):
    print "Slave: " + (buildStatusJson["builtOn"] if buildStatusJson["builtOn"] != "" else "master")


sys.exit(0)