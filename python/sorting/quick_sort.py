# note this implementation is not in place

def quick_sort(lst):
    if len(lst) < 2: return lst
    pivot_lst = lst[0]
    left_side = [el for el in lst[1:] if el < pivot_lst]
    right_side = [el for el in lst[1:] if el >= pivot_lst]  # this = in >= is the part that makes quicksort unstable, but it allows us to have dup elements
    return quick_sort(left_side) + [pivot_lst] + quick_sort(right_side)


print(quick_sort([]))

print(quick_sort([None]))

int_lst = [26, 26, 93, 17, 77, 31, 44, 55, 20]
print(quick_sort(int_lst))


int_lst_ev = [26, 26, 93, 17, 77, 31, 44, 55, 20, 12]
print(quick_sort(int_lst_ev))

int_lst2 = [6, 8, 1, 4, 10, 7, 8, 9, 3, 2, 5]
print(quick_sort(int_lst2))

best_case = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
print(quick_sort(best_case))

worst_case = [10, 9, 8, 8, 7, 6, 5, 4, 3, 2, 1]
print(quick_sort(worst_case))
