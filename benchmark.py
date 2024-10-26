import numpy as np


def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def filter_close_coordinates(coords: np.ndarray, min_distance: float) -> np.ndarray:
    # Sort coordinates by the x-axis
    sorted_indices = np.argsort(coords[:, 0])
    coords_sorted = coords[sorted_indices]

    filtered_coords = []
    sqr_dist=min_distance**2

    for i in range(len(coords_sorted)):
        keep = True
        for j in range(i - 1, -1, -1):
            # Break if x-distance exceeds min_distance (no need to check further)
            if (coords_sorted[i, 0] - coords_sorted[j, 0]) > min_distance:
                break

            # Check Euclidean distance for nearby points
            if euclidean_distance(coords_sorted[i], coords_sorted[j]) < sqr_dist:
                keep = False
                break

        if keep:
            filtered_coords.append(coords_sorted[i])

    return np.array(filtered_coords)


# Example usage
coords = np.array([[0, 1], [1, 1], [0, 10], [2, 13], [50, 50],[51,50]])
min_dist = 40  # Set the minimum distance threshold

# filtered = filter_close_coordinates(coords, min_dist)
# print(filtered)

import util
from resources import symbol as gui


data=util.find(gui.occupied_nomad_camp,threshold=0.1, unique_=False,asPoints=False)
print(len(data))
import time
from analitics import Memory

analytics = Memory()


def printMemory():
    results = analytics.get_results()
    print(f"Average memory usage: {results['average_memory']:.2f} MB")
    print(f"Maximum memory usage: {results['max_memory']:.2f} MB")

#
# start = time.time()
#
# filtered_data = filter_close_coordinates(data, min_dist)
#
# end = time.time() -start
# print(len(filtered_data), round(end,4))
# analytics.stop()
# printMemory()



analytics.start()
start = time.time()

field = util.ElementField((3000,3000))
field.group_occupation_area_half_side_length=int(min_dist/2)
field.group_occupation_area_half_side_length=100
field.group(data)
keys=field.keys()

end = time.time() - start
analytics.stop()

print(len(keys),round(end,4))

printMemory()

from models.objects.Point import Point
# util.showMatches(Point.From(keys),gui.occupied_nomad_camp,util.screenshot())



