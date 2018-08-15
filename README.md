# Abstract Data Types (ADTs)

> Abstract data types (ADTs) refer to classes of objects whose operations and properties are formally defined, but are not restricted to specific implementations.

This is a repository of ADTs, written in Ruby. It is an exercise in implementing abstract data structures in my own code and a guide for practical application in the future.

It is not intended to cover all of the API variations and implementations for a particular abstract data structure.

I define the following ADTs, including their specifications, common operations in their API, and possible implementations with comparisons. I also link my code at the bottom of each section.

Note that many of the ADTs have their own nomenclature, so the same methods may have various names across the data types.


- [Set](#set)
- [Map](#map)
- [List](#list)
- [Stack](#stack)
- [Queue](#queue)
- [Tree](#tree)

## Set
> A Set is an unordered collection of elements with no duplicates.

### Specifications
- Unordered (no promises regarding insertion order)
- Unique list of elements (no duplicates)

### API
- `insert(el)`: inserts a new element
- `include?(el)`: queries for an element
- `delete(el)`: removes an element
- `union(s2)`: returns a new set combining the elements from two provided sets
- `intersection(s2)`: returns a new set containing elements that are in both provided sets
- `difference(s2)`: returns a new set containing elements that are from the current set that don't exist in the provided set

### Implementations

1\) **Array Set**
- Use an array as storage
- Don't allow it to be indexed into
- **Time Complexity**

Method    | Avg. Case |Worst Case | Best Case  | Notes
 ---      | --- |    ---        | ---        | ---
`include?`|  O(n) | O(n)       |  O(1)      | Worst: searching for the last element. Best: searching for the first element
`insert`  |  O(n)  | O(n)       |  O(1)      | Check for inclusion before inserting. Because sets have no notion of order, you never select a specific index to insert. Best case is empty set
`delete`  |  O(n)   | O(n)       |   O(1)    | Need to scan through elements to find the one to delete

- **Space Complexity**: O(n)

- **Analysis**
  - Could do better. The array's fastest operation is indexing and that is not used.
    - Modifications:
      - a\) Restrict data type to only integers that live in a predefined range. Their value will correspond to an index in the array and the value at that index will correspond to its presence (either true or false) -> Improved time complexity O(1), abysmal space complexity O(range).
         - e.g., the set { 0, 2, 3 } will be stored as [true, false, true, true]
      - b\) Building on point a: augment to store sub-arrays (buckets) instead of indices for the values. Resize the array by a constant multiple that scales with the number of buckets -> Improved space complexity O(n).

2\) **Hash Set**
- Use a hash as storage
> Note: this is exactly how Sets are implemented in Ruby through the built-in Set library. They use a hash set under the hood.
- **Time Complexity**

Method    | Amortized   | Worst case  | Notes
---       | ---         |  ---        | ---
`include?`| O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`insert`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`delete`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision

  - Ruby handles a `hash collision` with `separate chaining`.
  - The maximum `density` (# of items chained at a location in memory) Ruby allows before `rehashing` is 5, which is O(n) time complexity.

- **Space Complexity**: O(n)

- **Analysis**:
  - A Hash Set is the fastest implementation of a Set: the hash uses a hashing function to store elements in memory and to later access where they are stored.
    - We want to use a Hash Set over an array-based set most of the time because hashes don't need to examine every element for inclusion.

### Usefulness
- The Hash Set is useful if you want to ensure absolutely no duplicates - Hash Maps can have duplicate values (but not keys).


[Set - hash implementation](./lib/hash_set.rb)

-------------------------------------------------

## Map
> At its essence, a **Map** is just an unordered set of key-value pairs.

### Terminology
- Also called a `Dictionary`, `Associative Array` and `Hash Table`.

### Specifications
- Unordered (no promises regarding insertion order)
- Duplicate values are allowed, but not duplicate keys

### API
- `get(k)`: queries for a key-value pair
- `set(k, v)`: creates a new key-value pair or updates the value for a pre-existing key
- `delete(k)`: deletes a key-value pair

### Implementations

1\) **Hash Map** :
- Hash Map vs. Hash Set
> Hash Map implements the Map interface and Hash Set implements the Set interface. In the implementation, we will now store values for keys not just true or false. The main difference is that the Hash Map allows for duplicate values (but not keys) and the Hash Set does not.
- **Time Complexity**

Method    | Amortized   | Worst Case  | Notes
---       | ---         |  ---        | ---
`get`     | O(1)        |   O(n)      | Worst case is in rare case of a hash collision
`set`     | O(1)        |   O(n)      | Worst case is in rare case of a hash collision    
`delete`  | O(1)        |   O(n)      | Worst case is in rare case of a hash collision

- **Space Complexity**: O(n)

- Note: the time and space complexities are the same as for the Hash Set.

2\) **2D Array**:
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

- **Analysis**
  - 2D array is a less common implementation than a Hash Map because its slower with insertion, deletion, and retrieval.

### Usefulness
 - Useful when you want to store values associated with keys.

[Map - 2D array implementation](./lib/array_map.rb)

-------------------------------------------------

## List
> A **Linked List** (also just referred to as a **List**) is linear collection of data elements of any type, called nodes, where each node itself has a value, and points to the next node in the list.

**Linked List vs Array**:
> While arrays have contiguously stored data, Linked Lists spread out their data across many different cells across the computer's memory. These cells are known as **nodes**. In addition to the data stored within the node, each node also stores the memory address of the next node in the Linked List. These pointers are known as a **link**.  

### Terminology
- `head`: first node
- `tail`: last node
  - Always points to nil

### Specifications
- Each node has a value
- Each node has a pointer to the next node in the list
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted

### API
- `include?(el)`: returns boolean indicating whether the element is in the List
- `append(el)`: appends an element
- `prepend(el)`: prepends an element
- `delete(el)`: removes an element
- `empty?`: returns boolean indicating whether the List is empty
- `[](index)`: returns the element at a specified index or nil if the element is not in the List
- `first`: returns the first element
- `last`: returns the last element

### Sub-Types

1\) **Singly-Linked List**

