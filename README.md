# Abstract Data Types (ADTs)

> Abstract data types (ADTs) refer to classes of objects whose operations and properties are formally defined, but are not restricted to specific implementations.

This is a repository of ADTs written in Ruby and, more recently, Python
(CPython). It is an exercise in implementing abstract data structures in my
own code and a guide for practical application in the future.

It is not intended to cover all the API variations and implementations for a particular abstract data structure.

I define the following ADTs, including their specifications, common operations in their API, and possible implementations with comparisons. I also link my code at the bottom of each section.

Note that many of the ADTs have their own nomenclature, so the same methods may have various names across the data types.

- [Set](#set)
- [Map](#map)
- [Linked List](#linked-list)
- [Stack](#stack)
- [Queue](#queue)
- [Tree](#tree)
- [Graph](#graph)

## Set

> A Set is an unordered collection of unique elements.

### Specifications

- Unordered (no promises regarding insertion order)
- Unique collection of elements (no duplicates)
- Mutability
  - Mutable:
    - Python: built-in type `set` derives from `MutableSet` (subclass of `Set`)
  - Immutable (read-only):
    - Python: built-in type `frozenset` derives from `Set` and `Hashable`

### API

- `insert(el)`: inserts a new element
- `include?(el)`: queries for an element
- `delete(el)`: removes an element

### Implementations

1\) **Array-Based Set**

- Contiguously stored data
- Don't allow it to be indexed into
- Elements aren't required to be hashable
- Goal is a smaller data structure

- **Time Complexity**

Method    | Avg. Case |Worst Case | Best Case  | Notes
 ---      | --- |    ---        | ---        | ---
 `include?` |  O(n) | O(n)       |  O(1)      | Worst: searching for the last element. Best: searching for the first element |
 `insert`  |  O(n)  | O(n)       |  O(1)      | Check for inclusion before inserting. Because sets have no notion of order, you never select a specific index to insert. Best case is empty set |
 `delete`  |  O(n)   | O(n)       |   O(1)    | Need to scan through elements to find the one to delete |

- **Space Complexity**: O(n)

- **Analysis**
  - Could do better. The array's fastest operation is indexing and that is not used.
  - Modifications:
    - a\) Restrict data type to only integers that live in a predefined range (the array is fixed size). Their value will correspond to an index in the array and the value at that index will correspond to its presence (either true or false)
      - e.g., the set { 0, 2, 3 } will be stored as [true, false, true, true]
      - Keeping the size of the array fixed allows us to maintain a contiguous place in memory.
      - Improved time complexity O(1), abysmal space complexity O(range)
    - b\) Building on point a: augment to store sub-arrays (buckets) instead of T/F for the values. When we insert an integer into the set, use the modulo operator to deterministically assign every integer to a bucket: `index = integer_val % num_buckets`
      - Augmented to keep track of an arbitrary range of integers, including negative integers
      - Array is still fixed size
      - Fine for smaller sample sizes, but as our sample size increases will rely more and more on an array scan - O(n) time complexity - which were trying to avoid
      - Improved space complexity O(n)
    - c\) Building on point b: resize the array by a constant multiple that scales with the number of buckets. The goal is to have `buckets.length > N` at all times
      - The array is no longer a fixed size.
      - Improved time complexity O(1) amortized, space complexity stays at O(n)

2\) **Hash Set**

- A Hash Set uses a hash function to compute an index into an array of buckets (sub-arrays)
- This implementation will be a simple improvement to "modification c" from the array-based set implementations above:
  - Modulo the hash of every item (returns an integer) by the # of buckets instead of the original integer value.
- With this simple construction, the set will be able to handle keys of any data type that can be hashed.
  - e.g., { 2, 4, 8, 16, “hello”, “dolly” }

> Note: in Ruby and Python, Sets are implemented as a hash table
>
- **Time Complexity**

Method    | Amortized   | Worst case  | Notes
---       | ---         |  ---        | ---
`include?`| O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`insert`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`delete`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision

- Ruby handles a `hash collision` with `separate chaining`.
- Python handles a `hash collision` with open addressing.

- The maximum `density` (# of items chained at a location in memory) Ruby allows before `rehashing` is 5, which is O(n) time complexity.

- **Space Complexity**: `O(n)`

- **Analysis**:
  - A Hash Set is the fastest implementation of a Set: the hash uses a hashing function to store elements in memory and to later access where they are stored.
    - This creates the highest chance of uniform distribution because there is no pattern to the output, although there is still the chance of a hash collision.
    - We want to use a Hash Set over an array-based set most of the time.
    - Useful if you want to ensure absolutely no duplicates - Hash Maps can have duplicate values (but not keys).
  - **Although it isn’t particularly compact (requires pre-allocation of memory), it provides near constant time insertion and removal in the average case.**

### Usefulness

- Sets are most commonly used for:
    1. Membership testing
    2. Eliminating duplicate entries (cleanup)
- **Not ideal for runtime operations**: unfortunately, the edge cases of Hash Set (and Hash Table - up next) performance are significant, the cases are inevitable, and the methods for dealing with them require some runtime tuning.
  - They are comprised of pre-allocated buckets of fixed size, and due to speed requirements of typical non-cryptographic hash functions, collisions are inevitable.
  - <details><summary><strong>There are a number of different ways of handling collisions</strong></summary>
      <ol>
        <li><strong>Chaining</strong>: In this case, collisions are resolved by using a second data structure (such as a <strong>linked list</strong>) to compare elements when a collision is found.
          <ul>
            <li>This method “degrades gracefully,” but requires a good idea of the bucket size to do so.</li>
          </ul>
          </li>
          <li><strong>Open addressing</strong>: Entries are all stored within the hash buckets, and when a collision is found, some probing algorithm is used to find the next free bucket. When free slots run low, the buckets are resized.</li>
          <li><strong>Cuckoo hashing</strong>: Multiple hash functions are used to insert into different places in the bucket. If all hash functions collide, the bucket is resized.
            <ul>
              <li>Might give us better general performance than linear probing on a busy / full table</li>
          </ul>
          </li>
          <li>Several other methods also exist.</li>
        </ol>
    </details>
  - When the buckets require resizing, every element stored in the bucket
   must be re-hashed to find its new place. With millions of keys, this resize operation becomes prohibitively expensive. **(We basically have to double the table size when we run out of space)**.
  - **The fundamental problem with these methods is that they require some level of runtime tuning.**
    - For ex., for the [Fastly CDN](https://www.fastly.com/blog/surrogatekeys-part-2), the time required to complete this operation could cause it to pause for a significant time period — significant enough to cause it to appear to “miss” purge requests for surrogate keys.
  - An example of a contiguous memory 2D array structure: an image - its really just a 2-D array of pixels.

**Ruby**

- [Set - array implementations](./ruby/array_set.rb)

- [Set - hash implementation](./ruby/hash_set.rb)

**Python**

- [Set implementation](./python/data_structures/dynamic_array_set.py)

-------------------------------------------------

## Map

> At its essence, a **Map** is just an unordered set of key-value pairs.

### Terminology

- Also called a `Dictionary`, `Associative Array` and `Hash Table`.

### Specifications

- Unordered (no promises regarding insertion order)
- Duplicate values are allowed, but not duplicate keys

### API

- `get(k)`: queries for a key-value pair and returns the value
- `set(k, v)`: creates a new key-value pair or updates the value for a pre-existing key
- `delete(k)`: deletes a key-value pair

### Implementations

1\) **Hash Map** :

> **Hash Map vs. Hash Set**
>
> Hash Map implements the Map interface and Hash Set implements the Set interface. The main difference is that the Hash Map allows for duplicate values (but not keys) and the Hash Set does not.

- For the Hash Map implementation, the internals will basically be the same, but we will use a Doubly Linked List for our buckets instead of sub-arrays so that we can use link objects that store both a key and a value in one node together.
  - We could also just use touples, but the Linked List is the classic, canonical way to implement a Hash Map.

- **Hash table**  - A hash table is a form of list where elements are accessed by a keyword rather than an index number. At least, this is how the client code will see it.
  Internally, it will use a slightly modified version of our hashing function in order to find the index position in which the element should be inserted.
  This gives us fast lookups, since we are using an index number which corresponds to the hash value of the key.

- **Time Complexity**

Method    | Amortized   | Worst Case  | Notes
---       | ---         |  ---        | ---
`get`     | O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`set`     | O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`delete`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision

- **Space Complexity**: O(n)

- Note: the time and space complexities are the same as for the Hash Set.

2\) **2D array-based Map**:

- Also called a `touple`.
- The array will contain several subarrays, and each subarray will contain a k,v pair.
- **Time Complexity**

Method    | Avg. Case | Worst Case | Best Case   | Notes
---       | --- | ---         |  ---        | ---
`get`     |   O(n) | O(n)      |  O(1)       |
`set`     |   O(n) | O(n)      |  O(1)       |
`delete`  |  O(n) |  O(n)      |  O(1)       |

- **Space Complexity**: O(n)

- Note: the time and space complexities are the same as for the array-based set.

### Usefulness

- Useful when you want to store values associated with keys.
- Dictionaries provide constant time (amortized) performance for assignments and accesses, which means they are ideal
   for bookkeeping dynamic information.

**Ruby**

- [Map - hash map implementation](./ruby/hash_map.rb)

- [Map - 2D array-based implementation](./ruby/array_map.rb)

**Python**

- [Map - 2D array-based implementation](./python/data_structures/map/dynamic_array_map.py)

-------------------------------------------------

## Linked List

> A **Linked List** is a linear collection of data elements of any type, called nodes, where each node itself has a value, and points to the next node in the list.

**Linked List vs Array**:
> While arrays have contiguously stored data, Linked Lists spread out their data across many cells across the computer's memory.
> These cells are **nodes**. In addition to the data stored within the node, each node also stores the memory address
> of the next node in the Linked List. These pointers are a **link**.
>
> - **Insertion**: Unlike arrays, the insertion of new elements at the beginning of the list is very cheap (`O(1)`), since it only requires us to change one reference or pointer
> - **No random access** and no access to **len** (number of elements in list)
> - **Searching**: for an element is the same as an array (`O(n)`)

### Terminology

- `Head`: first node
- `Tail`: last node
  - Points to `nil` / `None`

### Specifications

- Each node has a value
- Each node has a pointer to the next node in the list
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted
- No indexing (meaning no random access)

### API

- `include?(key)`: returns boolean indicating whether the node is in the List
- `append(key, value)`: appends a node
- `prepend(key, value)`: prepends a node
- `remove(key)`: removes a node
- `empty?`: returns boolean indicating whether the List is empty
- `[](index)`: returns the node at a specified index or nil if the node is not in the List
- `get(key)`: returns the value of the node at a specified index or nil if the node is not in the List
- `update(key, value)`: updates the value for a node and returns that node or nil if the node is not in the List
- `first`: returns the first node
- `last`: returns the last node

### Sub-Types

#### 1) **Singly-Linked List**

#### 2) **Doubly-Linked List**

- Singly-Linked List with augmentations: add a `previous` attribute for the nodes and keep track of the `tail`

### Implementation

- This implementation applies to both Linked List types mentioned above.
- Implemented using a `Node` class.
  - A Linked List is a `node-based data structure`.
    - Trees also fall into this category.
- The time and space complexities below refer to this implementation.
- Note that the time and space complexities for the Singly-Linked List and Doubly-Linked List will be the same asymptotically, so the following complexities are for both types.
- **Time Complexity**

Method | Avg. Case | Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`include?` | `O(n)` |   `O(n)` |   `O(1)`  |
`append` |   `O(1)` |   `O(1)` |   `O(1)`  | Assuming access to tail
`prepend` | `O(1)`  |   `O(1)` |   `O(1)`  | Assuming access to head
`remove` |  `O(n)`  |   `O(n)` |   `O(1)`  | Deletion is more efficient in a Doubly-Linked List than Singly because we have a previous pointer, so we can easily access the node before the node being deleted to change its next pointer
`empty?` | `O(1)`   |   `O(1)` |   `O(1)`  | Only have to check if the head's next pointer is the tail
`[]`     |  `O(n)`  |   `O(n)` |   `O(1)`  |
`get`    |  `O(n)`  |   `O(n)` |   `O(1)`  |
`update` |  `O(n)`  |   `O(n)` |   `O(1)`  |
`first`  |  `O(1)`  |   `O(1)` |   `O(1)`  |
`last`   |  `O(1)`  |   `O(1)` |   `O(1)`  | Assuming access to tail

- Note: insertion / deletion anywhere other than the beginning or end would only be `O(n)` (assuming you don't have a pointer / reference to the node) because it has to search the LinkedList for that node. But, that's not what we often use the Linked List for. The LinkedList is best for adding and removing elements sequentially.
  - **So insertion and deletion are summarized as `O(1)` assuming the LinkedList is used in its optimal way (e.g., LRU cache)**

- **Space Complexity**: `O(n)`
  - Space complexity for a Doubly-Linked List is more than a Singly-Linked List because were storing an extra link to a node, but it doesn't change it asymptotically (still linear).

### Usage

- The advantage of the Linked List is that the values are stable: they don't correspond to indices, so you never need to re-index.
  - If you are building an `LRU Cache` the Linked List is essential as an auxiliary structure for its quick insertion and deletion time `O(1)`. You never need to index because always delete from the beginning or end. The Hash Map on its own would be slower: `O(n)` because it would have to iterate to find the key with the most recent timestamp value since it is unordered. With an array as the auxiliary structure these operations would still take `O(n)` time because you would be stuck re-indexing.
  - Also, unlike lists, Linked Lists don't preallocate memory
- Useful in general if you are deleting many items: it will be faster than with an array, but doesn't make a difference in the time complexity asymptotically.

#### 3) **Circularly-Linked List**

- **Circular**
  - **Cycle**: when a node points back to a previous node. Begins at the last node of the linked list

**Ruby**

- [Doubly-Linked List - Node class implementation](./ruby/linked_list.rb)

**Python**

- [Singly, Doubly, and Circular - Node implementation](./python/data_structures/linked_list.py)

-------------------------------------------------

## Stack

> A **Stack** stores data in the same way that arrays do - it is simply a list of elements - but stacks have added on constraints.

### Specifications

- LIFO
  - Data can only be inserted at the end of a stack
  - Data can only be removed from the end of a stack
  - Data can only be read from the end of a stack
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted
- Addition and removal of a single item is an `O(1)` algorithm

### API

- `push(el)`: adds an element to the top of the Stack
- `pop`: removes the top element in the Stack and returns it
- `peek`: returns the top element in the Stack
- `empty`: check whether the stack is empty

### Implementations

1\) **Array**

- **Time Complexity**

Method  |  Worst Case | Notes
---     |  ---        | ---
`push`  | `O(1)`      | `Array#push` is `O(1)` time
`pop`   | `O(1)`      | `Array#pop` is `O(1)` time
`peek`  | `O(1)`      | `Array#last` is `O(1)` time
`empty` | `O(1)`      |

- **Space Complexity**: `O(n)`

2\) **Linked List**

- A Stack can be implemented as a Doubly Linked List by just enforcing constraints on it that only allow insertion, removal, and peeking at the tail.
- Initialize and track a `self.size` variable so that `empty()` remains `O(1)`

- **Analysis**:
  - Implementing a Stack with an array or Linked List will have the same space and time complexities asymptotically.

### Usage

- Recursion (stack frame)
- The 'back' button of our web browser
- Syntax checking; matching opening and closing parentheses (e.g., in regex, math equations, etc.) to be specific.
- Ideal as a temporary container for temporary data

-------------------------------------------------

### Monotonic Stack

> A monotonic stack is a stack whose elements are monotonically increasing or decreasing. It contains all qualities that a typical stack has.

-------------------------------------------------

**Ruby**

- [Stack - array implementation](./ruby/array_stack.rb)

**Python**

- [Stack - array and linked list implementation](./python/data_structures/stack.py)

-------------------------------------------------

## Queue

> Like a Stack, a **Queue** handles temporary data elegantly and is also essentially an array with restrictions.
>
> - Stacks and Queues can be effectively implemented by dynamic arrays or linked lists. However, unlike for stacks,
>   a simple underlying array won't cut it. The implementation would involve using 2 arrays implemented as stacks
>   (`inbound_stack` and `outbound_stack`)
> - Queues are harder to implement and appropriate when order is important.

### Specifications

- FIFO
  - Data can only be inserted at the end of a Queue (same as Stack)
  - Data can only be read from the front of a Queue (opposite behavior of Stack)
  - Data can only be removed from the front of a Queue (opposite behavior of Stack)
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted
- Unlike a stack, tracking the tail in a queue is not optional

### API

- `enqueue(el)`: adds an element to the back of the Queue
- `dequeue`: removes the element at the front of the Queue and returns it
- `peek`: returns the element at the front of the Queue

### Implementations

1\) **Array**

