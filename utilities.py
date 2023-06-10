import numpy as np

def compute_euclidean_distance(point1, point2) -> float:
    """
    Computes the Euclidean distance between the two provided points.

    Args:
        - point1 (array-like): The first point.
        - point2 (array-like): The second point.

    Returns:
        float: the Euclidean distance between the two points.
    """

    return np.linalg.norm(point2 - point1)

    # return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def compute_manhattan_distance(point1, point2) -> float:
    """
    Computes the Manhattan distance between the two provided points.

    Args:
        - point1 (array-like): the first point.
        - point2 (array-like): the second point.
    """

    return np.sum(np.abs(point1-point2))
