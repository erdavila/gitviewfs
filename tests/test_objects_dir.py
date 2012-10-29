import unittest
import os

from gitviewfs_objects import ObjectsDir
from tests.test_integration import TestIntegration


class TestObjectsDir(unittest.TestCase):

	def test_list(self):
		objects_dir = ObjectsDir.INSTANCE
		items = objects_dir.list()
		self.assertItemsEqual(['commits', 'trees', 'blobs', 'all'], items)


class TestObjectsDirIntegration(TestIntegration):

	def test_list(self):
		refs_dir = os.path.join(self.mountpoint, ObjectsDir.NAME)
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['all', 'blobs', 'commits', 'trees'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