- Naive implementation
- Note that it is your choice which ends of the array will be the "front" and "back".
  - This will change which array methods you use in your implementation.
- **Time complexity**

Method | Worst Case | Best case | Notes
---    | ---        | ---       |  ---
`enqueue` | `O(1)`    |   `O(1)`    |  `Array#push` has `O(1)` runtime
`dequeue`|  `O(n)`    |   `O(n)`    | `Array#shift` has `O(n)` runtime

- **Analysis**
  - Could do better: is there a way to implement a Queue using an array in constant time?
    - Yes, implement it using 2 stacks. (Amortized constant time)
    - See `NaiveArrayQueue` vs `BetterArrayQueue` linked at the end of this section.
  - Could still do better with Doubly-Linked List.

2\) **Doubly Linked List**

- A Queue can be implemented as a Doubly-Linked List by just enforcing constraints on it that only allow you to add to the back, delete from the front and peek at the first element in the front of the Queue.
- This is called a **Dequeue (double-ended queue)**

Method | Worst Case | Best case | Notes
---    | ---        | ---       |  ---
`enqueue` | `O(1)`    |   `O(1)`    |
`dequeue`|  `O(1)`    |   `O(1)`    |

- **Analysis**
  - Doubly-Linked List is the superior implementation - pure constant runtime.

