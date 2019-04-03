import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    # Your code here.
    if isinstance(n, int):
        times = [timedcall(fn,*args)[0] for i in range(n)]
    else:
        total_time = 0
        times = []
        while total_time<n:
            thistime = timedcall(fn, *args)[0]
            times.append(thistime)
            total_time += thistime
    return min(times), average(times), max(times)


if __name__=='__main__':
	print(timedcalls(1.0, lambda x: x^2, 2))