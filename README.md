# MongoDB object wrapper for python

## About

mongodb-object is a cocktail of the Django ORM mixed with JavaScript dot 
object notation. Every document is returned as object that can be traversed 
using the objects attributes. It is based on the awesome pymongo lib by
mike from mongodb.

A simple JSON document

    {
        'me': {'age': 24}, 
        'name': 'john', 
        'friends': ['mike', 'dwight', 'elliot']
    }
   
can now be accessed like this
   
    >>> print doc.name
    john
    >>> print friends[0]
    mike
    >>> print doc.me.age
    24
   
For those who are familar with the Django ORM, mongodb-object behaves very
similar.

## Getting started

### Installation

    git clone git://github.com/marcboeker/mongodb-object.git
    cd mongodb-object
    sudo python setup.py install
    
### Do the mambo

Let's start with a simple demonstration in the Python interactive console.
Open a MongoDB connection and start with a mongodb-object collection. The
collection is the base container for our work with mongodb-object.

    >>> from pymongo import Connection
    >>> from mongodbobject import Collection
    >>> from mongodbobject.nested import Nested
    
    >>> db = Connection().test_db
    >>> col = Collection(db, 'test_collection')

Now we create a new document using an empty document template from the
collection. This is necessary because the document needs to know to which
collection it belongs

    >>> doc = col.new()
    >>> doc.name = 'john'
    >>> doc.person = Nested()
    >>> doc.person.age = 24
    >>> doc.person.gender = 'male'
    >>> doc.save()
    >>> doc
    Doc(id=04be8d4a41950c76e8000000)
    
We can also reference documents on the fly. Retrieval is powered by lazy
loading. Only when you select an attribute of a referenced document, the
document will be retrieved.

    >>> doc2 = col.new()
    >>> doc2.friends = [doc]
    >>> doc2.save()
    >>> doc2.friends
    [Doc(id=04be8d4a41950c76e8000000)]
    >>> doc2.friends[0].person.age
    24
    
### Finding documents

As a collection holds all documents, we have to ask the collection when
we want to find a special document.

    >>> col.find_one(person__age=24)
    Doc(id=04be8d4a41950c76e8000000)
    >>> col.find_one(person__age__lt=25)
    Doc(id=04be8d4a41950c76e8000000)
    >>> col.find_one(person__age__lt=24)
    None
    >>> col.find_one(person__age=24, name='john')
    Doc(id=04be8d4a41950c76e8000000)
    
As you can see, we emulate the dot notation of embedded documents using
the __ chars like Django does. We can also append query operators 
($lt, $lte, $gt, $gte, $ne, $nin, $in, $all, $size) at the end.

You cannot only query for one document, you can retrieve also a list of
documents using find() instead of find_one().

    >>> doc_list = col.find()
    >>> doc_list
    <mongodbobject.doclist.DocList instance at 0x11d5f80>
    >>> doc_list.count()
    2
    >>> for doc in doc_list:
    ...     print doc, doc.keys()
    ... 
    Doc(id=c8c88d4a41950c42e9000000) ['name', 'person']
    Doc(id=c8c88d4a41950c42e9010000) ['friends']
    
find() accepts the same parameters as find_one() does.

### Bulk update and remove

To do a bulk update or remove, we use the query() method.

    >>> col.query(name='john').update(set__name='jack')
    >>> col.find_one(name='jack').name
    jack
    >>> col.query(name='jack').remove()
    >>> col.find().count()
    1

update() makes use of the MongoDB update operators 
($set, $inc, $push, $pushAll, $pull, $pullAll). You have to prefix the 
document key with one of the operators above. Embedded docs can be
accessed using the previously mentiond __ chars. For example:

    set__person__gender=10
    
### Document list options (count, skip, limit, sort)

Using the find() method, you get a list of documents. This list can be
sorted, or paginated using the known methods from pymongo.

    >>> col.find(name='jack').count()
    1
    >>> col.find().skip(1).limit(1).next()
    Doc(id=fecc8d4a41950c83e9010000)
   
    >>> for doc in col.find().sort(friends=1):
    ...    print doc
    Doc(id=82cd8d4a41950c8fe9000000)
    Doc(id=82cd8d4a41950c8fe9010000)
    
And now sort on another key.
    
    >>> for doc in col.find().sort(name=1):
    ...    print doc
    Doc(id=82cd8d4a41950c8fe9010000)
    Doc(id=82cd8d4a41950c8fe9000000)
    
### Document operations

A single document can be modified and afterwards saved without any 
restrictions. You can also delete the document, return its keys or
get a dict represntation.

    >>> col.find_one(name='jack').keys()
    ['name', 'person']
    >>> doc = col.find_one(name='jack')
    >>> doc.name = 'harry'
    >>> doc.save()
    >>> col.find_one(name='harry').name
    harry
    >>> doc.delete()
    >>> col.find_one(name='jack')
    None