### Usage

- Printing queues
- Handling asynchronous requests - queues ensure that requests are processed in the order in which they are received
- Internally, a list is represented as an array; the largest costs come from growing beyond the current allocation size (because everything must move), or from inserting or deleting somewhere near the beginning (because everything after that must move). **If you need to add/remove at both ends, consider using a `collections.deque` instead.**
  - A deque (double-ended queue) is represented internally as a doubly linked list. (Well, a list of arrays rather than objects, for greater efficiency.) Both ends are accessible, but even looking at the middle is slow, and adding to or removing from the middle is slower still.

### Dequeue

-------------------------------------------------

> **Deques** (not to be confused with the "dequeue" operation in queues) is a data structure that is closely related to queues. Deque simply stands for "double-ended queue," and as the name implies, it allows us to add and remove items at both sides of a queue.

![](./deque.png)

**API:**

- `add_front`
- `remove_front`
- `add_end`
- `remove_end`
- `show_front`
- `show_end`

> Again, because of the nature of Python lists, the `remove_front` and `add_front` become `O(n)` operations.

-------------------------------------------------

### Priority Queue

-------------------------------------------------

> A priority queue is somewhat similar to a queue, with an important distinction: each item is added to a priority queue with a priority level,
> and will be later removed from the queue with the highest priority element first. That is, the items are (conceptually) stored in the queue
> in priority order instead of in insertion order.

