import pytest

from xrtr import RadixTree


def test_tree():
    tree = RadixTree()
    assert tree is not None
    assert tree.root is not None
    assert len(tree.root.children) == 0
    assert tree.root.path is None
    assert tree.root.indices == ""
    assert tree.root.methods == {}
    assert tree.root.no_conflict_methods == {}

    r = tree.get("/foo", "BAR")
    assert r[0] is None
    assert r[1] == []
    assert r[2] == {}


def test_tree_repr(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()
    assert repr(tree) == repr(tree.root)
    assert (
        repr(tree)
        == '<RadixTreeNode path: None, methods: {}, indices: "", children: []>'
    )
    assert (
        repr(tree.root)
        == '<RadixTreeNode path: None, methods: {}, indices: "", children: []>'
    )
    tree.insert("/foo", endpoint_1, ["BAR"])
    assert (
        repr(tree.root.children[0])
        == '<RadixTreeNode path: "/foo", methods: {\'BAR\': <Endpoint 1>}, indices: "", children: []>'
    )


def test_tree_validations(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()

    with pytest.raises(ValueError):
        tree.insert(None, endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("     ", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("foo", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("   foo   ", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("f/oo/", endpoint_1, ["BAR"])


def test_tree_config_1(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()
    tree.VARIABLE = "$"
    tree.SEPARATOR = "."

    tree.insert(".foo", endpoint_1, ["BAR"])
    tree.insert(".foo.$bar", endpoint_1, ["BAR"])
    tree.insert(".bar", endpoint_1, ["BAR"])
    tree.insert(".bar.*rest", endpoint_1, ["BAR"])

    r = tree.get(".foo.hello", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"bar": "hello"}

    r = tree.get(".bar.avra.cadavra.alacazam", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"rest": "avra.cadavra.alacazam"}

    assert tree.config == {"variable": "$", "separator": "."}


def test_tree_config_2(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree(variable="$", separator=".")

    tree.insert(".foo", endpoint_1, ["BAR"])
    tree.insert(".foo.$bar", endpoint_1, ["BAR"])
    tree.insert(".bar", endpoint_1, ["BAR"])
    tree.insert(".bar.*rest", endpoint_1, ["BAR"])

    r = tree.get(".foo.hello", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"bar": "hello"}

    r = tree.get(".bar.avra.cadavra.alacazam", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"rest": "avra.cadavra.alacazam"}

    assert tree.config == {"variable": "$", "separator": "."}


def test_tree_config_error():
    tree = RadixTree()

    with pytest.raises(ValueError):
        tree.VARIABLE = "/"

    with pytest.raises(ValueError):
        tree.VARIABLE = "a"

    with pytest.raises(ValueError):
        tree.VARIABLE = "$$"

    with pytest.raises(ValueError):
        tree.VARIABLE = ""

    with pytest.raises(ValueError):
        tree.VARIABLE = None

    with pytest.raises(ValueError):
        tree.SEPARATOR = ":"

    with pytest.raises(ValueError):
        tree.SEPARATOR = "a"

    with pytest.raises(ValueError):
        tree.SEPARATOR = ".."

    with pytest.raises(ValueError):
        tree.SEPARATOR = ""

    with pytest.raises(ValueError):
        tree.SEPARATOR = None

    with pytest.raises(ValueError):
        RadixTree(variable="/")

    with pytest.raises(ValueError):
        RadixTree(separator=":")

    with pytest.raises(ValueError):
        RadixTree(variable=":", separator=":")

    with pytest.raises(ValueError):
        RadixTree(variable="a", separator="b")

    with pytest.raises(ValueError):
        RadixTree(separator="b")

    with pytest.raises(ValueError):
        RadixTree(variable="a")

    with pytest.raises(ValueError):
        RadixTree(variable="::", separator="//")

    with pytest.raises(ValueError):
        RadixTree(variable="::")

    with pytest.raises(ValueError):
        RadixTree(separator="//")

    # ----------------------------------------------------------------------- #
    # all tests bellow will assume defaults
    # ----------------------------------------------------------------------- #

    RadixTree(variable="", separator="")
    RadixTree(separator="")
    RadixTree(separator="")
    RadixTree(variable=None, separator=None)
    RadixTree(variable=None)
    RadixTree(separator=None)

    tree.insert("/", object(), ["BAR"])

    with pytest.raises(ValueError):
        tree.SEPARATOR = "."

    with pytest.raises(ValueError):
        tree.VARIABLE = "$"


def test_tree_single_endpoint(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()

    tree.insert("/foo/:bar", endpoint_1, ["BAR"])

    r = tree.get("/foo/hello", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"bar": "hello"}

    r = tree.get("/foooo", "BAR")
    assert r[0] is None
    assert r[1] == []
    assert r[2] == {}


def test_tree_methods_for(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    endpoint_2 = endpoint_factory(2)

    tree = RadixTree()

    tree.insert("/foo/:bar", endpoint_1, ["BAR"])
    tree.insert("/foo/:bar", endpoint_2, ["FOO"])

    r = tree.methods_for("/foo/hello")
    assert r == {"BAR", "FOO"}

    r = tree.methods_for("/foo/world")
    assert r == {"BAR", "FOO"}

    r = tree.methods_for("/foooo")
    assert r == set()


def test_tree_root_endpoint(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()

    tree.insert("/", endpoint_1, ["BAR"])

    r = tree.get("/", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {}


def test_tree_full(endpoint_factory, middleware_factory):
    endpoint_1 = endpoint_factory(1)
    middleware_1 = middleware_factory(1)
    middleware_2 = middleware_factory(2)
    middleware_3 = middleware_factory(3)
    middleware_4 = middleware_factory(4)

    tree = RadixTree()

    tree.insert("/foo", endpoint_1, ["FOO"])
    tree.insert("/foo", middleware_1, ["FOO", "BAR"], no_conflict=True)
    tree.insert("/foo", middleware_1, ["BAR"], no_conflict=True)
    tree.insert("/foo/:name", endpoint_1, ["FOO", "BAR"])
    tree.insert(
        "/foo/:name/:x", middleware_2, ["FOO", "BAR"], no_conflict=True
    )
    tree.insert("/foo/:name/:x/:y", endpoint_1, ["FOO", "BAR"])
    tree.insert("/static/*path", endpoint_1, ["FOO"])

    with pytest.raises(ValueError):
        tree.insert("/foo/:bar", endpoint_1, ["FOO"])

    with pytest.raises(KeyError):
        tree.insert("/foo", middleware_2, ["FOO"])

    r = tree.get("/foo/hello", "FOO")
    assert r[0] == endpoint_1
    assert r[1] == [middleware_1]
    assert r[2] == {"name": "hello"}

    r = tree.get("/foo/hello/a/b", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == [middleware_1, middleware_2]
    assert r[2] == {"name": "hello", "x": "a", "y": "b"}

    r = tree.get("/static/path/to/my/file.py", "FOO")
    assert r[0] == endpoint_1
    assert r[1] == []
    assert r[2] == {"path": "path/to/my/file.py"}

    tree.insert(
        "/foo/:name/:x", middleware_3, ["FOO", "BAR"], no_conflict=True
    )

    tree.insert("/foo/:name/:x/:y", middleware_4, ["FOO"], no_conflict=True)

    r = tree.get("/foo/hello/a/b", "FOO")
    assert r[0] == endpoint_1
    assert r[1] == [middleware_1, middleware_2, middleware_3, middleware_4]
    assert r[2] == {"name": "hello", "x": "a", "y": "b"}

    r = tree.get("/foo/hello/aa", "FOO")
    assert r[0] is None
    assert r[1] == []
    assert r[2] == {}

    r = tree.get("/foo/hello/a/b", "BAZ")
    assert r[0] is tree.sentinel
    assert r[1] == []
    assert r[2] == {}

    m = tree.methods_for("/foo/hello/aa")
    assert m == set()

    m = tree.methods_for("/foo/hello/a/b")
    assert m == {"BAR", "FOO"}

    m = tree.methods_for("/foo")
    assert m == {"FOO"}

    m = tree.methods_for("/static/abra/cadabra")
    assert m == {"FOO"}


def test_sentinel(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()
    tree.insert("/hello/:bar", endpoint_1, ["BAR"])

    r = tree.get("/hello/world", "BAZ")
    assert r[0] is tree.sentinel
    assert r[1] == []
    assert r[2] == {}


def test_duplicate_parameters(endpoint_factory):
    endpoint_1 = endpoint_factory(1)
    tree = RadixTree()
    tree.insert("/hello/:bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("/hello/:bar/:bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("/hello/:bar/world/:bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        tree.insert("/hello/:bar/world/*bar", endpoint_1, ["BAR"])

    another_tree = RadixTree(variable=".", separator="|")
    another_tree.insert("|hello|.bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        another_tree.insert("|hello|.bar|.bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        another_tree.insert("|hello|.bar|world|.bar", endpoint_1, ["BAR"])

    with pytest.raises(ValueError):
        another_tree.insert("|hello|.bar|world|*bar", endpoint_1, ["BAR"])


def test_tree_middleware_first(endpoint_factory, middleware_factory):
    endpoint_1 = endpoint_factory(1)
    middleware_1 = middleware_factory(1)

    tree = RadixTree()

    tree.insert("/hello", middleware_1, ["BAR"], no_conflict=True)
    tree.insert("/hello/world", endpoint_1, ["BAR"])

    r = tree.get("/hello", "BAR")
    assert r[0] is None
    assert r[1] == []
    assert r[2] == {}

    r = tree.get("/hello/world", "BAR")
    assert r[0] == endpoint_1
    assert r[1] == [middleware_1]
    assert r[2] == {}
