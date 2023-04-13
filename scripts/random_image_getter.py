# Grabs N number of random images from Unsplash.

import os
import time

import requests
import shutil

from pathlib import Path
from typing import List

from tqdm import tqdm


def get_random_image_url() -> str:
    """
    Returns a random image URL from Unsplash.

    Returns: str
    """
    response = requests.get("https://source.unsplash.com/random")
    return response.url


def download_image(image_url, output_dir):
    """
    Downloads an image from a URL.

    Args:
        image_url: URL of the image to download.
        output_dir: directory to save the image to.

    Returns: Path to the downloaded image.
    """
    response = requests.get(image_url, stream=True)
    filename = image_url.split("/")[-1].split("?")[0]
    filename = f"{filename}.jpg"
    output_path = Path(output_dir, filename)
    with open(output_path, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    return output_path


def download_n_random_images(n: int, output_dir: Path) -> List[Path]:
    """
    Downloads N number of random images from Unsplash.

    Args:
        n: number of images to download.
        output_dir: directory to save the images to.

    Returns: list of paths to the downloaded images.
    """
    image_paths = []
    for _ in tqdm(range(n)):
        image_url = get_random_image_url()
        image_path = download_image(image_url, output_dir)
        image_paths.append(image_path)
        time.sleep(0.01)
    return image_paths


def make_test_dir():
    test_dir = Path(os.getcwd(), "../bin/sampleindex")
    test_dir.mkdir(exist_ok=True)
    for i in range(10):
        subdir = Path(test_dir, f"subdir{i}")
        subdir.mkdir(exist_ok=True)
        download_n_random_images(100, subdir)
    return test_dir


if __name__ == "__main__":
    make_test_dir()
