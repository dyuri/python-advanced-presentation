.. include:: <s5defs.txt>

======================================
Advanced Python
======================================

:Author: Gyuri Horak
:Date: $Date: 2011-05-27 14:00:00 +0200 $

.. container: handout

  Advanced Python presentation

.. |copy| unicode:: U+00A9

.. footer:: |copy| Gyuri, euedge.com

Diamond inheritance problem
===========================

``Cls.__mro__`` - method resolution order

.. sourcecode:: python

  py> class A(object): pass
  py> class B(A): pass
  py> class C(A): pass
  py> class D(B,C): pass
  py> D.__mro__
  (<class '__main__.D'>,
   <class '__main__.B'>,
   <class '__main__.C'>, 
   <class '__main__.A'>,
   <type 'object'>)

Mixins
======

You can add baseclasses runtime

.. sourcecode:: python

  class A(object): pass
  class B(object): pass
  class C(A): pass

  py> C.__bases__ += (B,)
  py> C.__mro__
  (<class '__main__.C'>, <class '__main__.A'>, 
   <class '__main__.B'>, <type 'object'>)

Variable scope
==============

* No declaration, just use any variable whenever you want
* There's ``global`` but ...
* Namespaces are dicts
* ``module.submodule.variable = 42``
* ``del`` keyword
* ``__builtins__``, ``locals()``

Variable scope
==============

.. class:: small

  .. sourcecode:: python

    def scopetest(mut, imut):
      global gvar
      gvar = 11
      lvar = 12
      mut += [2]
      imut += "apple"
      print locals()
      # {'mut': [1, 2], 'lvar': 12, 'imut': 'pineapple'}

    gvar, lvar, amut, aimut = 1, 1, [1], "pine"
    print locals()
    # {'__builtins__': <..>, 'scopetest': <function ..>, 
    # '__file__': 'scope.py', 'amut': [1], 'gvar': 1, 
    # '__package__': None, 'lvar': 1, 'aimut': 'pine', 
    # '__name__': '__main__', '__doc__': None}
    scopetest(amut, aimut) 
    print locals()
    # {'__builtins__': <..>, 'scopetest': <function ..>, 
    # '__file__': 'scope.py', 'amut': [1, 2], 'gvar': 11, 
    # '__package__': None, 'lvar': 1, 'aimut': 'pine', 
    # '__name__': '__main__', '__doc__': None}

Iterators
=========

- ``container.__iter__()`` -> iterator
- ``iterator.__iter__()`` -> iterator (self)
- ``iterator.next()`` -> next item, or StopIteration exception

.. sourcecode:: python

  py> a = [1,2,3,4,5]
  py> i = a.__iter__()
  py> i.next()
  1
  py> i.next()
  2

Generators, yield
=================

Generate the next item only when we need it

.. class:: small

  .. sourcecode:: python
    
    class Fib(object):
      def __init__(self, limit):
        self.limit = limit
      def __iter__(self):
        p0, p = 0, 1 # tuple pack/unpack
        while p < self.limit:
          yield p
          p0, p = p, p+p0
        raise StopIteration

    py> f100 = Fib(100)
    py> for x in f100: 
    ...   print x,
    1 1 2 3 5 8 13 21 34 55 89

List comprehensions
===================

The *functional way* of list creation

.. sourcecode:: python
  
  py> [x+1 for x in f100]
  [2, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90]

.. class:: small

  In Python 3 ``dicts`` and ``sets`` can be created this way as well

Itertools
=========

Useful toolset for iterators

.. sourcecode:: python

  py> from itertools import izip
  py> for x,y in izip(xrange(10), f100):
  ...   print "(%s, %s)" % (x, y),
  (0, 1) (1, 1) (2, 2) (3, 3) (4, 5) (5, 8) \
  (6, 13) (7, 21) (8, 34) (9, 55)

Coroutines (PEP-342)
====================

.. sourcecode:: python

  def grep(pattern):
    print "Looking for %s" % pattern
    while True:
      line = (yield)
      if pattern in line:
        print line

  py> g = grep("python")
  py> g.next()
  py> g.send("No snakes here.")
  py> g.send("Generators in python ROCK!")
  Generators in python ROCK!
  py> g.close()

Operator overloading
====================

.. class:: small

  .. sourcecode:: python

    class Fun(object):
      def __init__(self, function):
        self.function = function
      def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
      def __add__(self, funinst):
        def inner(*args, **kwargs):
          return funinst(self.function(*args, **kwargs))
        return Fun(inner)
    
    py> f1 = Fun(a)
    py> f1(1,2) # 3
    py> f2 = Fun(lambda x: x*x)
    py> f2(2) # 4
    py> f3 = f1+f2
    py> f3(1,2) # 9

__getattr__
===========

