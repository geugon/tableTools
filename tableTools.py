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
		self._data = None #store transposed
	
	
	def load(self,filepath):
		"""Needs __doc__

		"""
		(self._labels,rawData) = self._parser.load(filepath)
		self._publicLabels = self._labels

		#Need sanity check
			#Label uniqueness
			#Row lengths consistent with labels

		#As possible convert data to int/floats
		data = []
		for rawRow in rawData:
			row = []
			for el in rawRow:
				try:
					row.append(int(el))
				except ValueError:
					try:
						row.append(float(el))
					except ValueError:
						row.append(el)
			data.append(row)
		self._data = self._transpose(data)
	

	def save(self,filepath):
		"""Needs __doc__

		"""
		data = self._transpose(self._subset(self._publicLabels,True))
		self._parser.save(filepath,self._publicLabels,data)

	
	def _transpose(self,data):
		return list(map(list, zip(*data)))


	def _subset(self,labels,strOutput=False):
		data = []
		for label in labels:
			if strOutput: 
				data.append([str(datum) for datum in self.get(label)])
			else:
				data.append(self.get(label))
		return data

	def _nRows(self):
		return len(self._data[0])
	

	def get(self,label):
		"""Needs __doc__

		"""
		if label not in self._labels: raise LookupError("Invalid column label")
		return self._data[self._labels.index(label)]


	def set(self,label,value):
		"""Needs __doc__

		"""
		if label not in self._labels:
			self._labels.append(label)
			self._data.append(self._nRows() * [value])
		else:
			self._data[self._labels.index(label)] = self._nRows() * [value]


	def get_labels(self): pass
	def get_public_labels(self): pass
	def set_public_labels(self,labels): pass
	def hide(self,label): pass
	def show(self,label): pass
	def apply_func(self,func,inputs,output): pass
	def column_contains(self,label,value): pass
	def match(self,rules): pass
	def remove_row(self,rules): pass
	def generate_row(self,unsure_of_args_for_this): pass
	def merge_rows(self,external): pass
	def merge_columns(self,external): pass
	#Need method(s) to allow interacting with subgroups, or change in base implentation to list of grouped tables


########################################


if __name__ == "__main__":
	#Test
	parser = PlainTextParser('\t')
	table = Table(parser)
	table.load('input.txt')
	table.set('new_label',2)
	table.save('output.txt')