2\) **Doubly-Linked List**
  - Singly-Linked List with augmentations: add a previous attribute for the nodes.

### Implementation
- This implementation applies to both Linked List types mentioned above.
- Implemented using a `Node` class.
  - A Linked List is often referred to as a `node-based data structure`.
    - Trees also fall into this category.
- The time and space complexities below refer to this implementation.
- Note that the time and space complexities for the Singly-Linked List and Doubly-Linked List will be the same asymptotically, so the following complexities are for both types.
- **Time Complexity**

Method | Avg. Case | Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`include?` | O(n) |   O(n)     |   O(1)    |
`append` |   O(1)   |    O(1)    |   O(1)    | Assuming access to tail
`prepend` | O(1)  |     O(1)   |     O(1)  | Assuming access to head
`delete` |  O(n)  |     O(n)   |     O(1)  | Deletion is more efficient in a Doubly-Linked List because we have a previous pointer, so we can easily access the node before the node being deleted to change its next pointer
`empty?` | O(1)  |   O(1)      |   O(1)     | Only have to check if the head's next pointer is the tail
`[]`     |  O(n) |    O(n)     |      O(1)  |
`first`  |  O(1) |    O(1)     |    O(1)    |
`last`  |  O(1) |    O(1)     |    O(1)     |


- Note: insertion anywhere other than the beginning or end of the List would be O(n).

- **Space Complexity**: O(n)
  - Space complexity for a Doubly-Linked List is more than a Singly-Linked List because were storing an extra link to a node, but it doesn't change it asymptotically (still linear).

### Usage
- The advantage of the Linked List is that the values are stable: they don't correspond to indices so you never need to re-index.
  - If you are building an `LRU Cache` you're prepending to the List so you can do this in constant time O(1) with the Linked List but with an array it would take linear time O(n).
- Also useful in general if you are deleting many items: it will be faster than with an array, but doesn't make a difference in the time complexity asymptotically.

[Doubly-Linked List - Node class implementation](./lib/linked_list.rb)

-------------------------------------

## Stack
> A **Stack** stores data in the same way that arrays do - its simply a list of elements - but Stacks have added on constraints.

### Specifications
- LIFO
  - Data can only be inserted at the end of a stack
  - Data can only be removed from the end of a stack
  - Data can only be read from the end of a stack
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted

### API
- `push(el)`: adds an element to the top of the Stack
- `pop`: removes the top element in the Stack and returns it
- `peek`: returns the top element in the Stack

### Implementations:

1\) **Array**
- **Time Complexity**

Method  |  Worst Case | Notes
---     |  ---        | ---
`push` | O(1)          | `Array#push` is O(1) time
`pop`  | O(1)           | `Array#pop` is O(1) time
`peek` | O(1)         | `Array#last` is O(1) time

- **Space Complexity**: O(n)

2\) **Linked List**
- A Stack can be implemented as a Doubly Linked List by just enforcing constraints on it that only allow insertion, removal, and peeking at the tail.

- **Analysis**:
  - Implementing a Stack with an array or Linked List will have the same space and time complexities asymptotically.

### Usage:
- Used in recursion to keep track of the stack frame.
- Used to write iterative quicksort.
- Ideal as a temporary container for temporary data.

[Stack - array implementation](./lib/array_stack.rb)

-------------------------------------

## Queue
> Like a Stack, a **Queue** handles temporary data elegantly and is also essentially an array with restrictions.

