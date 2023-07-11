from datetime import datetime, timedelta
from colorama import init as color #
from colorama import Fore, Style #
import json
import math
import re
import os
import time

color()

class CDE:

	def __init__(self):

		self.cms = None

		self.filters = {}
		self.filters['projects'] = r'^[_#!1-9]'
		self.filters['temp'] = r'^(?:FBR|GoL|GOS)$'

		self.filters['keep'] = ['99-Tmp']
		self.filters['skip'] = ['backup', 'central', 'log', 'temp', 'tmp']

		self.options = {}

		# max allowed level of aggregation (including)
		self.options['depth_max'] = 5
		# level of aggregation depth by zone
		# necessity differes for each status zone
		self.options['depth'] = {
			'00-Inc': 4,
			'00-Res': 4,
			'01-WiP': 5,
			'02-Sha': 5,
			'03-Pub': 4,
			'04-Arc': 2,
			'99-Tmp': 1,
			'99-Del': 1,
		}

	# C:\\Users\\i.yurasov\\Desktop\\dev\\bimcloud-api-old
	def fetchProjects(self, path='W:\\', extract=True):

		for p in os.listdir(path):
			if re.match(self.filters['temp'], p):
				if os.path.isdir(os.path.join(path, p)) and extract:
					self.fetchFolder(os.path.join(path, p))


	def fetchFolder(self, path):

		depth = 0
		depth_zone = 0

		print('Get path ' + Fore.YELLOW + '\"' + path + '\"' + Style.RESET_ALL)
		print('Retrieving stored entries by the given path...', end=' ', flush=True)

		q1 = {
			"filter": {
				"and": [
					{
						"property": "Path",
						"rich_text": {
							"contains": path
						},
					}
				]
			}
		}

		# performance
		# it's better to retrieve a full list of db entries to work within the lists later
		entries = self.cms.search(q1)
		en = len(entries) if entries and len(entries) > 0 else 0
		print(Fore.YELLOW + str(en) + Style.RESET_ALL + ' items found')
		time.sleep(1)

		stats = {
			path: {
				'size': 0,		# filesize in bytes
				'files': 0,		# files found
				'fmod': 0,		# files recently modified
				'mt': 0,		# modification time
				'nid': ''		# notion id
			}
		}

		# let's parse the given path
		for root, dirs, files in os.walk(path, topdown=False):
			for f in files:
				fp = os.path.join(root, f)
				if root not in stats: stats[root] = {'size': 0, 'files': 0, 'fmod': 0, 'mt': 0}

				if os.path.exists(fp):
					stats[root]['files'] += 1
					stats[root]['size'] += os.path.getsize(fp)
					if stats[root]['mt'] < os.path.getmtime(fp):
						stats[root]['mt'] = os.path.getmtime(fp)
					if time.time() - os.path.getmtime(fp) <= 60*60*24*30:
						stats[root]['fmod'] += 1
					# print('[' + root + '] file: ' + f)

			for d in dirs:
				dp = os.path.join(root, d)
				if root not in stats: stats[root] = { 'size': 0, 'files': 0, 'fmod': 0, 'mt': 0}
				if os.path.join(root, d) not in stats: stats[dp]['size'] = 0

				stats[root]['size'] += stats[dp]['size']
				stats[root]['files'] += stats[dp]['files']
				stats[root]['fmod'] += stats[dp]['fmod']
				if stats[root]['mt'] < stats[dp]['mt']:
					stats[root]['mt'] = stats[dp]['mt']
				# print('dir: ' + d + ' (' + str(stats['size'][os.path.join(root, d)]) + ')')

			
			parts = root.split('\\')
			depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
			if len(parts) >= 3: depth_zone = self.options['depth'].get(parts[2], 5)

			if root not in stats: stats[root] = {'size': 0, 'files': 0, 'fmod': 0, 'mt': 0}
			if os.path.isdir(root) and stats[root]['size'] > 0 and depth < self.options['depth_max']:

				print('Processing: ' + os.path.dirname(root) + ', \"' + os.path.basename(root) + '\"...', end=' ', flush=True)

				# check against depth and filters, skip if matches
				if (depth >= depth_zone or 
					(not any(k in os.path.basename(root) for k in self.filters['keep']) and any(f in os.path.basename(root).lower() for f in self.filters['skip']))
					):
					print(Fore.YELLOW + 'skip' + Style.RESET_ALL)

				else:
					# deal with related (subpages) items
					childs = {'base':[], 'over':[]}
					n = 0

					for i in os.listdir(root):
						if i and os.path.isdir(os.path.join(root, i)) and depth < self.options['depth_max'] - 1:
							if os.path.join(root, i) in stats and stats[os.path.join(root, i)]['size'] > 0 and 'nid' in stats[os.path.join(root, i)]:
								n += 1
								if n < 100: # notion limitation
									childs['base'].append({"id": stats[os.path.join(root, i)]['nid']})
								else:
									childs['over'].append({"id": stats[os.path.join(root, i)]['nid']})

					# check the activity
					status = 'N/a'
					if time.time() - stats[root]['mt'] > 60*60*24*365:  # 1y
						status = 'Dead'
					elif time.time() - stats[root]['mt'] > 60*60*24*90: # 3m
						status = 'Idle'
					elif time.time() - stats[root]['mt'] > 60*60*24*30: # 1m
						status = 'Recent'
					else:
						status = 'Active'

					# search in retrieved entries
					search = [e for e in entries if e['properties']['Name']['title'][0]['plain_text'] == os.path.basename(root) and e['properties']['Path']['rich_text'][0]['plain_text'] == root]

					if search and len(search) > 0:
						if not 'nid' in stats[root]: stats[root]['nid'] = search[0]['id']
						# reasons to update
						if (search[0]['properties']['Files']['number'] != stats[root]['files'] or
							search[0]['properties']['_fmod']['number'] != stats[root]['fmod'] or
							search[0]['properties']['_fsize']['number'] != stats[root]['size'] or
							search[0]['properties']['_mtime']['number'] != stats[root]['mt'] or
							search[0]['properties']['Status']['status']['name'] != status or
							set(map(lambda x: frozenset(x.items()), search[0]['properties']['Sub']['relation'])) != set(map(lambda x: frozenset(x.items()), childs['base']+childs['over']))): # subs

							# batch update the first 100, then each sub
							update = self.cms.update(search[0]['id'], path = root, files = stats[root]['files'], fmod = stats[root]['fmod'], size = stats[root]['size'], mtime = stats[root]['mt'], childs = childs['base'], status = status)
							if len(childs['over']) > 0:
								for child in childs['over']:
									u = self.cms.update(child['id'], root = [{'id': search[0]['id']}])
							print(Fore.GREEN + 'upd ' + Style.RESET_ALL)
						
						else:
							print(Fore.CYAN + 'n/m' + Style.RESET_ALL)
					
					else:
						response = self.cms.addPage(os.path.basename(root), path=root, files = stats[root]['files'], fmod = stats[root]['fmod'], size = stats[root]['size'], mtime = stats[root]['mt'], childs = childs['base'], status = status)
						if response:
							stats[root]['nid'] = response['id']
							# batch update the first 100, then each sub
							if len(childs['over']) > 0:
								for child in childs['over']:
									u = self.cms.update(child['id'], root = [{'id': response['id']}])
							print(Fore.GREEN + 'add' + Style.RESET_ALL)

#todo: add condition to skip childs that match filters
#todo: rewrite child update, to skip the procedure
#todo: log errors