**Specifications**

- Must support at least two operations:
  - Insertion: An element is added to the queue with a priority (a numeric value).
  - Top item removal: Deletes the element or one of the elements with the current top priority and return it.


**Ruby**

- [Queue - array implementation](./ruby/array_queue.rb)

**Python**

- [Queue - Naive array, stack array, and doubly linked list](./python/data_structures/queue_dequeue.py)

-------------------------------------------------

## Tree

> A **Tree** data structure is used to store hierarchical data (it is non-linear). It contains nodes where each node has a parent-child relationship.

### Terminology

- **Root**: top-level node
- **Leaf** (or **Terminal**, **External**) node: a node with no **children**
- **Internal** node: a node with at least 1 child
- **Parent** (or **superior**) node: has a child
  - child only has 1 parent, but possibly many **ancestors**, such as the parent's parent
- **Siblings**: child nodes with the same **parent** (same level doesn't necessarily mean siblings)
- **Neighbor**: parent or child
- **Subtree**: consists of a node and all of its **descendants**
- **Size** of a tree: the number of nodes it has
- **Path**: if `n_1, n_2, ..., n_k` is a sequence of nodes in the tree such that `n_i` is the parent of `n_i + 1` for
            `1 <= i < k` , then this sequence is called a path from `n_1` to `n_k`
  - The length of the path is `k - 1`
  - The length of a path is the number of **edges**
- **Edge** (or **Link**, **Line**): connection between one node to another. (two **vertices**).
  - All nodes can be reached from root by following these
- **Traversal** of a tree refers to visiting or performing an operation, at each node.
- **Searching** a tree refers to traversing all the nodes of a tree where each node is visited only once.

### Properties (Node)

> **Depth** and **height** are properties of a node:
>
> - **The depth of a node** is the number of edges on the path from the root of the tree to the node
>   - 0 indexed - the root is the only node at **level** 0, and its **depth** is 0
>
> - **The height of a node** is the number of edges on the longest path from the node to a leaf
>
>   - 0 indexed - a leaf node will have a height of 0
>   - Conventionally, an empty tree (tree with no nodes, if such are allowed) has height −1
>
> **Degree** of a node is the number of children it has
>
> - A leaf has degree 0.

### Properties (Tree)

> **The height of a tree** is the depth of its deepest node
>
> - Or equivalently, the height of its root node
> - A tree with only a single node (hence both a root and leaf) has depth and height zero.
>
> **Level**: All nodes of **depth** `d` are at **level** `d` in the tree
>
> - 0 indexed - since levels are 0 indexed, the below tree whose last level is 3 has 4 total levels
> - The below tree with 4 total levels also has a height of 3 - a tree's last level is represented by `h`, its height
>
> **The diameter (or width) of a tree** is the number of nodes on the longest path between any two leaf nodes.
>
> - The tree below has a diameter of 6 nodes.
>
> **Degree** or (**order**) of a tree: the maximum degree of a node in the tree
>
> - The degree of a binary tree is 2

![Tree Levels](./python/data_structures/trees/tree_d_h_levels.png)

### Specifications

- Directional (root to leaves) - Any node can have either zero, one, or two children
- Each child node must have a parent and only one parent

### API

- `add_child(node)`: adds a child node to a parent
- `remove_child(node)`: removes a child node from a parent
- `count`: returns the count of nodes starting from the passed in node and including all of its descendants

### Implementation

- When creating a tree object, you can keep all the business logic in a `Node` class.
  - You just create a root node and build on it: once you have the root you have the whole tree.
  - The tree is uni-directional, so you can only build children off of the root.
  - And the tree itself is recursive: the BFS and DFS algorithms apply the same way to the root as they do to any child node.

### Sub-Types

These sub-types are determined by the maximum number of children, not the number of children at any particular node.

The implementation above is generalized to apply to all types of the tree data structure. For specific implementations, augment to include the below restrictions for each type.

-------------------------------------------------

### Binary Tree

-------------------------------------------------

> A tree data structure in which each node has at most two children, which are referred to as the left child and the right child.
>
- One of the most typical tree structure
- Any node can have either zero, one, or two children.
- No notion of order

#### Complexity

-------------------------------------------------

**Time:** Assuming you are calling these methods on the root node,

Method | Avg. Case| Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`add_child` | `O(1)` |    `O(1)`     |   `O(1)`
`remove_child` | `O(n)` | `O(n)`   | `O(n)`
`count` |  `O(n)`    |     `O(n)`   |    `O(1)`  |

**Space**: `O(n)`

#### Attributes

-------------------------------------------------

> **Balanced** (or **height-balanced**): The left and right subtrees of every node differ in height by no more than 1. Otherwise, the binary tree is **unbalanced**.
>
> **Full** (or **Proper**, **Plane**): All nodes except leaf nodes have 2 children.
>
> **Complete**:
>
> - All nodes except for the level before the last must have 2 children.
> - All nodes in the last level are as far left as possible.
>
> **Perfect**: All interior nodes have two children and all leaves have the same depth.
>
> **Left** or **Right** **Skewed** (or **Pathological**): Each node has 1 child node only.

- **Summary**:
  - Complete trees: *must* be balanced; *can* be full
  - Full trees: *can* be balanced; *can* be complete
  - Balanced trees: *can* be complete; *can* be full
  - Perfect trees: *must* be balanced, complete, and full
    - Balanced, complete, and full trees *can* be perfect

*Examples*:

**Full, balanced & complete** - All nodes have 0 or 2 children, `3 - 2 <= 1`, last level nodes are as far left as possible:

```txt
             1             --- LEVEL 0
           /    \
          1      1         --- LEVEL 1
         /\      /\
        1  1    1  1       --- LEVEL 2
       /\  -    -  -
      1  1                 --- LEVEL 3
      -  -
```

**Full & balanced** -  All nodes have 0 or 2 children, `3 - 2 <= 1`, (**Not complete** - last level nodes are not as far left as possible)

```txt
             1            --- LEVEL 0
           /   \
          1     1         --- LEVEL 1
         /\     /\
        1  1   1  1       --- LEVEL 2
        -  /\  -  -
          1  1            --- LEVEL 3
      x x -  -
```

**Full** - All nodes have 0 or 2 children (**Unbalanced** - `3 - 1 > 1`, **Not complete** - level 2 has a node with 0 children):

```txt
            1              --- LEVEL 0
           / \
          1   1            --- LEVEL 1
         / \  -
        1   1              --- LEVEL 2
       / \  - x x
      1   1                --- LEVEL 3
      -   -
```

**Complete & balanced** - Last level nodes are as far left as possible, `3 - 3 <= 1` (**Not full** - there is a level 2 node with 1 child):

```txt
             1             --- LEVEL 0
           /    \
          1      1         --- LEVEL 1
         /\      /\
        1  1    1  1       --- LEVEL 2
       /\  /\  /\  /x
      1 1 1  11 1 1        --- LEVEL 3
      - - -  -- - -
```

**Balanced** - `3 - 3 <= 1`, (**Not full** - there is a level 2 node with 1 child, **Not complete** - last level nodes are not as far left as possible)

```txt
             1             --- LEVEL 0
           /   \
          1     1          --- LEVEL 1
         /\     /\
        1  1   1  1        --- LEVEL 2
       /\ /\  /x  /\
      1 11  11   1  1      --- LEVEL 3
      - --  -- x -  -
```

-------------------------------------------------

1a\) **Binary Search Trees**

