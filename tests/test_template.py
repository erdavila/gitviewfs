import unittest
from gitviewfs_objects import template


class TemplateTest(unittest.TestCase):
	
	def test_create_instance(self):
		class Class(object): pass
		tmpl = template(Class)
		
		instance = tmpl.create_instance()
		
		self.assertIsInstance(instance, Class)
	
	def test_forward_constructor_arguments(self):
		class Class(object):
			def __init__(self, name, age):
				self.name = name
				self.age = age
		NAME = 'name'
		AGE = 56
		tmpl = template(Class, name=NAME, age=AGE)
		
		instance = tmpl.create_instance()
		
		self.assertIs(instance.name, NAME)
		self.assertIs(instance.age, AGE)
	
	def test_recurse_on_list_arguments(self):
		class BaseClass(object):
			def __init__(self, **kwargs):
				for name, value in kwargs.iteritems():
					setattr(self, name, value)
		class Class1(BaseClass): pass
		class Class2(BaseClass): pass
		NAME = 'name'
		AGE = 99
		OTHER = object()
		tmpl = template(Class1, name=NAME, list_arg=[
			AGE,
			template(Class2, other=OTHER)
		])
		
		instance = tmpl.create_instance()
		
		self.assertIs(instance.name, NAME)
		self.assertIsInstance(instance.list_arg, list)
		self.assertIs(instance.list_arg[0], AGE)
		self.assertIsInstance(instance.list_arg[1], Class2)
		self.assertIs(instance.list_arg[1].other, OTHER)
	
	def test_create_with_additional_arguments(self):
		class Class(object):
			def __init__(self, **kwargs):
				self.kwargs = kwargs
		NAME = 'name'
		AGE = 56
		STATUS = True
		tmpl = template(Class, name=NAME, age=12)
		
		instance = tmpl.create_instance(age=AGE, status=STATUS)
		
		expected_kwargs = {
			'name'   : NAME,
			'age'    : AGE,
			'status' : STATUS,
		}
		self.assertDictEqual(instance.kwargs, expected_kwargs)
