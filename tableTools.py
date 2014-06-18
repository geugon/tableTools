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
		data = transpose(self._subset_col(self._publicLabels))
		self._parser.save(filepath,self._publicLabels,data)

	
	def _subset_col(self,labels):
		data = []
		for label in labels:
			data.append(self.get(label))
		return data


	def _nRows(self):
		return len(self._data[0])


	def _labelCheck(self,label):
		if label not in self._labels: raise LookupError("Invalid column label")


	def _divide_by_rules(self,rules):
		list(map(self._labelCheck,rules.keys()))
		indexed_rules = dict([(self._labels.index(k),v) for k,v in rules.items()])

		match,differ = [],[]
		for row in transpose(self._data):
			if all([row[k] in v for k,v in indexed_rules.items()]):
				match.append(row)
			else:
				differ.append(row)
		return match,differ	


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

	
	def subset(self,rules):
		"""subset(rules) -> returns a Table containing rows that meet the conditions specified in the rules.
		Each rule key is a column label, whose value is a list of valid matches.

		"""

		#Apply rules and record matches
		output = self._divide_by_rules(rules)[0]

		#Create new subset
		subset = Table(self._parser)
		subset._labels = copy.copy(self._labels)
		subset._publicLabels = copy.copy(self._publicLabels)
		subset._data = list(transpose(output))
		return subset


	def remove_rows(self,rules):
		"""remove_rows(rules) -> removes rows specifided by rules.
		Each rule key is a column label, whose value is a list of valid matches.

		"""
		output = self._divide_by_rules(rules)[1]
		self._data = list(transpose(output))


	def merge_columns(self,external):
		"""merge_columns(external) -> Add columns from a seperate Table.  If there is a column name conflict, the current column is retained.

		"""
		#Currently requires extranal to have same implementation instead of properly using interface
		#Checks
		if len(self._data[0])!=(external._data[0]): raise ValueError("Inconsistent number of rows for column merge")

		labels = [label for label in external._labels if label not in self._labels]#should use filter and lambda function instead
		for label in labels:
			self._data.append(copy.copy(external.get(label)))
			self._labels.append(label)
			if label in external._publicLabels: self._publicLabels.append(label)


	def merge_rows(self,external):
		"""merge_columns(external) -> Add columns from a seperate Table.  If there is a column name conflict, the current column is retained.

		"""
		#Currently requires extranal to have same implementation instead of properly using interface
		#Checks
		if self._labels != external._labels: raise ValueError("Inconsistent columns")

		self._data = list(transpose( transpose(self._data)+transpose(external._data) ))
		

	def generate_row(self,unsure_of_args_for_this): pass
	#Need method(s) to allow interacting with subgroups, or change in base implentation to list of grouped tables
	#Likewise need to be able to group columns


########################################


if __name__ == "__main__":
	pass
