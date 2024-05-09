import random
# from Chan.BichromaticClosestPair import BichromaticClosestPair
# from Chan.Util import ClosestPairElem
from BCNaive import BCNaive
from BCFaster import BCFaster
from BCFasterNN import BCFasterNN

def random_point():
    return (random.random(), random.random())
    

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


def create_test_sequence(q, n):
    test_seq = []
    cursize = [n, n]
    for _ in range(q):
        if min(cursize) > 0:
            command = random.choice(['insert', 'remove', 'query'])
        else:
            command = random.choice(['insert', 'query'])

        if command == 'insert':
            s = random.randint(0, 1)
            test_seq.append((command, random_point(), s))
            cursize[s] += 1
        elif command == 'remove':
            s = random.randint(0, 1)
            test_seq.append((command, random.randint(0, cursize[s]-1), s))
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
                if ans[0]>ans[1]:
                    ans = (ans[1], ans[0])
                output.append(ans)
        return output
        
from pprint import pprint
import time

n = 2000
q = 2000
test_seq = create_test_sequence(q, n)

def timefunc(func):
    start_time = time.time()
    output = func()
    end_time = time.time()
    return (end_time - start_time, output)

# t1, output1 = timefunc(lambda: Tester(BCNaive, n, 1, test_seq).get_output())
t2, output2 = timefunc(lambda: Tester(BCFaster, n, 1, test_seq).get_output())
t3, output3 = timefunc(lambda: Tester(BCFasterNN, n, 1, test_seq).get_output())

# print("Output matches:", output1 == output2 == output3)
assert output2 == output3
# print(f"Time taken (BCNaive): {t1:.2f} seconds")
print(f"Time taken (BCFaster): {t2:.2f} seconds")
print(f"Time taken (BCFasterNN): {t3:.2f} seconds")
