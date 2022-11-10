#!/usr/bin/env python3
import os, json5, requests, urllib.parse
from bs4 import BeautifulSoup

CONTACTS_URL = os.environ.get('LUCOS_CONTACTS', "https://contacts.l42.eu/")
LUCOS_HEADERS={'AUTHORIZATION':"key "+os.environ.get('LUCOS_CONTACTS_API_KEY')}

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
			profile_pic_url = row[2]
			person_id = row[3]
			cluster_media_key = row[8] # Same as row[11] from what I can tell
			escaped_key = cluster_media_key.replace("_", "~u")
			search_path = f"/search/_c{escaped_key}_{name}"

			data = {"identifiers": [
				{
					"type":"googlephotos",
					"person_id": person_id,
					"cluster_media_key": cluster_media_key,
					"search_path": search_path,
					"profile_pic_url": profile_pic_url,
				},
				{
					"type":"name",
					"name": name,
				}
			]};
			resp = requests.post(CONTACTS_URL+'agents/import', headers=LUCOS_HEADERS, allow_redirects=False, json=data)
			resp.raise_for_status()