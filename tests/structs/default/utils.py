import dir_structure.default
from tests.structs.default.paths import PathMaker
from tests.structs.utils import BaseIntegrationTest, BaseDirStructTest


class BaseDefaultDirStructIntegrationTest(BaseIntegrationTest, PathMaker):
	
	def get_dir_struct_name(self):
		return 'default'


class BaseDefaultDirStructTest(BaseDirStructTest):
	
	def _get_dir_structure(self):
		return dir_structure.default.Default()