> - **search tree**: an ordered tree data structure used to store a **dynamic set** or **associative array** where the keys are usually strings.

- Used for searching
  - The structure of the BST makes looking for the node with the maximum and minimum values very easy.
- An extension of the Binary Tree with the addition of a restriction:
  - The child nodes are stored in a specific order: the left subtree of a node only contains values less than itself and the right subtree only contains values greater than it.
- There are essentially two operations that are needful for having a usable BST. These are the `insert` and `remove` operations.

```puml
graph searchtree {
  size=6;
  2 -- 1;
  2 -- 3;
}
```

```puml
graph searchtree {
  size=6;
  5 -- 2;
  5 -- 7;
  2 -- 1;
  2 -- 3;
  7 -- 6;
  7 -- 9;
  9 -- 8;
  9 -- 13;
}
```

- **Time Complexity**

Method | Avg. Case| Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`add_child` | log(n) | O(n)     |  O(1)    | Refer to this method by the Avg. Case: you can only add from the root so it has to find the correct node to add to either from the left or right. log(n) where n is the height of the tree. Worst Case: the tree is one-sided (most extreme case of **unbalanced** - at this point it's pretty much just a linked list) so you can't take advantage of the logarithmic property of this tree type.
`remove_child` | log(n) | O(n)  |  O(1)    |
`count` |     O(n)       |  O(n) |  O(1)   |

- Note: Time complexities assume you are calling these methods on the root node.

- **Space Complexity**: `O(n)`

Subtype: There is an auto-balancing binary search tree called **AVL tree** where every node also stores the number of children to its left and right and it uses that as a sort of balancing metric. When you insert, you can get it down to the worst case being log(n), and so you can actually get your inserts to maintain a balanced tree in log(n) every time.

2\) **N-ary Tree (Poly Tree)**
- Can have an arbitrary number of children.
- Does not have the additional restriction of the search tree above.
- Note: complexities for the Poly Tree and Binary Tree are the same.

