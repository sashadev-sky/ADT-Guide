def selection_sort(lst):
    spot = 0
    while spot < len(lst):
        for i in range(spot, len(lst)):
            if lst[i] < lst[spot]:
                lst[spot], lst[i] = lst[i], lst[spot]
        spot += 1


int_lst = [6, 8, 1, 4, 10, 7, 8, 9, 3, 2, 5]
selection_sort(int_lst)
print(int_lst)  # [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
