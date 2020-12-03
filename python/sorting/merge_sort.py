def merge_sort(lst):
    if len(lst) < 2: return lst

    mid_x = len(lst) // 2

    return merge(
        merge_sort(lst[:mid_x]),
        merge_sort(lst[mid_x:])
    )


def merge(left, right):
    merge_lst = []
    if left: left.reverse()
    if right: right.reverse()
    while left and right:
        merge_lst.append((left.pop() if left[-1] <= right[-1] else right.pop()))

    if left: left.reverse()
    if right: right.reverse()
    merge_lst.extend(left if left else right)
    return merge_lst


int_lst = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(merge_sort(int_lst))

int_lst2 = [6, 8, 1, 4, 10, 7, 8, 9, 3, 2, 5]
print(merge_sort(int_lst2))

best_case = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
print(merge_sort(best_case))

worst_case = [10, 9, 8, 8, 7, 6, 5, 4, 3, 2, 1]
print(merge_sort(worst_case))
