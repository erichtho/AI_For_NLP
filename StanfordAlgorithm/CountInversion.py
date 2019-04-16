'''
计算向量的逆的个数
'''


def count_split_inv(left_sorted, right_sorted):
    merge_sorted = []
    split_inv_cnt = 0
    n_l = len(left_sorted)
    n_r = len(right_sorted)
    j = 0
    i = 0
    while i<n_l and j<n_r:
        if left_sorted[i]<=right_sorted[j]:
            merge_sorted.append(left_sorted[i])
            i += 1
        else:
            split_inv_cnt += n_l - i
            merge_sorted.append(right_sorted[j])
            j += 1
    if i<n_l:
    	merge_sorted += left_sorted[i:]
    if j<n_r:
    	merge_sorted += right_sorted[j:]
    return split_inv_cnt, merge_sorted

def count_inversions(A):
    n = len(A)

    if n<=1:
        return 0, A

    left_side = A[:int(n/2)][:]
    right_side = A[int(n/2):][:]


    left_num, left_sorted = count_inversions(left_side)
    right_num, right_sorted = count_inversions(right_side)

    split_num, merge_sorted = count_split_inv(left_sorted, right_sorted)

    return left_num+right_num+split_num, merge_sorted


def test():
    sample1 = [1,3,5,2,4,6]
    sample2 = [1,2,3,4,5,6,7]
    sample3 = [7,6,5,4,3,2,1]
    sample4 = [1,1,1,1,1,1,1]
    sample5 = [1,5,2,6,8,7]
    assert(count_inversions(sample1)[0]==3)
    assert(count_inversions(sample2)[0]==0)
    assert(count_inversions(sample3)[0]==21)
    assert(count_inversions(sample4)[0]==0)
    assert(count_inversions(sample5)[0]==2)

    print("test pass")

if __name__=='__main__':
    test()