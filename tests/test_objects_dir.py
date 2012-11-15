import unittest
import os

from tests.test_integration import TestIntegration


class TestObjectsDirIntegration(TestIntegration):

	def test_list(self):
		refs_dir = self.make_objects_dir_path()
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['blobs', 'commits', 'trees'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
