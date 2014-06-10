import copy


def str_to_num(item):
	try:
		return int(item)
	except ValueError:
		try:
			return float(item)
		except ValueError:
			return item


def transpose(data):
	return map(list, zip(*data))


########################################


class PlainTextParser():
	"""simple parser for handling I/O of text data tables

	"""

	def __init__(self,delimiter):
		self.delimiter = delimiter


	def load(self,filepath):
		import string
		with open(filepath) as lines:
			try:
				(labels,*data) = [line.rstrip().split(self.delimiter) for line in lines]
			except ValueError:
				raise ValueError('Incomplete data for creating table')
			data = [list(map(str_to_num,row)) for row in data]
		return (labels,data)


	def save(self,filepath,header,data):
		f=open(filepath,'w') #DANGER
		print(self.delimiter.join(header),file=f)
		for row in data:
			print(self.delimiter.join([str(item) for item in row]),file=f)
		f.close()


########################################


class Table():
	"""stores table data and provides access methods

	"""

	def __init__(self,parser):
		self._parser = parser
		self._labels = []
		self._publicLabels = []
		self._data = [] #list of column data (i.e. transposed)
	
	
	def load(self,filepath):
		"""Needs __doc__

		"""
		(self._labels,data) = self._parser.load(filepath)

		#Input checks
		#Label uniqueness
		if len(self._labels) != len(set(self._labels)): raise ValueError('Repeated column names')
		#Row lengths consistent with labels and each other
		if bool(data):
			lengths = [len(row) for row in data]
			if len(self._labels) != lengths[0]: raise ValueError('Inconsistent column number')
			if max(lengths) != min(lengths): raise ValueError('Inconsistent column number')
	
		self._publicLabels = copy.copy(self._labels)
		self._data = list(transpose(data))


	def save(self,filepath):
		"""Needs __doc__

		"""
		data = transpose(self._subset(self._publicLabels))
		self._parser.save(filepath,self._publicLabels,data)

	
	def _subset(self,labels):
		data = []
		for label in labels:
			data.append(self.get(label))
		return data


	def _nRows(self):
		return len(self._data[0])


	def _labelCheck(self,label):
		if label not in self._labels: raise LookupError("Invalid column label")
	

	def get(self,label):
		"""Needs __doc__

		"""
		self._labelCheck(label)
		return self._data[self._labels.index(label)]


	def set(self,label,values):
		"""Needs __doc__

		"""
		if label not in self._labels:
			self._labels.append(label)
			self._publicLabels.append(label)
			self._data.append(values)
		else:
			self._data[self._labels.index(label)] = values


	def get_labels(self):
		"""Needs __doc__

		"""
		return self._labels


	def get_public_labels(self):
		"""Needs __doc__

		"""
		return self._publicLabels


	def set_public_labels(self,labels):
		"""Needs __doc__

		"""
		for label in labels: self._labelCheck(label)
		self._publicLabels = labels


	def hide(self,label):
		"""Needs __doc__

		"""
		if label in self._publicLabels: self._publicLabels.remove(label)


	def show(self,label):
		"""Needs __doc__

		"""
		self._labelCheck(label)
		if label not in self._publicLabels: self._publicLabels.append(label)


	def column_contains(self,label,value):
		"""Needs __doc__

		"""
		return bool(value in self.get(label))


	def apply_func(self,func,input_labels,output_label):
		"""apply_func(func,inputs,output) -> Use data in columns corresponding to list of inputs to calculate func and store results in output

		"""
		cols = (self.get(label) for label in input_labels)
		output = [func(*row) for row in transpose(cols)]
		self.set(output_label,output)


	def match(self,rules): pass
	def remove_row(self,rules): pass
	def generate_row(self,unsure_of_args_for_this): pass
	def merge_rows(self,external): pass
	def merge_columns(self,external): pass
	#Need method(s) to allow interacting with subgroups, or change in base implentation to list of grouped tables
	#Likewise need to be able to group columns


########################################


if __name__ == "__main__":
	pass
