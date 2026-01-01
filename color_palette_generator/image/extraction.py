import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

from ..color import create_color


def extract_colors(image_path, n_colors=20):
    """Extract dominant colors using k-means clustering"""
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((300, 300))
    pixels = np.array(img).reshape(-1, 3)

    # Remove extreme pixels
    mask = (pixels.sum(axis=1) > 30) & (pixels.sum(axis=1) < 735)
    filtered_pixels = pixels[mask]

    if len(filtered_pixels) < n_colors:
        filtered_pixels = pixels

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(filtered_pixels)

    colors = []
    for center in kmeans.cluster_centers_:
        r, g, b = int(center[0]), int(center[1]), int(center[2])
        colors.append(create_color(r, g, b))

    return colors


def find_average_color(image_path):
    """Get overall average color of image"""
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((100, 100))
    pixels = np.array(img).reshape(-1, 3)
    avg = pixels.mean(axis=0)
    return create_color(int(avg[0]), int(avg[1]), int(avg[2]))
