import unittest

from fs_objects import create_fs_object, RootDir, RefsDir


class Test(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_fs_object_RootDir(self):
		obj = create_fs_object("/")
		self.assertIsInstance(obj, RootDir)
	
	def test_get_fs_object_RefsDir(self):
		obj = create_fs_object("/refs")
		self.assertIsInstance(obj, RefsDir)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_get_fs_object_RootDir']
	unittest.main()
