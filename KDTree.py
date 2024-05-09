import matplotlib.pyplot as plt

def distance(p1, p2):
    return sum((x - y) ** 2 for x, y in zip(p1, p2))

NDIM = 2
MINX = -0.1
MAXX = 1.1
MINY = -0.1
MAXY = 1.1
class KDTree:
    class Node:
        def __init__(self, point, dim, left=None, right=None):
            self.point = point
            self.left = left
            self.right = right
            self.dim = dim
            self.low = [float('-inf')] * NDIM
            self.high = [float('inf')] * NDIM
            self.minimal = [(float('inf'), float('inf'))] * NDIM
            self.maximal = [(float('-inf'), float('-inf'))] * NDIM
            self.dead = False
        
        def set_bounds(self):
            self.low = list(self.point)
            self.high = list(self.point)
            self.minimal = [self.point] * NDIM
            self.maximal = [self.point] * NDIM
            if self.left is not None:
                for i in range(NDIM):
                    self.low[i] = min(self.low[i], self.left.low[i])
                    self.high[i] = max(self.high[i], self.left.high[i])
                    if self.left.minimal[i][i] < self.minimal[i][i]:
                        self.minimal[i] = self.left.minimal[i]
                    if self.left.maximal[i][i] > self.maximal[i][i]:
                        self.maximal[i] = self.left.maximal[i]
            if self.right is not None:
                for i in range(NDIM):
                    self.low[i] = min(self.low[i], self.right.low[i])
                    self.high[i] = max(self.high[i], self.right.high[i])
                    if self.right.minimal[i][i] < self.minimal[i][i]:
                        self.minimal[i] = self.right.minimal[i]
                    if self.right.maximal[i][i] > self.maximal[i][i]:
                        self.maximal[i] = self.right.maximal[i]

        def contains(self, point):
            return all(self.low[d] <= point[d] <= self.high[d] for d in range(NDIM))
        
        def distance_to_box(self, point):
            dist = 0
            for d in range(NDIM):
                if point[d] < self.low[d]:
                    dist += (self.low[d] - point[d]) ** 2
                elif point[d] > self.high[d]:
                    dist += (point[d] - self.high[d]) ** 2
            return dist

    def __init__(self, points, dim=2, plot=False):
        self.dim = dim
        self.root = self.build_tree(points, 0)
        if plot:
            self.fig, self.ax = plt.subplots(figsize=(8, 8))

    def build_tree(self, points, dim):
        if not points:
            return None
        points.sort(key=lambda x: x[dim])

        median = len(points) // 2
        node = self.Node(points[median], dim, 
            self.build_tree(points[:median], (dim + 1) % self.dim), 
            self.build_tree(points[median + 1:], (dim + 1) % self.dim)
        )
        node.set_bounds()
        return node

    def nearest_neighbor(self, point, node=None):
        if node is None:
            self.best = float('inf')
            self.best_point = None
            return self.nearest_neighbor(point, self.root)
        
        new_dist = distance(point, node.point)
        if not node.dead and new_dist < self.best:
            self.best = new_dist
            self.best_point = node.point

        if point[node.dim] < node.point[node.dim]:
            if node.left is not None:
                if node.left.contains(point) or node.left.distance_to_box(point) < self.best:
                    new_dist_left, new_point_left = self.nearest_neighbor(point, node.left)
                    if new_dist_left < self.best:
                        self.best = new_dist_left
                        self.best_point = new_point_left
            if node.right is not None:
                if node.right.contains(point) or node.right.distance_to_box(point) < self.best:
                    new_dist_right, new_point_right = self.nearest_neighbor(point, node.right)
                    if new_dist_right < self.best:
                        self.best = new_dist_right
                        self.best_point = new_point_right
        else:
            if node.right is not None:
                if node.right.contains(point) or node.right.distance_to_box(point) < self.best:
                    new_dist_right, new_point_right = self.nearest_neighbor(point, node.right)
                    if new_dist_right < self.best:
                        self.best = new_dist_right
                        self.best_point = new_point_right
            if node.left is not None:
                if node.left.contains(point) or node.left.distance_to_box(point) < self.best:
                    new_dist_left, new_point_left = self.nearest_neighbor(point, node.left)
                    if new_dist_left < self.best:
                        self.best = new_dist_left
                        self.best_point = new_point_left
           
        return self.best, self.best_point
    


    def remove(self, point):
        self.remove_node(point, self.root)

    # def remove_node(self, point, node):
    #     if node is None:
    #         return
    #     if point == node.point:
    #         node.dead = True
    #         return
    #     if point[node.dim] < node.point[node.dim]:
    #         self.remove_node(point, node.left)
    #     else:
    #         self.remove_node(point, node.right)
    
    def remove_node(self, point, node):
        if node is None:
            return None
        if point == node.point:
            node.dead = True
            if node.left is not None:
                replacement = node.left.maximal[node.dim]
                node.point = replacement
                node.left = self.remove_node(replacement, node.left)
            elif node.right is not None:
                replacement = node.right.minimal[node.dim]
                node.point = replacement
                node.right = self.remove_node(replacement, node.right)
            else:
                return None
            node.set_bounds()
            return node
        if point[node.dim] < node.point[node.dim]:
            node.left = self.remove_node(point, node.left)
        else:
            node.right = self.remove_node(point, node.right)
        node.set_bounds()
        return node

    def plot(self, node=None, min_x=MINX, max_x=MAXX, min_y=MINY, max_y=MAXY, depth=0):
        if node is None:
            node = self.root
            # plt.figure(figsize=(8, 8))
            # plt.title("KD-Tree Structure")
            # plt.grid(False)

       
        # Determine the axis and the next min/max
        axis = depth % self.dim
        if axis == 0:
            # Vertical line
            self.ax.axvline(x=node.point[0], ymin=(min_y - MINY) / (MAXY - MINY), ymax=(max_y - MINY) / (MAXY - MINY), color='r')
            if node.left:
                self.plot(node.left, min_x, node.point[0], min_y, max_y, depth + 1)
            if node.right:
                self.plot(node.right, node.point[0], max_x, min_y, max_y, depth + 1)
        else:
            # Horizontal line
            self.ax.axhline(y=node.point[1], xmin=(min_x - MINX) / (MAXX - MINX), xmax=(max_x - MINX) / (MAXX - MINX), color='b')
            if node.left:
                self.plot(node.left, min_x, max_x, min_y, node.point[1], depth + 1)
            if node.right:
                self.plot(node.right, min_x, max_x, node.point[1], max_y, depth + 1)
        
        # Draw the point
        self.ax.plot(node.point[0], node.point[1], 'ko', markersize=10)
        if node == self.root:
            self.ax.set_xlim(min_x, max_x)
            self.ax.set_ylim(min_y, max_y)
            # plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class KDTreeVisualization(KDTree):
    def __init__(self, points, plot=False):
        super().__init__(points, plot=plot)
        self.search_path = []

    def nearest_neighbor(self, point, node=None, depth=0):
        if node is None:
            node = self.root
            self.search_path = []
        
        if not node.dead:
            best = distance(point, node.point)
            best_point = node.point
            self.search_path.append((node.point, 'current', best))
        else:
            best = float('inf')
            best_point = None

        if node.left is not None and (node.left.contains(point) or node.left.distance_to_box(point) < best):
            best_left, best_point_left = self.nearest_neighbor(point, node.left, depth + 1)
            if best_left < best:
                best = best_left
                best_point = best_point_left
        if node.right is not None and (node.right.contains(point) or node.right.distance_to_box(point) < best):
            best_right, best_point_right = self.nearest_neighbor(point, node.right, depth + 1)
            if best_right < best:
                best = best_right
                best_point = best_point_right
        self.search_path.append((best_point, 'best', best))
        return best, best_point

    def update(self, frame):
        self.ax.clear()
        self.plot(self.root)
        point, status, dist = self.search_path[frame]
        if status == 'current':
            self.ax.plot(point[0], point[1], 'go', markersize=20)  # green for current node
        elif status == 'best':
            self.ax.plot(point[0], point[1], 'ro', markersize=20)  # red for best found
        self.ax.plot(self.target[0], self.target[1], 'o', color='orange')  # orange for target point
        self.ax.add_patch(plt.Circle(self.target, dist, color='orange', fill=False))

    def animate_search(self, target_point, interval=2000):
        self.target = target_point
        _, _ = self.nearest_neighbor(target_point)
        ani = FuncAnimation(self.fig, self.update, frames=len(self.search_path), repeat=False, interval=interval)
        plt.show()

import random
if __name__ == '__main__':
    # Example usage
    # points = [(0.1, 0.2), (0.4, 0.2), (0.3, 0.6), (0.9, 0.9)]
    points = [(random.random(), random.random()) for _ in range(10)]
    tree = KDTree(points, plot=True)
    tree.plot()
    plt.show()
    # tree.animate_search((0.8, 0.7))
        

