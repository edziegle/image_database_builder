from imagedirectory import is_image_directory


def test_is_image_directory_returns_true_when_tuple_has_no_sub_dirs_and_has_images():
    test_tuple = ("foo/bar", [], ["foo.jpeg", ".bar", "baz.qux"])

    assert is_image_directory(test_tuple)


def test_is_image_directory_returns_false_when_tuple_has_sub_dirs():
    test_tuple = ("foo/bar", ["foo", "bar"], ["foo.jpeg"])

    assert not is_image_directory(test_tuple)


def test_is_image_directory_returns_false_when_tuple_has_no_images():
    test_tuple = ("foo/bar", [], ["foo.bax"])

    assert not is_image_directory(test_tuple)


def test_is_image_directory_returns_false_when_tuple_has_no_images_and_has_sub_dirs():
    test_tuple = ("foo/bar", ["foo", "bar"], ["foo.bax"])

    assert not is_image_directory(test_tuple)
