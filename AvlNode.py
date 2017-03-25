class AvlNode:
	def __init__(self, key):
		self.key = key
		self.parent = None
		self.leftChild = None
		self.rightChild = None
		self.height = 0

	def is_leaf(self):
		return self.height == 0

	def max_children_height(self):
		if self.leftChild and self.rightChild:
			return max(self.leftChild.height, self.rightChild.height)
		elif self.leftChild and not self.rightChild:
			return self.leftChild.height
		elif not self.leftChild and self.rightChild:
			return self.rightChild.height
		else:
			return -1

	def balance(self):
		return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)
