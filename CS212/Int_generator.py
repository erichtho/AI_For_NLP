def ints(start, end = None):
    i = start
    while end is None or i <= end:
        yield i
        i = i + 1
    

def all_ints():
    "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
    # Your code here.
    positive = ints(1)
    negative = ints(0)
    is_odd = True
    while True:
        if is_odd:
            yield -next(negative)
        else:
            yield next(positive)
        is_odd = not is_odd

if __name__=='__main__':
    ai = all_ints()
    for i in range(10):
        print(next(ai))