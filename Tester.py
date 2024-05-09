import random
from BichromaticClosestPair import BichromaticClosestPair
# from Chan.Util import ClosestPairElem
from BCNaive import BCNaive
from BCFaster import BCFaster
from BCFasterNN import BCFasterNN


class DataGenerator:
    def __init__(self, n, seed=1, type='random'):
        self.n = n
        self.type = type
        self.points = [None, None]
        self.random = random.Random(seed)
        self.generate()

    def generate(self):
        if self.type == 'random':
            self.points[0] = [(self.random.random(), self.random.random()) for _ in range(self.n)]
            self.points[1] = [(self.random.random(), self.random.random()) for _ in range(self.n)]
        else:
            raise NotImplementedError

    def add_point(self, point, s):
        assert s in [0, 1]
        self.points[s].append(point)
        
    def remove_point_at_index(self, index, s):
        assert s in [0, 1]
        self.points[s][index] = self.points[s][-1]
        self.points[s].pop()


def create_test_sequence(q, n, seed=3):
    test_seq = []
    cursize = [n, n]
    rng = random.Random(seed)
    for _ in range(q):
        if min(cursize) > 0:
            command = rng.choice(['insert', 'remove', 'query'])
        else:
            command = rng.choice(['insert', 'query'])

        if command == 'insert':
            s = rng.randint(0, 1)
            test_seq.append((command, (rng.random(), rng.random()), s))
            cursize[s] += 1
        elif command == 'remove':
            s = rng.randint(0, 1)
            test_seq.append((command, rng.randint(0, cursize[s]-1), s))
            cursize[s] -= 1
        else:
            test_seq.append((command, None, None))
    return test_seq


class Tester:
    def __init__(self, bc_class, n, seed, test_seq):
        self.data = DataGenerator(n, seed, type='random')
        self.bc = bc_class(list(self.data.points[0]), list(self.data.points[1]))
        self.test_seq = test_seq
        
    def handle_insert(self, point, s):
        self.bc.add_point(point, s)
        self.data.add_point(point, s)

    def handle_remove(self, index, s):
        self.bc.remove_point(self.data.points[s][index], s)
        self.data.remove_point_at_index(index, s)

    def handle_query(self):
        return self.bc.query()
    
    def get_output(self):
        output = []
        for command, arg, s in self.test_seq:
            if command == 'insert':
                self.handle_insert(arg, s)
            elif command == 'remove':
                self.handle_remove(arg, s)
            else:
                ans = self.handle_query()
                if ans[0] is not None and ans[1] is not None and ans[0]>ans[1]:
                    ans = (ans[1], ans[0])
                output.append(ans)
        return output
        
from pprint import pprint
import time

n = 0
q = 10000

def timefunc(func):
    start_time = time.time()
    output = func()
    end_time = time.time()
    return (end_time - start_time, output)

seed1 = random.randint(0, 1000)
print("seed1", seed1)
seed2 = random.randint(0, 1000)
print("seed2", seed2)
test_seq = create_test_sequence(q, n, seed2)

t1, output1 = timefunc(lambda: Tester(BCNaive, n, seed1, test_seq).get_output())
# t2, output2 = timefunc(lambda: Tester(BCFaster, n, seed1, test_seq).get_output())
# t3, output3 = timefunc(lambda: Tester(BCFasterNN, n, seed1, test_seq).get_output())
t4, output4 = timefunc(lambda: Tester(BichromaticClosestPair, n, seed1, test_seq).get_output())
from NearestNeighbor import ops

# print("points:", DataGenerator(n, seed1, type='random').points)
# print("test_seq:", test_seq)
from math import log2
# print(ops)
# print(ops / (n * (log2(n))))
# print(output1)
# print(output4)
print("Output matches:", output1 == output4)
assert output1== output4
print(f"Time taken (BCNaive): {t1:.8f} seconds")
# print(f"Time taken (BCFaster): {t2:.8f} seconds")
# print(f"Time taken (BCFasterNN): {t3:.2f} seconds")
print(f"Time taken (BichromaticClosestPair): {t4:.8f} seconds")

