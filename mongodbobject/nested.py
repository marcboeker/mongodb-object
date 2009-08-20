class Nested(object):
	"""Nested represents a dumb object, that converts a given dict 
	to internal attributes.
	"""
	
	
	def __init__(self, d={}):
		"""Convert dict to class attributes.
		"""
		
		for a, b in d.items():
			# handle lists and tuples
			if isinstance(b, (list, tuple)):
				setattr(self, a, 
					[Nested(x) if isinstance(x, dict) else x for x in b])
			# the rest
			else:
				setattr(self, a, Nested(b) if isinstance(b, dict) else b)
