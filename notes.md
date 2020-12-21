# DS Complexities

<https://wiki.python.org/moin/TimeComplexity>

## Lists and Tuples

- Lists and tuples are a class of data structures called arrays.

### Lists

- Dynamic arrays that let us modify and resize the data we are storing
- Have a built-in sorting algorithm that uses Tim sort.
- Use for storing collections of data about completely disparate objects
- Building a list with appends versus a list comprehension:
  - Uses more memory because of the extra memory allocated when resizing. When creating a list directly, only the number of elements needed is alloccated.
  - Overall runtime is slower, because of the extra Python statements that must be run as well as the cost of reallocating memory

### Tuples

- Static arrays whose contents are fixed and immutable
- Cached by the Python runtime, which means we don't need to talk to the kernel to reserve memory everytime we want to use one. (Created quicker than lists)
  - For tuples of sizes 1-20, when they are no longer in use, the space isn't immediately given back to the system: up to 20,000 of each size are saved for future use. This means that when a new tuple of that size is needed in the future, we don't need to communicate with the operating system to find a region in memory to put the data into, since we have a reserve of free memory already. However, this also means that the Python proccess will have some extra memory overhead.
- Use for describing multiple properties of one unchanging thing
- Because of its fixed length, a tuple instance is allocated the exact memory space in needs. Instances of list, on the other hand, are allocated with room to spare, to ammortize the cost of future appends.
- Both lists and tuples can take mixed types. This can introduce quite a bit of overhead and
  reduce some potential optimizations. This overhead can be removed if we force all our data to be of the same type.

#### Exercise

For the following example datasets, would you use a tuple or list?

1. First 20 prime numbers: Tuple, since the data is static and will not change
2. Names of programming languages: List, since the dataset is constantly growing
3. A person's age, weight, and height: List, since the values will need to be updated
4. A person's birthday and birthplace: Tuple, since the information is static and will not change
5. The result of a particular game of pool: Tuple, since the data is static
6. The results of a continuing series of pool games: List, since more games will be played. In fact, we could use a list of tuples since each individual game's results will not change, but we will need to add more results as more games are played.

## Arrays

Arrays represent basic values and behave very much like lists, except
the type of objects stored in them is constrained. The type is specified
at object creation time by using a `type code`, which is a single character.
The following type codes are defined:

 |Type code |  C Type            | Minimum size in bytes|
 |----------|--------------------|----------------------|
 |   'b'    |   signed integer   |  1                   |
 |   'B'    |   unsigned integer |  1                   |
 |   'u'    |   Unicode character|  2 (see note)        |
 |   'h'    |   signed integer   |  2                   |
 |   'H'    |   unsigned integer |  2                   |
 |   'i'    |   signed integer   |  2                   |
 |   'I'    |   unsigned integer |  2                   |
 |   'l'    |   signed integer   |  4                   |
 |   'L'    |   unsigned integer |  4                   |
 |   'q'    |   signed integer   |  8 (see note)        |
 |   'Q'    |   unsigned integer |  8 (see note)        |
 |   'f'    |   floating point   |  4                   |
 |   'd'    |   floating point   |  8                   |

`NumPy` has arrays that can hold a wider range of datatypes — you have more control
over the number of bytes per item, and you can use `complex` numbers and `datetime`
objects. A `complex128` object takes 16 bytes per item: each item is a pair of 8-byte
floating-point numbers. You can’t store complex objects in a Python array, but
they come for free with numpy.

Using a regular list to store many numbers is much less efficient in RAM than using an array object.

### Static Array

- **`get`**: `0(1)` (`address + (idx * 8)`)
- **`set`**: `0(1)`

## Dictionaries and Sets

- Dictionaries and sets give us `O(1)` lookups based on the arbitrary index.
- In addition, like lists/tuples, dictionaries and sets have `O(1)` insertion time.
  - This speed is accomplished through the use of an open address hash table as the underlying data structure.
- However, there is a cost to using dictionaries and sets.
  - First, they generally take up a larger footprint in memory.
  - Also, although the complexity for insertions/lookups is `O(1)`, the actual speed depends greatly on the hashing function that is in use.

This idea of “how well distributed my hash function is” is called the **entropy** of the hash function.

- It is maximized when every hash value has equal probability of being chosen. A hash function that maximizes entropy is called an ideal hash function since it guarantees the minimal number of collisions.
