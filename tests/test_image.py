from data_model.image import EXTENSIONS, get_images, has_images, is_image


def test_valid_image_jpg():
    assert is_image("foo.jpg")


def test_valid_image_jpeg():
    assert is_image("foo.jpeg")


def test_valid_image_png():
    assert is_image("foo.png")


def test_valid_image_gif():
    assert is_image("foo.gif")


def test_valid_image_fails_non_valid():
    assert not is_image("foo.txt")


def test_has_images_returns_true_with_one_image_in_list():
    for ext in EXTENSIONS:
        assert has_images(["foo", "bar.txt", ".venv", f"foo.{ext}"])


def test_has_images_returns_false_when_no_images():
    assert not has_images(["foo", "bar.txt", ".venv"])


def test_get_images_returns_empty_when_no_images():
    expected = []
    actual = get_images(["foo", "bar.txt", ".venv"])

    assert actual == expected


def test_get_images():
    for ext in EXTENSIONS:
        the_image = f"foo.{ext}"
        expected = [the_image]
        actual = get_images(["foo", "bar.txt", ".venv", the_image])

        assert actual == expected
