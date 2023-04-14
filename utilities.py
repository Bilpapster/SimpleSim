import numpy as np

def compute_euclidean_distance(point1, point2) -> float:
    """
    Computes the Euclidean distance between the two 2D provided points.

    Args:
        - point1 (array-like): The first point. Must be in the form (x, y).
        - point2 (array-like): The second point. Must be in the form (x, y).

    Returns:
        float: the Euclidean distance between the two points.
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
