import CountInversion

def read_arr_from_file(path):
    with open(path) as f:
        # print(f.read().split()[:20])
        arr = [int(i.strip()) for i in f.read().strip().split('\n')]
        # arr = []
        return arr

if __name__=='__main__':
    
    arr = read_arr_from_file('IntegerArray.txt')
    print(CountInversion.count_inversions(arr)[0])