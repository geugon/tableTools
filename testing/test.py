import unittest
import os
import tableTools


########################################


class IOTest(unittest.TestCase):


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		self.table = tableTools.Table(parser)
		self.validFname='input_valid.txt'
		self.emptyFname='input_empty.txt'
		self.onelineFname='input_oneline.txt'
		self.inconsistantFname='input_inconsistantColumns.txt'
		self.repeatedFname='input_repeatedLabels.txt'
		self.outputFname='output.txt'


	def tearDown(self):
		self.table = None
		try:
			os.remove(self.outputFname)
		except OSError:
			pass


	def test_load_valid(self):
		self.table.load(self.validFname)
		self.assertTrue(self.table._labels != [])
		self.assertTrue(self.table._data != [])

	
	def test_casting(self):
		self.table.load(self.validFname)
		data = self.table._data
		self.assertTrue(isinstance(data[1][0], int))
		self.assertTrue(isinstance(data[3][0], float))
		self.assertTrue(isinstance(data[5][0], str))
	

	def test_save_valid(self):
		self.table.load(self.validFname)
		self.table.save(self.outputFname)
		import filecmp
		self.assertTrue(filecmp.cmp(self.validFname,self.outputFname))


	def test_load_empty(self):
		with self.assertRaises(ValueError):
			self.table.load(self.emptyFname)


	def test_load_oneline(self):
		self.table.load(self.onelineFname)
		self.assertTrue(self.table._labels != [])
		self.assertTrue(self.table._data == [])


	def test_load_inconsistantColumns(self):
		with self.assertRaises(ValueError):
			self.table.load(self.inconsistantFname)


	def test_load_repeatedLabels(self):
		with self.assertRaises(ValueError):
			self.table.load(self.repeatedFname)


########################################


class EditTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get(self): pass
	def test_set(self): pass
	def test_apply_func(self): pass
	def test_column_contains(self): pass

	
########################################


class LabelTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get_public_labels(self): pass
	def test_set_public_labels(self): pass
	def test_hide(self): pass
	def test_show(self): pass


########################################


class AddDropTest(unittest.TestCase):


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get_public_labels(self): pass
	def test_match(self): pass
	def test_remove_row(self): pass
	def test_generate_row(self): pass
	def test_merge_rows(self): pass
	def test_merge_columns(self): pass


########################################


class EditTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get(self): pass
	def test_set(self): pass
	def test_apply_func(self): pass
	def test_column_contains(self): pass

	
########################################


class LabelTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get_public_labels(self): pass
	def test_set_public_labels(self): pass
	def test_hide(self): pass
	def test_show(self): pass


########################################


class AddDropTest(unittest.TestCase):


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get_public_labels(self): pass
	def test_match(self): pass
	def test_remove_row(self): pass
	def test_generate_row(self): pass
	def test_merge_rows(self): pass
	def test_merge_columns(self): pass


########################################


if __name__ == "__main__":
	unittest.main()
