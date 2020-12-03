def insertion_sort(lst):
    for key in range(1, len(lst)):
        if lst[key] < lst[key - 1]:
            j = key
            while j > 0 and lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
                j -= 1


int_lst = [6, 1, 8, 4, 10]
insertion_sort(int_lst)
print(int_lst)  # [1, 4, 6, 8, 10]
