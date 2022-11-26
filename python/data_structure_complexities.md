# Data Structures and Algorithms

## Data Structures

| Data Structure | Access (Avg Case) | Search (Avg Case) | Insertion (Avg Case) | Deletion (Avg Case) | Access (Worst Case) | Search (Worst Case) | Insertion (Worst Case) | Deletion (Worst Case) | Worst Space Complexity |
|---|---|---|---|---|---|---|---|---|---|
| Array | `O(1)` | `O(n)` | `O(n)` | `O(n)` | `O(1)` | `O(n)` | `O(n)` | `O(n)` | `O(n)` |
| Stack | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` |
| Singly-Linked List | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` |
| Doubly-Linked List | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` | `O(n)` | `O(1)` | `O(1)` | `O(n)` |
| Skip List | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` | `O(n)` | `O(n)` | `O(n)` | `O(n log(n))` |
| Hash Table |  -  | `O(1)` | `O(1)` | `O(1)` | - | `O(n)` | `O(n)` | `O(n)` | `O(n)` |
| Binary Search Tree | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` | `O(n)` | `O(n)` | `O(n)` | `O(n)` |
| Cartesian Tree | - | `O(log(n))` | `O(log(n))` | `O(log(n))` | - | `O(n)` | `O(n)` | `O(n)` | `O(n)` | |
| B-Tree | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` |
| Red-Black Tree | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` |
| Splay Tree | - | `O(log(n))` | `O(log(n))` | `O(log(n))` | - | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` |
| AVL Tree | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)` |

### List (Array) vs. Linked List

> Linked lists are good for inserts/deletes, and arrays are good for random access.

list (array):

- reading: `O(1)`
  - random access: are great if you want to read random elements, because you can look up any
      element in your array instantly. With a linked list, the elements aren’t next to each
      other, so you can’t instantly calculate the position of the fifth element in memory—you
      have to go to the first element to get the address to the second element, then go to the second
      element to get the address of the third element, and so on until you get to the fifth element.
- insertion: `O(n)`
- deletion: `O(n)`
