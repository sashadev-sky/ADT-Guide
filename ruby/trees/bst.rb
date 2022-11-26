require_relative './bst_node'

class BinarySearchTree
  attr_reader :root

  def initialize
    @root = nil
  end

  def insert(val)
    @root = insert_tree_node(@root, val)
  end

  def find(node, val)
    return node if node.nil? || val == node.val
    return find(node.left, val) if val < node.val

    find(node.right, val)
  end

  def delete(val)
    @root = delete_from_tree(@root, val)
  end

  # O(n): must check every node (stops at first detected violation).
  def valid_bst?(node, min = nil, max = nil)
    return true if node.nil?

    return false if (min && (min > node.val)) || (max && (max < node.val))

    valid_bst?(node.left, min, node.val) && valid_bst?(node.right, node.val, max)
  end

  private

  def insert_tree_node(node, val)
    return BSTNode.new(val) unless node

    if val <= node.val
      node.left = insert_tree_node(node.left, val)
    else
      node.right = insert_tree_node(node.right, val)
    end

    node
  end

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
end

if $PROGRAM_NAME == __FILE__
  tree = BinarySearchTree.new
  tree.insert(5)
  tree.insert(2)
  tree.insert(7)
  tree.insert(9)
  tree.insert(1)
  tree.insert(8)
  tree.insert(3)
  tree.insert(10)
  tree.insert(13)
  tree.insert(6)

  # Creates the tree
  #
  #         5
  #       /   \
  #      2      7
  #     / \    /  \
  #    1   3  6    9
  #              /  \
  #             8    10
  #                   \
  #                   13
  #

  found = tree.find(tree.root, 7)
  puts "Node: #{found.val}" # 7
  puts "\tLeft Child: #{found.left}" # 6
  puts "\tRight Child: #{found.right}" # 9
  found = tree.find(tree.root, 10)
  puts "Node: #{found}" # 10
  puts "\tLeft Child: #{found.left}" # nil
  puts "\tRight Child: #{found.right}" # 13

  tree.delete(10)
  found = tree.find(tree.root, 10)
  puts "Node: #{found}" # nil

  found = tree.find(tree.root, 9)
  puts "Node: #{found.right}" # 13

  puts "Count: #{tree.root.count}" # 9

  tree.insert(6)

  puts "Count: #{tree.root.count}" # 10
end
