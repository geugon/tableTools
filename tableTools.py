class PlainTextParser():
	"""simple parser for handling I/O of text data tables

	"""

	def __init__(self,delimiter):
		self.delimiter = delimiter


	def load(self,filepath):
		import string
		with open(filepath) as lines:
			(labels,*data) = [line.rstrip().split(self.delimiter) for line in lines]
		return (labels,data)


	def save(self,filepath,header,data):
		f=open(filepath,'w') #DANGER
		print(self.delimiter.join(header),file=f)
		for el in data:
			print(self.delimiter.join(el),file=f)


########################################


class Table():
	"""stores table data and provides access methods

	"""

	def __init__(self,parser):
		self._parser = parser
		self._labels = None
		self._publicLabels = None
		self._data = None
	
	
	def load(self,filepath):
		(self._labels,self._data) = self._parser.load(filepath)
		self._publicLabels = self._labels
	
	
	def save(self,filepath):
		self._parser.save(filepath,self._publicLabels,self._data)


	def get_labels(self): pass
	def set_labels(self,labels): pass
	def get(self,label): pass
	def set(self,label,value): pass
	def apply_func(self,func,inputs,output): pass
	def subset(self,rules): pass
	def remove(self,rules): pass
	def generate(self,unsure_of_args_for_this): pass
	def merge_rows(self,external): pass
	def merge_columns(self,external): pass
	#Need method(s) to allow interacting with subgroups, or change in base implentation to list of grouped tables


########################################


if __name__ == "__main__":
	#Test
	parser = PlainTextParser('e')
	table = Table(parser)
	table.load('input.txt')
	print(table._labels)
	print(table._data)
	table.save('output.txt')
