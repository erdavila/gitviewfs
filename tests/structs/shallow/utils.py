import dir_structure.shallow
from tests.structs.shallow.paths import PathMaker
from tests.structs.utils import BaseIntegrationTest, BaseDirStructTest


class BaseDefaultDirStructIntegrationTest(BaseIntegrationTest, PathMaker):
	
	def get_dir_struct_name(self):
		return 'shallow'


class BaseDefaultDirStructTest(BaseDirStructTest):
	
	def _get_dir_structure(self):
		return dir_structure.shallow.Shallow()
