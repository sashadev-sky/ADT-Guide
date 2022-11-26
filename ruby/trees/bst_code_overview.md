# Binary Search Tree Code Overview

Many of the methods that we'll write for the BST are inherently a recursive algorithm.

## Insert

```ruby
  def insert(val)
    @root = insert_tree_node(@root, val)
  end
```

**(Recursive Approach)**  ✅

> This is the canonical way to insert new items into a BST

- If root is nil, make the new node the root
- If val is greater than root.val, recusively insert the val to root.right
- Else, recursivley insert the val to root.left

```ruby
def insert_tree_node(root, val)
  return BSTNode.new(val) if root.nil?

  if val > root.val
    root.right = insert_tree_node(root.right, val)
  else
    root.left = insert_tree_node(root.left, val)
  end

  root
end
```

<details>
  <summary>Iterative Approach</summary>

  ```ruby
    def iterative_insert_tree_node(val)
      node = BSTNode.new(val)

      if @root.nil?
        @root = node
      else
        curr, parent = @root, nil
        while curr
          parent = curr
          if val <= curr.val
            curr = curr.left
            parent.left = node if curr.nil?
          else
            curr = curr.right
            parent.right = node if curr.nil?
          end
        end
      end
    end
```

</details>

-----------------------------------------------------------------

## Find

**(Recursive Approach)**  ✅

- If the root is nil or root.val == val, return root
- Elsif value is less than root.val, recursivley examine root.left
- Else recursively examine root.right.
- Return nil if val does not exist

```ruby
def find(root, val)
  return root if root.nil? || val == root.val
  return find(root.left, val) if val < root.val

  find(root.right, val)
end
```

<details>
  <summary>Iterative Approach</summary>

  ```ruby
    def iterative_find(root, val)
      root = val < root.val ? root.left : root.right while !root.nil? && root.val != val

      root
    end
```

</details>

-----------------------------------------------------------------

## Delete

```ruby
  def delete(val)
    @root = delete_from_tree(@root, val)
  end

  def change_parent(node)
    replacement_node = maximum(node.left)
    promote_child(node.left) if replacement_node.left

    replacement_node.left = node.left
    replacement_node.right = node.right

    replacement_node
  end

  def maximum(node = @root)
    return node if node.right.nil?

    maximum(node.right)
  end

  def promote_child(node)
    return node unless node.right

    current_parent = node
    maximum_node = maximum(node.right)
    current_parent.right = maximum_node.left
  end

  def remove(node)
    if node.left.nil? && node.right.nil?
      node = nil
    elsif node.left && node.right.nil?
      node = node.left
    elsif node.left.nil? && node.right
      node = node.right
    else
      node = change_parent(node)
    end
  end
```

**(Recursive Approach)**  ✅

- Recursively search for the node
- If node is nil, return nil (**`delete_from_tree`**)
- If node has one child, replace node with the child (**`remove`**)
- If node has two children, replace node with the maximum of it's smaller children (**`change_parent`**)
- If that node has a left side, promote that left side to the node's previous position (**`promote_child`**)

```ruby
def delete_from_tree(node, val)
  return nil if node.nil?

  if node.val == val
    node = remove(node)
  elsif val <= node.val
    node.left = delete_from_tree(node.left, val)
  else
    node.right = delete_from_tree(node.right, val)
  end

  node
end
```

-----------------------------------------------------------------
