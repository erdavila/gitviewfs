import unittest

from gitviewfs_objects import ObjectsDir
from tests.test_integration import TestIntegration
import os


class TestObjectsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list(self):
		objects_dir = ObjectsDir(parent=None)
		items = objects_dir.list()
		self.assertItemsEqual(['commits', 'trees', 'blobs', 'all'], items)


class TestObjectsDirIntegration(TestIntegration):

	def test_list_objects_dir(self):
		refs_dir = os.path.join(self.mountpoint, ObjectsDir.NAME)
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['all', 'blobs', 'commits', 'trees'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
