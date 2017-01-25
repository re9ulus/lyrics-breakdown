class KeyLoader:

	def __init__(self, filename, delimeter=' '):
		self.filename = filename
		self.delimeter = delimeter
		self.keys = {}

	def load(self):
		self.keys = {}
		with open(self.filename, 'r') as f:
			for line in f.readlines():
				print(line)
				name, token = line.split(self.delimeter)
				self.keys[name.strip()] = token.strip()
		return self.keys
