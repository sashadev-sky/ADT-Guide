# Sorting

- stable sort algo - IBM (Insertion, Bubble, Merge)
- n logn algorithms are the fastest way to sort

Algorithm      | Avg Case   | Worst Case | Best Case  | Space Complexity | Stability | Internal/External | Iterative/Recursive | Method | Comments
---------      | ---------  | ---------- | -------    | --------         | ----      | ---               | ---                 | ---    | ----
Bubble Sort    | O(n^2)     | O(n^2)     | O(n)       |   O(1)           |  Stable   |  Internal         | Iterative           | Exchanging | `O(n^2)` bc we iterate through `n` items `n-1` times. `O(n)` when the list is already sorted. `O(1)` bc in-place
Selection Sort | O(n^2)     | O(n^2)     | O(n^2)     |   O(1)           |  Unstable |  Internal         | Iterative           | Selection | `O(n^2)` best case bc this one has to continue iterating even if the list is already sorted. But avg. case faster than bubble sort bc iterates over a list with 1 less element every time
Insertion Sort | O(n^2)     | O(n^2)     | O(n)       |   O(1)           |  Stable   |  Internal         | Iterative           | Insertion | Iterates 2x. Nearly sorted lists are closer to `O(n)`. Also beneficial for "small enough" lists
Merge Sort     | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) |   O(n)           |  Stable   |  External         | Recursive           | Merging | Out of place because requires a temporary list structure in order to sort and append elements. `O(n)` is the memory needed for the temporary buffer list. `log(n)` steps to break down a list of size `n` (We already computed in a **binary search** that we can divide a list in half `log(𝑛)` times where `n` is the length of the list) then `O(n)` complexity at each level for the number of elements at that level. Together that is `O(nlog(n))` 
Quick Sort     | O(nlog(n)) | O(n^2)     | O(nlog(n)) |   O(log(n))      |  Unstable |  Internal         | Recursive           | Partitioning | `O(log(n))` space complexity since quicksort calls itself on the order of `log(n)` times (in the average case, worst case number of calls is `O(n)`), at each recursive call a new stack frame of constant size must be allocated.
Heap Sort      | O(nlog(n)) | O(nlog(n)) | O(n)       |   O(1)           |  Unstable |                   |                     | Selection |
Tim Sort       |            | O(nlog(n)) | O(n)       |                  |  Stable   |                   |                     |        |
Radix Sort     |            |            |            |                  |           |                   |                     |        |
Tree Sort      |            |            |            |                  |  Unstable |                   |                     |        |
Shell Sort      |            |            |            |                 |           |                   |                     |        |

## Bubble Sort

- The largest numbers bubble to the back
- In general, given a collection of `n` unsorted elements, it takes `(n-1)` iterations 
through the list in order to sort it
- `n(n-1)` comparisons
- After `x` iterations, checking the last `x` elements in a collection is redundant.

1. Go down the list, and compare if the element in the list is bigger than the next element in the list
2. If it's not, move on
3. If it is, swap them
    - By the time you reach the end of the list, the highest number in the list will be there
4. Keep doing this until you have a sorted list
    - Completely sorted when no swaps have taken place

- [Bubble Sort](./sorting/bubble_sort.py)

## Selection Sort

- Selecting the smallest number one at a time, and moving it to its correct, “sorted” location at the front. 
- In general, given a collection of `n` unsorted elements, it takes `(n^2 / 2) + (n / 2)` comparisons
  in order to sort it.

1. Compare first number in the outer loop to every number in inner loop
2. If the outer element is bigger, swap them
3. If not, move on
4. Keep doing this, each time increase the index of the outer loop number being compared to the inner loop #s.
5. You know you're done when the outer loop number is the last number in the list

- [Selection Sort](./sorting/selection_sort.py)

## Insertion Sort

- Uses temporary variable references to elements at a certain index in the list
- Use insertion sort for when list is almost sorted or when you have to sort smaller lists
- The best case running time of running an insertion sort algorithm on a nearly-sorted list ends up being linear — 
  or, `O(n)` — since far fewer comparisons need to be made by the inner loop.
  If `I` is the number of inversions in an input array of `n` records, then Insertion Sort will run in what time? `O((n-1)+I)`
- One note about shifting versus exchanging is also important. In general, a shift operation requires approximately a third of the processing work of an exchange since only one assignment is performed. In benchmark studies, insertion sort will show very good performance.

1. Key points to index 1, not 0
2. Compare the item at your key with the item before your key
3. If your key is less, swap
4. Compare the swapped number to every number to its left and swap if it's less
4. Increment the key

- In numpy, array sizes smaller than 20 will run insertion sort instead of merge sort.