.. sourcecode:: python

  class JSObj(dict):
    def __getattr__(self, attr):
      return self.get(attr)
    def __setattr__(self, attr, value):
      self[attr] = value
  
  py> o = JSObj({'a': 10, 'b': 20})
  py> o.a # 10
  py> o.c # None
  py> o.c = 30
  py> o['c'] # 30
  py> o.c # 30

__dict__
========

.. sourcecode:: python

  class Borg(object):
    __shared_state = {}
    def __init__(self):
      self.__dict__ = self.__shared_state

  py> a = Borg()
  py> b = Borg()
  py> a.x = 42
  py> b.x
  42
  py> a == b
  False

http://docs.python.org/reference/datamodel.html#special-method-names

Nothing is private (again)
==========================

.. class:: small

  .. sourcecode:: python

    def hide(o):
      class Proxy(object):
        __slots__ = ()
        def __getattr__(self, name):
          return getattr(o, name)
      return Proxy()

    class A(object):
      a = 42

    py> a = hide(A())
    py> a.a
    42
    py> a.a = 43
    AttributeError: 'Proxy' object has no attribute 'a'

.. class:: incremental small

  ::

    py> a.__getattr__.func_closure[0].cell_contents
    <__main__.A object at 0x7faae6e16510>

Decorators
==========

- syntactic sugar
- class decorators in Python 3
- ``functool.wraps`` helper - sets ``__name__``, docstring, etc.
- ``@classmethod``, ``@staticmethod``

.. class:: incremental

  .. sourcecode:: python

    def funct(): pass
    funct = decorator(funct)

  .. sourcecode:: python

    @decorator
    def funct(): pass

Example decorator
=================

.. sourcecode:: python
  
  def logger(f):
    def inner(*args, **kwargs):
      print "%s called with arguments: %s; %s" % (f.__name__, args, kwargs)
      retval = f(*args, **kwargs)
      print "%s returned: %s" % (f.__name__, retval)
      return retval
    return inner

  @logger
  def mul(a,b):
    return a*b

  py> mul(1,2)
  mul called with arguments: (1, 2); {}
  mul returned: 2

Descriptors
===========

- to "hide" getter/setter methods

  * ``__get__(self, instance, owner)``
  * ``__set__(self, instance, value)``
  * ``__delete__(self, instance)``

- functions are descriptors (with ``__get__``), late binding is possible

Properties
==========

.. class:: small

  .. sourcecode:: python

    class PropEx(object):

      __a = 1
      __b = 2

      @property
      def c(self):
        return self.__a + self.__b
    
      def getA(self): return self.__a
      def setA(self, value): self.__a = value
      def delA(self): self.__a = 1

      a = property(getA, setA, delA)
      # @property, @m.setter, @m.deleter

    py> x = PropEx()
    py> x.a = 12
    py> x.c
    14
    py> x.__class__.__dict__['a'].fset
    <function setA at 0x7ff241c266e0>

Functions/methods
=================

.. class:: small

  .. sourcecode:: python

    def myclass(self):
      return self.__class__

    class A(object):
      def method(self):
        pass

    py> a = A(); a.__class__.__dict__['method']
    <function method at 0x7ff241c26cf8>
    py> a.__class__.method
    <unbound method A.method>
    py> a.method
    <bound method A.method of <__main__.A object at 0x7ff242d56bd0>>
    py> a.myclass = myclass; a.myclass()
    TypeError: myclass() takes exactly 1 argument (0 given) # ???
    py> a.myclass
    <function myclass at 0x7ff241c26b18> # :(
    py> a.myclass = myclass.__get__(a, A); a.myclass()
    <class '__main__.A'>
    py> a.myclass
    <bound method A.myclass of <__main__.A object at 0x7ff242d56bd0>> # :)

type()
======

.. class:: incremental

  - function: returns the type of the argument
  - but it's a type too
  - moreover it's the root of all classes

  .. sourcecode:: python

    py> type(object)
    <type 'type'>
    py> type(type)
    <type 'type'>

  - AND it can create new classes runtime

metaprogramming
===============

.. sourcecode:: python

  def constr(self):
    print "new instance created"
    self.foo = "foo"

  def method(self):
    print "foo: " + self.foo

  py> MyClass = type("MyClass",      # classname
                     (dict, object), # baseclasses
                     {'PI': 3.14,    # __dict__
                      'method': method, 
                      '__init__': constr})
  py> myinstance = MyClass()
  new instance created
  py> myinstance.method()
  foo: foo
  
__metaclass__
=============

When defined, it is called instead of ``type`` at class generation

.. class:: small

  .. sourcecode:: python
    
    class mymeta(type):
      def __new__(mcs, name, bases, dict):
        dict['myprop'] = 'metaclass property'
        return type.__new__(mcs, name, bases, dict)

    class A(object):
      __metaclass__ = mymeta

    py> a = A()
    py> a.myprop
    'metaclass property'

.. class:: incremental

  You can do _anything_ here, like type checking based on docstrings (or py3 annotations), decorating all the methods, create mixins ...

Questions?
==========

Thanks!
=======

