.. _using:

==============
Using ``xrtr``
==============

``xrtr`` is a fast (and will be faster) path router for Python written in Cython, primarily for web frameworks but it's flexible to be used with other conventions as well. It is based on a compressed dynamic trie (radix tree) structure for efficient matching, with support for variables, endpoints, layered middlewares (or any other objects) and very fast speeds provided by a Cython optimization of the tree.

The tree
--------

To use the ``xrtr`` router, you simply need to instantiate the ``RadixTree`` object:

.. code-block:: pycon

    >>> from xrtr import RadixTree

    >>> tree = RadixTree()

Now, let's say you have an endpoint (object, function) to be run without variables:

.. code-block:: pycon

    >>> def myendpoint():
    ...     return "hello, world"

    >>> tree.insert("/", myendpoint, ["GET"])

    >>> tree.get("/", "GET")
    (<function __main__.myendpoint()>, [], {})

If you want to grab variables, you can choose to get a variable between the ``separator`` (defaults to ``/``) or glob everything that comes after.

To create a simple variable, use a colon ``:`` as identifier:

.. code-block:: pycon

    >>> tree.insert("/foo/:bar", myendpoint, ["GET"])

    >>> tree.get("/foo/hello", "GET")
    (<function __main__.myendpoint()>, [], {'bar': 'hello'})

If you want to glob everything in a variable, use an asterisk ``*`` as identifier:

.. code-block:: pycon

    >>> tree.insert("/static/*path", myendpoint, ["GET"])

    >>> tree.get("/static/my/file/may/be/somewhere.py", "GET")
    (<function __main__.myendpoint()>, [], {'path': 'my/file/may/be/somewhere.py'})

.. note::

    You may have already noticed that the method ``RadixTree.get`` returns a ``tuple`` of three objects: the endpoint (or None), a list of middlewares (see the next chapter) and a dictionary of the variables and its values (if any matches). In case of no matches or an endpoint object / function is not found, the default return will be ``None, [], {}``.

Middlewares
-----------

Sometimes, you want to add a function or, most commonly, a middleware to be executed before or after a request, to any or certain points. Luckily, to execute a middleware in certain points may be hard on most solutions, either leaving you without any alternatives to implement one or based on subclassing views, routes, handlers, you name it. ``xrtr`` aims to make this very, very simple.

Nothing better than a simple example:

.. code-block:: pycon

    >>> def mymiddleware():
    ...     return "hello, middle world"

    >>> tree.insert("/foo", mymiddleware, ["GET"], no_conflict=True)

    >>> tree.get("/foo/hello", "GET")
    (<function __main__.myendpoint()>, [<function __main__.mymiddleware()>], {'bar': 'hello'})

Those middlewares can be stacked without replication and, again, can be a function, object, anything you find appropriate. Just don't forget to add the keyword ``no_conflict`` to ``True`` when invoking the ``RadixTree.insert`` method.

Configuring identifiers
-----------------------

In case you're wondering: "*another path based router*?", don't worry: the ``separator`` (defaults to ``/``) and ``variable`` (defaults to ``:``) can be configurable (as long as they're `punctuations <https://docs.python.org/3.7/library/string.html#string.punctuation>`_). The glob identifier (defaults to ``*``) is not configurable.

There are two ways of changing the identifiers: using the class constructor or changing them at runtime.

.. warning::

    You can only change the identifiers prior to inserting routes, otherwise it raises ``ValueError``.

Changing at runtime
~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> from xrtr import RadixTree

    >>> tree = RadixTree()

    >>> tree.SEPARATOR = "."
    >>> tree.SEPARATOR
    '.'

    >>> tree.VARIABLE = "$"
    >>> tree.VARIABLE
    '$'

    >>> tree.insert(".foo.$bar", object, ["FOO"])
    >>> tree.get(".foo.hello", "FOO")
    (object, [], {'bar': 'hello'})

    >>> tree.config
    {'variable': '$', 'separator': '.'}

Using the constructor
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> from xrtr import RadixTree

    >>> tree = RadixTree(separator=".", variable="$")

    >>> tree.SEPARATOR
    '.'

    >>> tree.VARIABLE
    '$'

    >>> tree.insert(".foo.$bar", object, ["FOO"])
    >>> tree.get(".foo.hello", "FOO")
    (object, [], {'bar': 'hello'})

    >>> tree.config
    {'variable': '$', 'separator': '.'}

Method utilities
----------------

Starting with ``xrtr`` 0.2.0, some changes were required to quickly identify if the given ``route`` does in fact exists, but the requested ``method`` is not available. Enter in scene: the ``sentinel`` object.

Sentinel object
~~~~~~~~~~~~~~~

Everytime you search for a route and its specific method, sometimes the route even exists (let's say, ``/foo``), but the requested method doesn't (``GET`` exists, ``OPTIONS`` don't). This can be quickly checked against the ``sentinel`` object (or property, in ``xrtr`` case):

.. code-block:: pycon

    >>> from xrtr import RadixTree

    >>> tree = RadixTree()

    >>> tree.insert("/foo", some_endpoint, ["GET"])

    >>> handler, middlewares, params = tree.get("/foo", "OPTIONS")

    >>> handler is tree.sentinel
    True

This way, it is simple to deal with more fine grained errors, such as ``HTTP 405``.

Available methods
~~~~~~~~~~~~~~~~~

In case you need just to get the available methods of one simple endpoint (for informational purposes), you can perform that by using the ``methods_for`` method:

    >>> from xrtr import RadixTree

    >>> tree = RadixTree()

    >>> tree.insert("/foo", some_endpoint, ["GET"])

    >>> tree.methods_for("/foo")
    {'GET'}

Code coverage
~~~~~~~~~~~~~

For now, ``xrtr`` may have a low coverage (than intended), but that's due to a characteristic of Cython projects where ``coverage`` won't catch function signatures. See more regarding this `here <https://groups.google.com/d/topic/cython-users/N6bgNQvEdVg/discussion>`_. When a less hacky, integrated solution becomes available, it shall be used.
