import numpy as np

def compute_Euclidean_distance(point1, point2) -> float:
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
