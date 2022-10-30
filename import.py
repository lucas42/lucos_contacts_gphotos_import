#!/usr/bin/env python3
import os, json5, requests, urllib.parse
from bs4 import BeautifulSoup

CONTACTS_URL = os.environ.get('LUCOS_CONTACTS', "https://contacts.l42.eu/")
LUCOS_HEADERS={'AUTHORIZATION':"key "+os.environ.get('LUCOS_CONTACTS_API_KEY')}


# Search for an existing match in lucos, based on the order of items in the accounts arround
#
# Returns the agentid as a string, if a match is found.  Otherwise returns None
def matchContact(accounts, primaryName):
	for account in accounts:
		resp = requests.get(CONTACTS_URL+"identify", headers=LUCOS_HEADERS, params=account, allow_redirects=False)
		if resp.status_code == 302:
			return resp.headers['Location'].replace("/agents/","")
		if resp.status_code == 409:
			print("Conflict for "+primaryName+" - "+account['type'])
		if resp.status_code >= 500:
			resp.raise_for_status()
	return None

def newContact(name):
	resp = requests.post(CONTACTS_URL+"agents/add", headers=LUCOS_HEADERS, allow_redirects=False, data={'name': name})
	if resp.status_code == 302:
		return resp.headers['Location'].replace("/agents/","")
	raise Exception("Unexpected status code "+str(resp.status_code)+" "+resp.reason+": "+resp.text)


with open('data.html') as fp:
	doc = BeautifulSoup(fp, "html.parser")
	for script in doc.find_all("script"):
		if "AF_initDataCallback(" not in script.get_text():
			continue
		raw = script.get_text().replace("AF_initDataCallback(","",1).replace(");","",1)
		data = json5.loads(raw)
		if data['key'] != "ds:3":
			continue
		for row in data['data'][0][0][0][0]:
			name = row[1]
			if not name:
				continue
			image = row[2]
			numericId = row[3]
			id1 = row[8]
			id2 = row[11] # All examples I've looked at have the same value for id1 and id2
			url = f"/_search/c{id1}_{name}"
			print(name, url)