### Specifications:
- FIFO
  - Data can only be inserted at the end of a Queue (same as Stack)
  - Data can only be read from the front of a Queue (opposite behavior of Stack)
  - Data can only be removed from the front of a Queue (opposite behavior of Stack)
- Sequential/Ordered (i.e. consistent element ordering based on collection population)
- Duplicates permitted


### API
- `enqueue(el)`: adds an element to the back of the Queue
- `dequeue`: removes the element at the front of the Queue and returns it
- `peek`: returns the element at the front of the Queue

### Implementations

1\) **Array**
- Note that it is your choice which ends of the array will be the "front" and "back".
  - This will change which array methods you use in your implementation.
- **Time complexity**

Method | Worst Case | Best case | Notes
---    | ---        | ---       |  ---
`enqueue` | O(1)    |   O(1)    |  `Array#push` has O(1) runtime
`dequeue`|  O(n)    |   O(n)    | `Array#shift` has O(n) runtime

- **Analysis**
  - Could do better: is there a way to implement a Queue using an array in constant time?
    - Yes, only use the `Array#push` and `Array#pop` operations for the Queue. But, this is amortized constant time.
    - See `NaiveArrayQueue` vs `BetterArrayQueue` linked at the end of this section.
  - Could still do better with Doubly-Linked List.

2\) **Doubly Linked List**
- A Queue can be implemented as a Doubly-Linked List by just enforcing constraints on it that only allow you to add to the back, delete from the front and peek at the first element in the front of the Queue.

- **Analysis**
  - Doubly-Linked List is the superior implementation - pure constant runtime.

### Usage
- Printing queues.
- Handling asynchronous requests - they ensure that the requests are processed in the order in which they are received.

[Queue - array implementation](./lib/array_queue.rb)

-------------------------------------

## Tree
> A **Tree** data structure is used to store hierarchical data (it is non-linear). It contains nodes where each node has a parent-child relationship.

### Terminology
- **depth of tree**: deepest path from leaf to node
  - Also referred to as **levels**
- **root**: top level node
- **leaf**: a node with no children
- nodes in the same row are **siblings**
- if a node connects to other nodes, then the preceding node is the **parent** and the nodes following it are **child** nodes
- **subtree**: consists of a node and all of its **descendants**

### Specifications
- Directional (root to leaves)
- Each child node must have a parent and only one parent

### API
- `add_child(node)`: adds a child node to a parent
- `remove_child(node)`: removes a child node from a parent
- `count`: returns the count of nodes starting from the passed in node and including all of its descendants

### Implementation
- When creating a tree object, you can keep all of the logic in a Node class.
  - You just create a root node and build off of it: once you have the root you have the whole tree.
  - The tree is uni-directional so you can only build children off of the root.
  - And the tree itself is recursive: the BFS and DFS algorithms apply the same way to the root as they do to any child node.

### Sub-Types
- The sub-types are determined by the maximum number of children, not the number of children at any particular node.
- Note: the implementation above is generalized to apply to all types of the tree data structure. For specific implementations, augment to include the below restrictions for each type.

1\) **Binary Tree**:
- Binary Tree has maximum 2 children, but any node can have either zero, one, or two children.
- No notion of order: note the nodes in the below example can really be in any order.

    ```
      1
     / \
    2   3
    ```
- **Time Complexity**

Method | Avg. Case| Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`add_child` | O(1) |    O(1)     |   O(1)
`remove_child` | O(n) | O(n)   | O(n)
`count` |  O(n)    |     O(n)   |    O(1)  |

- Note: Time complexities assume you are calling these methods on the root node.

- **Space Complexity**: O(n)

1a\) **Binary Search Trees**
- Used for searching
- An extension of the Binary Tree with the addition of a restriction:
  - The child nodes are stored in a specific order: the left subtree of a node only contains values less than itself and the right subtree only contains values greater than it.

    ```
      2
     / \
    1   3
    ```

- **Time Complexity**

Method | Avg. Case| Worst Case | Best Case | Notes
---    | ---      | ---        | ---       | ---
`add_child` | log(n) | O(n)     |  O(1)    | Refer to this method by the Avg. Case: you can only add from the root so it has to find the correct node to add to either from the left or right. Worst Case: the tree is one-sided so you can't take advantage of the logarithmic property of this tree type
`remove_child` | log(n) | O(n)  |  O(1)    |
`count` |     O(n)       |  O(n) |  O(1)   |

- Note: Time complexities assume you are calling these methods on the root node.

- **Space Complexity**: O(n)

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

- **Space Complexity**: O(n)

### Usefulness
- Binary Search Tree: maintains order and has fast search, insertion and deletion.
  - Used on databases to perform quick searches.
- The others are useful for storing data:
  - Operating Systems use tree structure to store files.
  - HTML `DOM` uses a tree data structure to represent the hierarchy of elements.


[Tree - Poly Tree implementation](./lib/poly_tree.rb)