- [Insertion Sort](./sorting/insertion_sort.py)

## Merge Sort

- Based on the **divide and conquer** technique.
- Divides the list into equal halves until the pieces cannot be divided anymore, 
  and then combines them in a sorted manner.
- At each level, `n` operations for `n` elements (`O(n)` complexity). Then multiplied by the number of steps (ie. levels)
  it would take to break down our entire list, which is calculated by `log(n)` where `n` is now the total # of elements
  in the list.
- If we multiply the log of `n` by the value of `n`, the result ends up being the number of total append operations to perform.
- Good for large datasets - because merge sort is often implemented as an external sorting algorithm, it can do the work of 
  sorting outside of main memory, and then later can pull the sorted data back into the internal, main memory.

1. If it is only one element in the list it is already sorted, return
2. Divide the list recursively into two halves until it no longer divides
    - (base case = single element = `[el]`)
3. Merge the smaller lists into new list in sorted order
    - compare the 1st (smallest) element in the 1st list to the 1st (smallest) element in the 2nd list
      to figure out which one is smaller
    - append the bigger one onto the smaller one
4. At the end, when you only have 2 sorted lists left, you will iterate through them and move the smallest number
   to a new finally sorted list.
   - So compare index 0 of left to index 0 of right
   - Whichever element is smaller, move it to the new sorted list and move the marker on the unsorted list up an index.
   - Compare this index with index 0 of the other unsorted list
   - You know you're done when you run through one of the lists - at that point, append the remainder of the other list to 
     the new sorted list
     
<blockquote>
Merge sort is not as fast as the quicksort algorithm that we will see next because it does extra copying into the temporary array. 
We can avoid some of the copying by exchanging the roles of a and tmp on alternate recursive calls. This speeds up the algorithm at 
the cost of more complex code. It is actually possible to do an in-place merge in linear time, but in-place merging is tricky and 
is slower in practice than using a separate array.
</blockquote>

## Quicksort
- The quick sort uses divide and conquer to gain the same advantages as the merge sort, while not using additional storage. 
- As a trade-off, however, it is possible that the list may not be divided in half. When this happens, we will see that performance is diminished.
- Ruby's .sort uses quicksort
- Naturally recursive
- For a list of length `n`, if the partition always occurs in the middle of the list, there will again be `log𝑛` divisions.
- Unfortunately, in the worst case, the split points may not be in the middle and can be very skewed to the left or the right, 
  leaving a very uneven division. In this case, sorting a list of n items divides into sorting a list of 0 items and a list of 𝑛−1 items. 
  Then sorting a list of 𝑛−1 divides into a list of size 0 and a list of size 𝑛−2, and so on. The result is an 𝑂(𝑛2) sort with the 
  overhead recursion requires.

1. Selects a **pivot value** to assist with splitting the list
    - Many ways to choose the pivot value, a popular choice is the 1st or last element.
2. **Partitioning** begins by locating two position markers— let’s call them 
   `leftmark` and `rightmark` — at the beginning and end of the remaining items in the list 
3. The goal is to move items that are smaller than the pivot to the left of the pivot, larger than the pivot to the right of the pivot, while
   also converging on the actual position where the pivot value belongs in the final sorted list, commonly called the 
   **split point**. The **split point**, will be used to divide the list for subsequent calls to the quick sort.
4. We first compare the `leftmark` to the pivot value. If it is less than the value, continue (increment the `leftmark` up an index
   to the next value). If it is greater than the value, stop there and now perform a similar comparison with the `rightmark`.
5. If the `rightmark` is less than the pivot value, we do the opposite on this side and stop. Otherwise, we continue iterating over
   the list backwards to move the `rightmark`.
6. Once we are stopped for both the `leftmark` and `rightmark`, **exchange** the values there.
7. Then go back to step 4 and repeat until they cross (`rightmark` becomes less than `leftmark`)
8. Once they cross, you have found the split point - it is the value `leftmark` crossed over and now the position of `rightmark`
9. Exchange the pivot value and split point. The pivot value is now in place.
   -  In addition, all the items to the left of the split point are less than the pivot value, and all the items to the right of 
      the split point are greater than the pivot value.
10. The list can now be divided at the split point, and the quick sort can be invoked recursively on the two halves.
   
   


## Tim Sort

use insertion sort for smaller arrays, and merge sort for larger ones. 

The threshold for choosing between Insertion sort and Mergesort is 13, as determined by a bit of quick tests.

Utilizes multiple types of sorting algorithms and using heuristics to guess which algorithm 
will perform the best, given the data (more specifically, it hybridizes `insertion` and `merge sort` 
algorithms).

