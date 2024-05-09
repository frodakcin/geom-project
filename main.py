from BichromaticClosestPair import PQStructure
from Util import Point
import random

if __name__ == "__main__":
    random.seed(0)
    P = [
        Point.new_random(2, f"P{i}") for i in range(1, 500)
    ]
    Q = [
        Point.new_random(2, f"Q{i}") for i in range(1, 500)
    ]
    pq = PQStructure.new(P, Q)

    print(pq.find_closest_pair())
    pq.display_all()

