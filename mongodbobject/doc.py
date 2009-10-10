from pymongo.dbref import DBRef
from nested import Nested
from platform import python_version

class Doc(object):
	"""The Doc class represents a single document and its features.
	"""
	
	
	def __init__(self, collection, data):
		"""A documents gets initialized with its collection and the data.
		"""
		
		self.__dict__['_data'] = Nested(data)
		self._db = collection._db
		self._collection = collection._name

	def __getattr__(self, key):
		"""Return value from data attribute.
		"""

		return getattr(self.__dict__['_data'], key)

	def __setattr__(self, key, value):
		"""Convert dicts to Nested object on setting the attribute.
		"""
		
		if type(value) == dict:
			value = Nested(value)
	
		setattr(self.__dict__['_data'], key, value)
	
	def to_dict(self):
		"""Public wrapper for converting an Nested object into a dict.
		"""
		
		dict = self.__to_dict(self.__dict__['_data'])

		if hasattr(self.__dict__['_data'], '_id'):
		    dict['_id'] = getattr(self.__dict__['_data'], '_id')

		return dict
	
	def __to_dict(self, obj):
		"""Iterate over the nested object and convert it to an dict.
		"""
		
		d = {}
		for k in dir(obj):
			# ignore values with a beginning underscore. these are private.
			if k.startswith('_'): continue
	
			# get value an type
			value = getattr(obj, k)
			obj_type = type(value)
			
			# preocess Nested objects
			if obj_type == Nested:
				d[k] = self.__to_dict(value)
			# items
			elif obj_type == Doc:
				d[k] = DBRef(value._collection, value._id)
			# lists, that can consist of Nested objects, 
			# Docs (references) or primitive values
			elif obj_type == list:
				d[k] = []
				for i in value:
					if type(i) == Nested:
						d[k].append(self.__to_dict(i))
					elif type(i) == Doc:
						d[k].append(DBRef(i._collection, i._id))
					else:
						d[k].append(i)
			# primitive values
			else:
				d[k] = value
			
		return d

	def keys(self):
		"""Get a list of keys for the current level.
		"""
		
		keys = []
		for i in dir(self.__dict__['_data']):
			# skip private members
			if not i.startswith('_') and i != '_id':
				keys.append(i)

		return keys

	def save(self):
		"""Save document to collection. 
		If document is new, set generated ID to	document _id.
		"""

		self.__dict__['_data']._id = self._db[self._collection].save(self.to_dict())
		
	def delete(self):
		"""Remove document from collection if a document id exists.
		"""
		
		if not hasattr(self.__dict__['_data'], '_id'):
			return self._db[self._collection].remove(
				{'_id': self.__dict__['_data']['_id']}
			)
		
	def __repr__(self):
		"""String representation of a document.
		"""
		
		if not hasattr(self.__dict__['_data'], '_id'):
			return 'Doc(id=<not_saved>)'
		
		# use format for python versions above 2.5
		if map(int, python_version().split('.')) < [2, 6, 0]:
			return 'Doc(id=%s)' % self.__dict__['_data']._id.url_encode()
		else:
			return 'Doc(id={0})'.format(
				self.__dict__['_data']._id.url_encode()
			)
