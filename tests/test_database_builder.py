from src import builder
from pathlib import Path


def test_valid_image_jpg():
    assert builder.is_valid_image(Path('foo.jpg'))


def test_valid_image_jpeg():
    assert builder.is_valid_image(Path('foo.jpeg'))


def test_valid_image_png():
    assert builder.is_valid_image(Path('foo.png'))


def test_valid_image_gif():
    assert builder.is_valid_image(Path('foo.gif'))


def test_valid_image_fails_non_valid():
    assert not builder.is_valid_image(Path('foo.txt'))
