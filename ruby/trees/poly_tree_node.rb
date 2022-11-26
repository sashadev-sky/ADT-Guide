require_relative './searchable'

# represents a node in a PolyTree
class PolyTreeNode
  include Searchable

  attr_accessor :val
  attr_reader :parent

  def initialize(val = nil)
    @val, @parent, @children = val, nil, []
  end

  def to_s
    "#{@val}"
  end

  def children
    @children.dup
  end

  def parent=(parent)
    return if self.parent == parent

    self.parent&._children&.delete(self)

    @parent = parent
    self.parent._children << self unless self.parent.nil?
  end

  def add_child(child)
    child.parent = self
  end

  def remove_child(child)
    raise "Tried to remove a node that isn't a child" if child && !children.include?(child)

    child.parent = nil
  end

  def count(node = self)
    return 0 if node.nil?

    return 1 if node._children.empty?

    1 + node._children.map(&:count).inject(:+)
  end

  protected

  # Protected method to give a node direct access to another node's children.
  def _children
    @children
  end
end

if $PROGRAM_NAME == __FILE__
  node1 = PolyTreeNode.new(1)
  node2 = PolyTreeNode.new(2)
  node3 = PolyTreeNode.new(3)
  node4 = PolyTreeNode.new(4)
  node5 = PolyTreeNode.new(5)
  node1.add_child(node2)
  node3.parent = node1
  node1.add_child(node4)
  node1.add_child(node5)

  # Creates the tree
  #
  #        1
  #      /| |\
  #    2 3 4  5
  #

  puts node1.children.join(', ') # 2, 3, 4, 5
  puts node1.count # 5

  puts node1.bfs(4).val # 4
  puts node1.bfs(4) == node4 # true
  puts node1.dfs(4).val # 4
  puts node1.dfs(4) == node4 # true

  node6 = PolyTreeNode.new(6)
  node7 = PolyTreeNode.new(7)
  node8 = PolyTreeNode.new(8)

  # Creates the tree
  #
  #        1
  #      /| |\
  #    2 3 4  5
  #     / /\
  #    8 6  7
  #

  node4.add_child(node6)
  node4.add_child(node7)
  node3.add_child(node8)

  puts node1.count # 8
  puts node3.count # 2
  puts node4.count # 3
end