- **Time Complexity**

Method | Avg. Case| Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`add_child` | O(1) |    O(1)   |     O(1)  |
`remove_child` | O(n) | O(n)   | O(n)      |
`count` |  O(n)    |     O(n)   |    O(1)  |

- Note: Time complexities assume you are calling these methods on the root node.

- **Space Complexity**: `O(n)`

3\) [**Trie**](https://en.wikipedia.org/wiki/Trie)

- A kind of **search tree**.
- Also called `digital tree` or `prefix tree`.
- **Unlike a binary search tree**, no node in the tree stores the key associated with that node; instead, its position in the tree defines the key with which it is associated.
  - All the descendants of a node have a common **prefix** of the string associated with that node, and the root is associated with the **empty string**.
  - Keys tend to be associated with leaves, though some inner nodes may correspond to keys of interest. Hence, keys are not necessarily associated with every node.

4\) [**Radix Tree**](https://en.wikipedia.org/wiki/Radix_tree)

- Also called a `radix trie` or `compact prefix tree`.
- Represents a **space-optimized trie** in which each node that is the only child is merged with its parent.

4a) [**Crit-bit Tree**](http://cr.yp.to/critbit.html)

- A condensed **radix trie**, generally yielding better performance due to the reduced number of pointers involved in maintaining nodes of the tree (and they’re significantly more compact than **trie** implementations requiring more pointers).

### Usefulness

- Binary Search Tree: maintains order and has fast search, insertion and deletion.
  - Used on databases to perform quick searches (e.g., indexing in Rails used a sorted tree to make lookup time go from linear to logarithmic)
- The others are useful for storing data:
  - Operating Systems use a tree structure to store files.
  - HTML `DOM` uses a tree data structure to represent the hierarchy of elements.
  - **Expression trees**: The tree structure is also used to parse arithmetic and Boolean expressions.
- **Crit-bit Tree**: used by the [Fastly CDN](https://www.fastly.com/blog/surrogate-keys-part-2) for its surrogate key functionality.``

**Ruby**

- [Tree - Poly Tree implementation](./ruby/poly_tree.rb)

-------------------------------------------------

## Graph

> A graph is a set of vertices and edges that form connections between the vertices.

### Terminology

- **Node** or **vertex**: A point, usually represented by a dot in a graph
- **Edge**: This is a connection between two vertices
- There are two well-known implementations of a graph, the **adjacency matrix** and the **adjacency list**.
- Graphs can be classified based on whether they are **undirected** or **directed**.
  - An undirected graph simply represents edges as lines between the nodes. There is no additional information about the relationship between the nodes than the fact that they are connected
  - In a directed graph, the edges provide orientation in addition to connecting nodes. That is, the edges, which will be drawn as lines with an arrow, will point in which direction the edge connects the two nodes
- **weighted graphs** associate edges with a numerical value indicating some extra information
