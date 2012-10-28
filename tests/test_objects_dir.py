import unittest

from gitviewfs_objects import ObjectsDir


class TestObjectsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list(self):
		objects_dir = ObjectsDir(parent=None)
		items = objects_dir.list()
		self.assertItemsEqual(['commits', 'trees', 'blobs', 'all'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
