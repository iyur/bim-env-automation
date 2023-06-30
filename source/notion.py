import json
import requests
import time

mt = 3

class Notion:

	def __init__(self, token):

		self.token = token
		self.headers = {
		    'Notion-Version': '2022-06-28',
		    'Content-Type': 'application/json',
		    'Authorization': 'Bearer ' + self.token,
		}

		self.dbId = '71052cdf8b6248c1870e3c4422ab0274'


	@staticmethod
	def process_response(response, json=True):
		has_content = response.content is not None and len(response.content)
		if response.ok:
			if has_content:
				return response.json() if json else response.content
			else:
				return None
		raise Exception(response)


	# def preQuery(self, pid, name=None, path=None, files=None, size=None, mtime=None, root=None, subs=None):

	# 	query = {
	# 		"parent": { "database_id": self.dbId },
	# 		"properties": {}
	# 	}

	# 	if path:
	# 		query['properties']['Path'] = {
	# 			'type': 'rich_text',
 #                'rich_text': [
 #                    {
 #                        'type': 'text',
 #                        'text': {
 #                            'content': path,
 #                        },
 #                    }
 #                ]
	# 		}

	# 	if files:
	# 		query['properties']['Files'] = {
	# 			'type': 'number',
	# 			'number': files
	# 		}

	# 	if size:
	# 		query['properties']['Size'] = {
	# 			'type': 'number',
	# 			'number': size
	# 		}

	# 	if mtime:
	# 		query['properties']['Mtime'] = {
	# 			'type': 'number',
	# 			'number': mtime
	# 		}

	# 	if root and len(root) > 0:
	# 		query['properties']['Root'] = {
	# 			'type': 'relation',
	# 			'relation': root
	# 		}

	# 	if subs and len(subs) > 0:
	# 		query['properties']['Sub'] = {
	# 			'type': 'relation',
	# 			'relation': subs
	# 		}

	# 	return query


	def getDatabase(self, id):
		url = 'https://api.notion.com/v1/databases/' + id + '/query'
		response = requests.post(url, headers=self.headers)

		return response.json()


	def getPage(self, id):

		url = 'https://api.notion.com/v1/pages/' + id
		response = requests.get(url, headers=self.headers)

		return response.json()


	def getBlock(self, pid=None):

		url = "https://api.notion.com/v1/blocks/6b19d65bff9a4d9898251baea086a64c/children?page_size=10000"
		response = requests.get(url, headers=self.headers)

		return response.json()


	def search(self, query):

		url = 'https://api.notion.com/v1/databases/' + self.dbId +'/query'
		response = self.request(url, query)

		result = []

		if response:
			if len(response.get('results')) > 0:
				result.extend(response.get('results'))

			while response and response.get('has_more'):
				query['start_cursor'] = response.get('next_cursor')
				response = self.request(url, query)
				if response and len(response.get('results')) > 0:
					result.extend(response.get('results'))

		return result


	def addPage(self, name, path=None, files=None, fmod=None, size=None, mtime=None, pid=None, childs=None, status=None):

		url = "https://api.notion.com/v1/pages"
		query = {
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
			                "Path": {
			                    "type": "rich_text",
			                    "rich_text": [
			                        {
			                            "type": "text",
			                            "text": {
			                                "content": path,
			                            },
			                        }
			                    ]
			                },
			                "Files": {
			                    "type": "number",
								"number": files
			                },
			                "Size": {
			                    "type": "number",
								"number": size
			                },
			                "Mtime": {
			                    "type": "number",
								"number": mtime
			                },
			                '_fmod': {
			                	'type': 'number',
			                	'number': fmod
			                },
			                "Root": {
			                    "type": "relation",
			                    "relation": [],
			                },
			                "Sub": {
			                    "type": "relation",
			                    "relation": [],
			                },
			                'Status': {
			                	'type': 'status',
			                	'status': {
			                		'name': status
			                	}
			                }
			            }
		}

		if pid: query["properties"]["Root"]["relation"].append({"id": pid})
		if childs: query["properties"]["Sub"]["relation"] = childs

		response = self.request(url, query)

		return response


	def update(self, pid, path=None, files=None, fmod=None, size=None, mtime=None, root=None, childs=None, status=None):

		query = {
			"parent": { "database_id": self.dbId },
			"properties": {}
		}

		if path:
			query['properties']['Path'] = {
				'type': 'rich_text',
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': path,
                        },
                    }
                ]
			}

		if files:
			query['properties']['Files'] = {
				'type': 'number',
				'number': files
			}

		if size:
			query['properties']['Size'] = {
				'type': 'number',
				'number': size
			}

		if mtime:
			query['properties']['Mtime'] = {
				'type': 'number',
				'number': mtime
			}

		if fmod:
			if fmod == 0: fmod = 0.00001
			query['properties']['_fmod'] = {
				'type': 'number',
				'number': fmod
			}

		if root and len(root) > 0:
			query['properties']['Root'] = {
				'type': 'relation',
				'relation': root
			}

		if childs and len(childs) > 0:
			query['properties']['Sub'] = {
				'type': 'relation',
				'relation': childs
			}

		if status:
			query['properties']['Status'] = {
				'type': 'status',
				'status': {
					'name': status,
				}
			}

		url = 'https://api.notion.com/v1/pages/' + pid
		response = self.request2(url, query)

	# def update2(self, pid, root):

	# 	query = {
	# 		"parent": { "database_id": self.dbId },
	# 		"properties": {
	# 		                "Root": {
	# 		                    "type": "relation",
	# 		                    "relation": root,
	# 		                },
	# 		            }
	# 	}

	# 	url = 'https://api.notion.com/v1/pages/' + pid
	# 	response = self.request2(url, query)


	def request(self, url, query, retries=5, timeout=300, backoff=2):

		r = 0
		d = 1

		while r < retries:
			try:
				response = requests.post(url, json=query, headers=self.headers, timeout=timeout)
				response.raise_for_status()

				return response.json()

			except requests.exceptions.RequestException as e:
				print(f"Request failed: {e}")

				r += 1
				if r < retries:
					print(f"Retrying in {d} seconds...")
					time.sleep(d)
					d *= backoff
				else:
					print("Max retries reached. Request failed.")

			return None

	def request2(self, url, query, retries=5, timeout=300, backoff=2):

		r = 0
		d = 1

		while r < retries:
			try:
				response = requests.patch(url, json=query, headers=self.headers, timeout=timeout)
				response.raise_for_status()

				return response.json()

			except requests.exceptions.RequestException as e:
				print(f"Request2 failed: {e}")

				r += 1
				if r < retries:
					print(f"Retrying2 in {d} seconds...")
					time.sleep(d)
					d *= backoff
				else:
					print("Max retries reached. Request2 failed.")

			return None	