import random

class MergeSort():
    
    def __init__(self):
        pass

    def sort(self, arr):
        if arr is None or len(arr)==0:
            return arr
        if len(arr)==1:
            return arr
        arr_l, arr_r = self.divide(arr)

        return self.merge(self.sort(arr_l), self.sort(arr_r))

    def divide(self, arr):
        l = len(arr)

        if l==0:
            return [], []

        elif l==1:
            return arr, []

        else:
            return arr[:int(l/2)], arr[int(l/2):]

    def merge(self, arr_l, arr_r):
        if arr_l is None or len(arr_l)==0:
            return arr_r
        elif arr_r is None or len(arr_r)==0:
            return arr_l

        merged_arr = []
        i = 0
        j = 0

        while i<len(arr_l) and j<len(arr_r):
            if arr_l[i]<arr_r[j]:
                merged_arr.append(arr_l[i])
                i += 1

            elif arr_l[i]>arr_r[j]:
                merged_arr.append(arr_r[j])
                j += 1

            elif arr_l[i]==arr_r[j]:
                merged_arr += [arr_l[i], arr_r[j]]
                i += 1
                j += 1

        if i<len(arr_l) and j==len(arr_r):
            merged_arr += arr_l[i:]

        if j<len(arr_r) and i==len(arr_l):
            merged_arr += arr_r[j:]

        return merged_arr

class Test():
   
    def get_random_arr(self, n=50, n_range=100):
        numbers = list(range(n_range))
        return [random.choice(numbers) for i in range(n)]

    def check_order(self, arr):
        return all([arr[i+1]>=arr[i] for i in range(len(arr)-1)])

    def test_sort(self):
    	print('sorted array:{}'.format(MergeSort().sort(self.get_random_arr(n=20))))

    	return 'Single test passes.'

    def test_sort_batch(self):
        assert(all([self.check_order(MergeSort().sort(self.get_random_arr())) for i in range(100)]))

        return 'Batch test passes.'

if __name__=='__main__':
    print(Test().test_sort())
    print(Test().test_sort_batch())
    print('All tests pass.')
