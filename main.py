import argparse
import json
import source
import time

start_time = time.time()

cmd = argparse.ArgumentParser()
cmd.add_argument('-t', '--token', required=True, help='Notion Token')
arg = cmd.parse_args()

core = source.Core(arg.token)
# print(core.test())

# no = source.Notion(arg.token)
# print(no.addPage('SHA', '6b1be2304d17479aa1e601b5f1122df0'))
# print(json.dumps(no.search('AKD'), indent = 4))

# print(json.dumps(no.getPage('6b19d65bff9a4d9898251baea086a64c'), indent = 4))

# print(json.dumps(core.cms.getDatabase('ac2e2d746b5945b8bb2ab884b7600f5a'), indent = 4))

core.fetch()

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