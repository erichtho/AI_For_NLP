import math
import matplotlib.pyplot as plt
import random
import numpy as np

class Point():
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y

    def to_string(self):
        return '('+str(self.x)+','+str(self.y)+')'


    @staticmethod
    def euclidean_distance(point_1, point_2):
        return math.sqrt((point_1.x-point_2.x)**2+(point_1.y-point_2.y)**2)

    @staticmethod
    def sort_by_x_y(points):
        points.sort(key=lambda p:(p.x, p.y))
        return points

    @staticmethod
    def batch_to_string(points):
        return ' '.join(['('+str(p.x)+','+str(p.y)+')' for p in points])

class ClosestPair():
    
    def __init__(self, points):
        assert(len(points)>=2)

        self.points = points
        self.sorted_points = Point.sort_by_x_y(points)

    def get_closest_pair(self):
        assert(self.sorted_points is not None)
        return ClosestPair.closest_pair(self.sorted_points)


    @staticmethod
    def closest_pair(sorted_points):
        assert(len(sorted_points)>0)
        if len(sorted_points)==1:
            return sorted_points[0],sorted_points[0],np.inf

        elif len(sorted_points)==2:
            return sorted_points[0], sorted_points[1], Point.euclidean_distance(sorted_points[0], sorted_points[1])

        points_Q, points_R = ClosestPair.split_to_QR(sorted_points)

        q_point_1,q_point_2,q_d = ClosestPair.closest_pair(points_Q)
        r_point_1,r_point_2,r_d = ClosestPair.closest_pair(points_R)

        s_point_1,s_point_2,s_d = ClosestPair.closest_split_pair(sorted_points, points_Q[-1].x, min([q_d, r_d]))

        return min([(q_point_1,q_point_2,q_d), (r_point_1,r_point_2,r_d), (s_point_1,s_point_2,s_d)], key=lambda x:x[2])

    @staticmethod
    def closest_split_pair(sorted_points, rightest_Q_x, delta):
        left_idx = -1

        for i,p in enumerate(sorted_points):
            if p.x >= rightest_Q_x - delta:
                left_idx = i
                break
        
        right_idx = -1
        for i,p in enumerate(sorted_points[::-1]):
            if p.x <= rightest_Q_x + delta:
                right_idx = len(sorted_points) - i + 1
                break

        assert(left_idx!=-1 and right_idx!=-1 and left_idx<=right_idx)

        candidates = sorted_points[left_idx:right_idx+1]

        best_pair = (None, None)
        best_d = delta

        for i in range(len(candidates)-7 if len(candidates)>7 else 1):
            for j in range(1,min(len(candidates),7)):
                current_d = Point.euclidean_distance(candidates[i], candidates[i+j])
                if current_d < delta:
                    best_pair = (candidates[i], candidates[i+j])
                    best_d = current_d

        return best_pair[0], best_pair[1], best_d

    @staticmethod
    def split_to_QR(sorted_points):
        l = len(sorted_points)
        middle_x = int(l/2)
        divide_x = middle_x
        for i in range(middle_x+1, l):
            if sorted_points[i].x>sorted_points[divide_x].x:
                break
            else:
                divide_x += 1

        return sorted_points[:divide_x+1],sorted_points[divide_x+1:]



class Test():

    def get_random_points_int(self, n=100):
        xs = list(range(n))
        ys = list(range(n))
        random.shuffle(xs)
        random.shuffle(ys)
        points = [Point(x,y) for x,y in zip(xs,ys)]
       
        return points

    def get_random_points(self, n=100, x_limit=100, y_limit=100):
        return [Point(random.random()*x_limit*2-x_limit, random.random()*y_limit*2-y_limit) for i in range(n)]


    def plot_closet_pair(self, points, best_p, best_q, best_d):
        xs = [p.x for p in points]
        ys = [p.y for p in points]

        plt.scatter(xs, ys)

        plt.plot(best_p.x, best_p.y, 'ro')
        plt.plot(best_q.x, best_q.y, 'ro')

        plt.plot([best_p.x, best_q.x], [best_p.y, best_q.y])

        plt.show()

    def plot_two_part(self, left_part, right_part):
        xs_l = [p.x for p in left_part]
        ys_l = [p.y for p in left_part]

        xs_r = [p.x for p in right_part]
        ys_r = [p.y for p in right_part]

        plt.scatter(xs_l, ys_l, c='g')
        plt.scatter(xs_r, ys_r, c='b')

        plt.show()

    def test_sort(self):

        points = self.get_random_points_int()
            
        sorted_points = Point.sort_by_x_y(points)
        
        assert(all([(sorted_points[p+1].x==sorted_points[p].x and sorted_points[p+1].y>=sorted_points[p].y) \
         or sorted_points[p+1].x>sorted_points[p].x for p in range(len(sorted_points)-1)]))

        return "sort pass"

    def test_split(self):
        
        points = self.get_random_points_int()
        
        self.plot_two_part(*ClosestPair.split_to_QR(Point.sort_by_x_y(points)))
        return "split pass"

    def test_closest_pair(self):

        points = self.get_random_points(n=50)
        points = self.get_random_points_int(n=50)

        closestPair = ClosestPair(points)
        
        cp = closestPair.get_closest_pair()
        print('the closest pair is:{} and {}, distance is {}'.format(cp[0].to_string(),cp[1].to_string(),cp[2]))

        self.plot_closet_pair(points, *cp)
        return "closest pair pass"

 
if __name__=='__main__':
    
    print(Test().test_sort())

    print(Test().test_split())

    print(Test().test_closest_pair())

    print("All Test Pass.")



