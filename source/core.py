from .cde import CDE
from .notion import Notion
import os

class Core:

	def __init__(self, token):

		self.cms = Notion(token)
		self.cde = CDE()

		self.cde.cms = self.cms

	def fetch(self, path='W:/', filter=r'^[_#!1-9]'):

		self.cde.fetchProjectData(path, filter)
