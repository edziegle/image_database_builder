from collection import is_collection


def test_is_collection_returns_true_when_tuple_has_no_sub_dirs_and_has_images():
    test_tuple = ("foo/bar", [], ["foo.jpeg", ".bar", "baz.qux"])

    assert is_collection(test_tuple)


def test_is_collection_returns_false_when_tuple_has_sub_dirs():
    test_tuple = ("foo/bar", ["foo", "bar"], ["foo.jpeg"])

    assert not is_collection(test_tuple)


def test_is_collection_returns_false_when_tuple_has_no_images():
    test_tuple = ("foo/bar", [], ["foo.bax"])

    assert not is_collection(test_tuple)


def test_is_collection_returns_false_when_tuple_has_no_images_and_has_sub_dirs():
    test_tuple = ("foo/bar", ["foo", "bar"], ["foo.bax"])

    assert not is_collection(test_tuple)
