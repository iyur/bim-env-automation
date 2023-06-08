from datetime import datetime
import json
import math
import re
import os
import time

to = 10

class CDE:

	def __init__(self):

		self.cms = None

		self.filter = {}
		self.filter['merged'] = r"(\d{2}-|##-|ZZ-|XX-)"


	def fetchProjectData(self, path, filter):

		for prj in os.listdir(path):
			if not re.match(filter, prj) and os.path.isdir(os.path.join(path, prj)):

				query = {
					"filter": {
						"property": "Name",
						"rich_text": {
							"equals": prj
						},
					}
				}

				result = self.cms.search(query)

				if result:
					pid = result[0]['id']
					print(str(time.time()) + ' ' + prj + ': exists')
				else:
					result = self.cms.addPage(prj, 'Project')
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					pid = result['id']
					print(str(time.time()) + ' ' + prj + ': added')

				self.fetchZoneData(os.path.join(path, prj), pid)



	# path:	string,filesystem path to the item
	# pid:	string, parent project id in cms
	def fetchZoneData(self, path, pid):

		statuses = {
		   #'INC': '00-Inc',
		   #'RES': '00-Res',
			'WIP': '01-WiP',
			'SHA': '02-Sha',
			'PUB': '03-Pub'
		}

		for s in statuses:
			if os.path.isdir(os.path.join(path, statuses[s])):

				query = {
					"filter": {
						"and": [
							{
								"property": "Name",
								"rich_text": {
									"equals": s
								},
							},
							{
								"property": "Parent",
								"relation": {
									"contains": pid
								}
							}
						]
					}
				}

				result = self.cms.search(query)

				if result:
					sid = result[0]['id']
					print(str(time.time()) + ' ' + path + '/' + statuses[s] + ' exists')
				else:
					result = self.cms.addPage(s, 'Status', pid)
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					sid = result['id']
					print(str(time.time()) + ' ' + path + '/' + statuses[s] + ' added')

				self.fetchStageData(os.path.join(path, statuses[s]), sid)


	# sid:	string, parent status zone id in cms
	def fetchStageData(self, path, sid):

		for s in os.listdir(path):
			if os.path.isdir(os.path.join(path, s)):

				stage = s
				if re.search(self.filter['merged'], s):
					res = s.split('-')
					stage = res[1]

				query = {
					"filter": {
						"and": [
							{
								"property": "Name",
								"rich_text": {
									"equals": stage
								},
							},
							{
								"property": "Parent",
								"relation": {
									"contains": sid
								}
							}
						]
					}
				}

				result = self.cms.search(query)

				if result:
					eid = result[0]['id']
					print(str(time.time()) + ' ' + path + '/' + s + ' exists')
				else:
					result = self.cms.addPage(stage, 'Stage', sid)
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					eid = result['id']
					print(str(time.time()) + ' ' + path + '/' + s + ' added')

				self.fetchGroupData(os.path.join(path, s), eid)


	# eid:	string, parent stage (epic) id in cms
	def fetchGroupData(self, path, eid):

		for g in os.listdir(path):
			if os.path.isdir(os.path.join(path, g)):

				query = {
					"filter": {
						"and": [
							{
								"property": "Name",
								"rich_text": {
									"equals": g
								},
							},
							{
								"property": "Parent",
								"relation": {
									"contains": eid
								}
							}
						]
					}
				}

				result = self.cms.search(query)

				if result:
					gid = result[0]['id']
					print(str(time.time()) + ' ' + path + '/' + g + ' exists')
				else:
					result = self.cms.addPage(g, 'Group', eid)
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					gid = result['id']
					print(str(time.time()) + ' ' + path + '/' + g + ' added')

				self.fetchRoleData(os.path.join(path, g), gid)


	# gid:	string, parent group id in cms
	def fetchRoleData(self, path, gid):

		for r in os.listdir(path):
			if os.path.isdir(os.path.join(path, r)):

				query = {
					"filter": {
						"and": [
							{
								"property": "Name",
								"rich_text": {
									"equals": r
								},
							},
							{
								"property": "Parent",
								"relation": {
									"contains": gid
								}
							}
						]
					}
				}

				result = self.cms.search(query)

				if result:
					rid = result[0]['id']
					print(str(time.time()) + ' ' + path + '/' + r + ' exists')
				else:
					result = self.cms.addPage(r, 'Role', gid)
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					rid = result['id']
					print(str(time.time()) + ' ' + path + '/' + r + ' added')

				self.fetchFolderData(os.path.join(path, r), rid)


	# rid:	string, parent role id in cms
	def fetchFolderData(self, path, rid):

		for f in os.listdir(path):
			if os.path.isdir(os.path.join(path, f)):

				query = {
					"filter": {
						"and": [
							{
								"property": "Name",
								"rich_text": {
									"equals": f
								},
							},
							{
								"property": "Parent",
								"relation": {
									"contains": rid
								}
							}
						]
					}
				}

				result = self.cms.search(query)

				if result:
					fid = result[0]['id']
					print(str(time.time()) + ' ' + path + '/' + f + ' exists')
				else:
					result = self.cms.addPage(f, 'Folder', rid)
					if isinstance(result, dict):
						t = time.time()
						while 'id' not in result:
							if time.time() - t > to:
								break
							time.sleep(1)
					fid = result['id']
					print(str(time.time()) + ' ' + path + '/' + f + ' added')