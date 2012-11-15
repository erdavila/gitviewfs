import unittest
import os

from tests.test_integration import TestIntegration


class TestRefsDirIntegration(TestIntegration):
	
	def test_list(self):
		refs_dir_path = self.make_refs_dir_path()
		items = os.listdir(refs_dir_path)
		self.assertItemsEqual(['HEAD', 'branches'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
