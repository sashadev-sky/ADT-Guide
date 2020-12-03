# parallel assignment, ‘while [unsorted] true’ loop

def bubble_sort(lst):
    unsorted = True
    while unsorted:
        unsorted = False
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                unsorted = True
                lst[i], lst[i + 1] = lst[i + 1], lst[i]


int_lst = [6, 8, 1, 4, 10, 7, 8, 9, 3, 2, 5]
bubble_sort(int_lst)
print(int_lst)  # [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
