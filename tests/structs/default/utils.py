import dir_structure.default
from tests.structs.default.paths import PathMaker
from tests.structs.test_integration_base import TestIntegrationBase, DirStructPathTest


class TestIntegration(TestIntegrationBase, PathMaker):
	pass


class DefaultDirStructPathTest(DirStructPathTest):
	
	def _get_dir_structure(self):
		return dir_structure.default.Default()
