import argparse
import source
import json

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


# no.addPage('ac2e2d746b5945b8bb2ab884b7600f5a')

# cde = source.CDE()


# data = cde.test('W:/')
# for i in data:
# 	# print(i + " " + data[i]['modified'])
# 	no.addPage('ac2e2d746b5945b8bb2ab884b7600f5a', i, data[i]['modified'])

# cde.test('W:/')