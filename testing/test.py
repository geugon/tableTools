import unittest
import os
import copy
import tableTools


########################################


class IOTest(unittest.TestCase):


	def setup(self):
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


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		self.table = tableTools.Table(parser)
		self.validFname='input_valid.txt'
		self.emptyFname='input_empty.txt'
		self.onelineFname='input_oneline.txt'
		self.inconsistantFname='input_inconsistantColumns.txt'
		self.repeatedFname='input_repeatedLabels.txt'
		self.outputFname='output.txt'



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
		self.table = tableTools.Table(parser)
		self.table.load('input_valid.txt')


	def tearDown(self):
		self.table = None


	def test_get(self):
		from_call = self.table.get("mixed_1")
		from_data = self.table._data[-2]
		self.assertEqual(from_call,from_data)


	def test_set_new(self):
		self.table.set("new",4*["value"])
		self.assertEqual(4*["value"],self.table._data[-1])
		self.assertEqual("new",self.table._labels[-1])
		self.assertEqual("new",self.table._publicLabels[-1])


	def test_set_overwrite(self):
		self.table.set("name",4*["value"])
		self.assertEqual(4*["value"],self.table._data[0])
		

	def test_apply_func_copy(self):
		func = lambda x: x
		self.table.apply_func(func,['mixed_2'],'mixed_3')
		self.assertEqual(self.table._data[-1],self.table._data[-2])


	def test_apply_func_inplace(self):
		func = lambda x: 2*x
		expected = [ 2*x for x in self.table._data[1] ]
		self.table.apply_func(func,['ints_1'],'ints_1')
		self.assertEqual(expected,self.table._data[1])

		
	def test_apply_func_multiargs(self):
		def func (a,b): return a+b
		self.table.apply_func(func,['ints_1','ints_2'],'ints_3')
		expected = [ func(*args) for args in zip(self.table._data[1],self.table._data[2]) ]
		self.assertEqual(expected,self.table._data[-1])
		

	def test_column_contains_true(self):
		self.assertEqual(self.table.column_contains('ints_1',1),True)


	def test_column_contains_false(self):
		self.assertEqual(self.table.column_contains('ints_1',5),False)

	
########################################


class LabelTest(unittest.TestCase): 

	
	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		self.table = tableTools.Table(parser)
		self.table.load('input_valid.txt')


	def tearDown(self):
		self.table = None


	def test_get_public_labels(self):
		labels = self.table.get_public_labels()
		self.assertEqual(labels, ['name','ints_1','ints_2','float_1','float_2','str_1','str_2','mixed_1','mixed_2'])


	def test_set_public_labels_valid(self):
		labels = ['name','float_2','str_2']
		self.table.set_public_labels(labels)
		self.assertEqual(labels,self.table._publicLabels)


	def test_set_public_labels_invalid(self):
		with self.assertRaises(LookupError):
			self.table.set_public_labels(['penguin'])


	def test_hide_valid(self):
		self.table.hide('ints_2')
		self.table.hide('mixed_1')
		self.assertEqual(self.table._publicLabels, ['name','ints_1','float_1','float_2','str_1','str_2','mixed_2'])


	def test_hide_alreadyHidden(self):
		self.table.hide('ints_2')
		self.table.hide('mixed_1')
		self.table.hide('ints_2')
		self.table.hide('mixed_1')
		self.assertEqual(self.table._publicLabels, ['name','ints_1','float_1','float_2','str_1','str_2','mixed_2'])

	
	def test_hide_invalid(self):
		self.table.hide('ints_2')
		self.table.hide('mixed_1')
		self.table.hide('penguin')
		self.assertEqual(self.table._publicLabels, ['name','ints_1','float_1','float_2','str_1','str_2','mixed_2'])


	def test_show(self):
		self.table._publicLabels = ['name','ints_1','float_1','float_2','str_1','str_2','mixed_2']
		self.table.show('ints_2')
		self.assertEqual(self.table._publicLabels, ['name','ints_1','float_1','float_2','str_1','str_2','mixed_2','ints_2'])


########################################


class AddDropTest(unittest.TestCase):


	def setUp(self):
		parser = tableTools.PlainTextParser('\t')
		self.table = tableTools.Table(parser)
		self.table.load('input_valid.txt')


	def tearDown(self):
		self.table = None


	def test_match(self): pass
	def test_remove_row(self): pass
	def test_generate_row(self): pass
	def test_merge_rows(self): pass
	def test_merge_columns(self): pass


########################################


if __name__ == "__main__":
	unittest.main()
