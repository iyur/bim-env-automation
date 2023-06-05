import requests
import json

class Notion:

	def __init__(self, token):

		self.token = token
		self.headers = {
		    'Notion-Version': '2022-06-28',
		    'Content-Type': 'application/json',
		    'Authorization': 'Bearer ' + self.token,
		}

		self.dbId = 'ac2e2d746b5945b8bb2ab884b7600f5a'

	def getDatabase(self, id):
		url = 'https://api.notion.com/v1/databases/' + id + '/query'
		response = requests.post(url, headers=self.headers)

		return response.json()

	def getPage(self, id):

		url = 'https://api.notion.com/v1/pages/' + id
		response = requests.get(url, headers=self.headers)

		return response.json()

	def addPage(self, name, type='Item', pid=False, date=None):

		url = "https://api.notion.com/v1/pages"
		schema = {
			"parent": { "database_id": self.dbId },
			"properties": {
			                "Name": {
			                    "id": "title",
			                    "type": "title",
			                    "title": [
			                        {
			                            "type": "text",
			                            "text": {
			                                "content": name,
			                            },
			                        }
			                    ]
			                },
			                "Type": {
			                    "type": "rich_text",
			                    "rich_text": [
			                        {
			                            "type": "text",
			                            "text": {
			                                "content": type,
			                            },
			                        }
			                    ]
			                },
			     #            "Date": {
			     #                "type": "date",
								# "date": {
								# 	"start": date,
			     #                    "end": None,
			     #                    "time_zone": 'Europe/Kiev'
								# }
			     #            },
			                "Parent": {
			                    "type": "relation",
			                    "relation": [],
			                },
			            }
		}

		if pid:
			schema["properties"]["Parent"]["relation"].append({"id": pid})

		response = requests.post(url, json=schema, headers=self.headers)

		return response.json()

	def search(self, query):

		url = 'https://api.notion.com/v1/databases/' + self.dbId +'/query'
		response = requests.post(url, json=query, headers=self.headers)

		return response.json()['results']