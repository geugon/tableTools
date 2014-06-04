class PlainTextParser():
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



class Table():
	def __init__(self,parser):
		self._parser = parser
		self._labels = None
		self._data = None
	def load(self,filepath):
		(self._labels,self._data) = self._parser.load(filepath)
	def save(self,filepath):
		self._parser.save(filepath,self._labels,self._data)



if __name__ == "__main__":
	#Test
	parser = PlainTextParser('e')
	table = Table(parser)
	table.load('input.txt')
	print(table._labels)
	print(table._data)
	table.save('output.txt')
