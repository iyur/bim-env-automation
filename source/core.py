from .cde import CDE
from .notion import Notion
import os
import datetime
class Core:

	def __init__(self, token):

		self.cms = Notion(token)
		self.cde = CDE()

		self.cde.cms = self.cms

	def fetch(self, path='W:/', filter=r'^[_#!1-9]'):

		start_date = datetime.datetime(2023, 6, 6)
		end_date = datetime.datetime(2023, 6, 30)


		self.cde.fetchProjects()
		# self.cde.fetchFolder('W:\\Zrc\\01-Inc\\')

		# print(self.cde.test_walk('W:\\NVR'))
		# print(self.cde.test_listdir('W:\\NVR'))
		# print(self.cde.test_glob('W:\\NVR'))
		# print(self.cde.test_pathlib('W:\\NVR'))