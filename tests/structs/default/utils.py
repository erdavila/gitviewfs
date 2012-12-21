import dir_structure.default
from tests.structs.default.paths import PathMaker
from tests.structs.utils import BaseIntegrationTest, BaseDirStructTest


class BaseDefaultDirStructIntegrationTest(BaseIntegrationTest, PathMaker):
	pass


class BaseDefaultDirStructTest(BaseDirStructTest):
	
	def _get_dir_structure(self):
		return dir_structure.default.Default()
