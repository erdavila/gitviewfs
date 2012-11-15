import unittest
import os

from tests.test_integration import TestIntegration
from gitviewfs_objects import ROOT_DIR


class TestRootDir(unittest.TestCase):

	def test_list(self):
		items = ROOT_DIR.list()
		self.assertItemsEqual(['refs', 'objects'], items)


class TestRootDirIntegration(TestIntegration):
	
	def test_list(self):
		items = os.listdir(self.mountpoint)
		self.assertItemsEqual(['refs', 'objects'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
