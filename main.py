import argparse
import json
import source
import time

from datetime import datetime, timedelta

# import win32com.client as com

# secret_Y4wcJwXcdXLW4u7DVKjx7TCRBVOL5wjpyd4W3L0IaRz

start_time = time.time()

cmd = argparse.ArgumentParser()
cmd.add_argument('-t', '--token', required=True, help='Notion Token')
arg = cmd.parse_args()

core = source.Core(arg.token)
# print(core.test())

# no = source.Notion(arg.token)
# print(core.cms.addPage('testing', round(time.time())))
# print(json.dumps(core.cms.addPage('root3', path='W:\\NVR', mtime=datetime.now().timestamp(), cid='e8cf0c572a4f493680bb5d6f968f82c3'), indent = 4))

# "archived": true,

# query1 = {
# 	"filter": {
# 		"and": [
# 			{
# 				"property": "Name",
# 				"rich_text": {
# 					"equals": 'IvS-E111'
# 				},
# 			},
# 			{
# 				"property": "Path",
# 				"rich_text": {
# 					"equals": 'W:\\Zab\\00-Inc\\##-Z00\\Z\\Z\\IvS-E'
# 				},
# 			}
# 		]
# 	}
# }

query = {
	"filter": {
		"and": [
			{
				"property": "Path",
				"rich_text": {
					"contains": 'W:\\AVR\\'
				},
			}
		]
	}
}
# search = core.cms.search(query)

# print(json.dumps(search, indent = 4))
# print(str(len(search)))

# print(json.dumps(core.cms.getPage('566a439fb7c2438b9908d67983dfa08d'), indent = 4))
# print(json.dumps(core.cms.getDatabase('6b8f01dd359a491696f9110be1c366a6'), indent = 4))
# print(json.dumps(core.cms.getBlock(), indent = 4))

# print(json.dumps(core.cms.getDatabase('ac2e2d746b5945b8bb2ab884b7600f5a'), indent = 4))




# folderPath = r"W:/NVR/01-WiP/03-C00/A"
# fso = com.Dispatch("Scripting.FileSystemObject")
# folder = fso.GetFolder(folderPath)
# MB = 1024 * 1024.0
# print("%.2f MB" % (folder.Size / MB))

core.fetch()

# core.cde.fetchFolder2('W:\\AVR\\')

# core.cde.search_recent_files()

# query = {
# 	"filter": {
# 		"property": "Name",
# 		"rich_text": {
# 			"equals": 'testi2323ng'
# 		},
# 	}
# }


# # print(json.dumps(core.cms.addPage('testing'), indent = 4))
# test = core.cms.search(query)

# if test:
# 	print(json.dumps(test, indent = 4))
# else:
# 	print('none')
# for i in range (1,26):
# 	print(json.dumps(core.cms.search(query), indent = 4))

print("\n%s sec" % (time.time() - start_time))

# no.addPage('ac2e2d746b5945b8bb2ab884b7600f5a')

# cde = source.CDE()


# data = cde.test('W:/')
# for i in data:
# 	# print(i + " " + data[i]['modified'])
# 	no.addPage('ac2e2d746b5945b8bb2ab884b7600f5a', i, data[i]['modified'])

# cde.test('W:/')


# C:\Python38>python C:\Users\i.yurasov\Desktop\dev\bim-env-automation\main.py -t="secret_Y4wcJwXcdXLW4u7DVKjx7TCRBVOL5wjpyd4W3L0IaRz"