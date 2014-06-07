import unittest
import tableTools


########################################


class IOTest(unittest.TestCase):


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)


	def test_load_valid(self,fname='input_valid.txt'): pass
	def test_save_valid(self,fname='input_valid.txt'): pass
	def test_load_empty(self,fname='input_empty.txt'): pass
	def test_load_inconsistantColumns(self,fname='input_inconsistantColumns.txt'): pass
	def test_load_repeatedLabels(self,fname='input_repeatedLabels.txt'): pass


########################################


class SimpleTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		table = tableTools.Table(parser)
		table.load('input_valid.txt')


	def test_get(self): pass
	def test_set(self): pass

	
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


if __name__ == "__main__":
	unittest.main()
