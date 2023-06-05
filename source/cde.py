from datetime import datetime
import json
import math
import re
import os

class CDE:

	def __init__(self):

		self.cms = None

	def test(self, path):

		items = {}

		for item in os.listdir(path):
			item_path = os.path.join(path, item)

			if not re.match(r'^[_#!1-9]', item):
				if os.path.isdir(item_path):
					#print(item)
					md = datetime.fromtimestamp(math.floor(os.path.getmtime(item_path)))
					items[item] = {
						'path': item_path,
						'modified': md.strftime(f"%Y-%m-%dT%H:%M:%SZ")
					}
					#items.append(item = {'path': item_path})

		return items

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
					print(prj + ': exists')
				else:
					result = self.cms.addPage(prj, 'Project')
					pid = result['id']
					print(prj + ': added')

				self.fetchZoneData(os.path.join(path, prj), pid)


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
					print(path + '/' + statuses[s] + ' exists')
				else:
					result = self.cms.addPage(s, 'Status', pid)
					sid = result['id']
					print(path + '/' + statuses[s] + ' added')

				self.fetchStageData(os.path.join(path, statuses[s]))

	def fetchStageData(self, path, sid=None):

		for stage in os.listdir(path):
			if os.path.isdir(os.path.join(path, stage)):
				print(stage)


