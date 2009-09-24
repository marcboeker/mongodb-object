from pymongo import Connection
from mongodbobject import Collection
from mongodbobject.nested import Nested
    
db = Connection().test_db
col = Collection(db, 'test_collection')
col.query().remove()

doc = col.new()
doc.name = 'john'
doc.person = Nested()
doc.person.age = 24
doc.person.gender = 'male'
doc.save()
print doc

doc2 = col.new()
doc2.friends = [doc]
doc2.save()
print doc2.friends
print doc2.friends[0].person.age

print col.find_one(person__age=24)
print col.find_one(person__age__lt=25)
print col.find_one(person__age__lt=24)
print col.find_one(person__age=24, name='john')

doc_list = col.find()
print doc_list
print doc_list.count()

for doc in doc_list:
    print doc, doc.keys()
    
    
col.query(name='john').update(set__name='jack')
print col.find_one(name='jack').name
col.query(name='john').remove()

print col.find().count()

print col.find(name='jack').count()

print col.find().skip(1).limit(1).next()

for doc in col.find().sort(friends=1):
    print doc
    
for doc in col.find().sort(name=1):
    print doc
    
print col.find_one(name='jack').keys()

doc = col.find_one(name='jack')
print doc
doc.name = 'harry'
doc.save()

print col.find_one(name='harry').name
print doc
doc.delete()
print col.find_one(name='jack')