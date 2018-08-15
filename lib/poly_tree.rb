class PolyTreeNode

  attr_accessor :value
  attr_reader :parent

  def initialize(value = nil)
    @value, @parent, @children = value, nil, []
  end

  def children
    @children.dup
  end

  # this simplifies the code to do the adding and removing operations
  # under one method
  def parent=(parent)
    return if self.parent == parent

    if self.parent
      self.parent._children.delete(self)
    end

    @parent = parent
    unless self.parent.nil?
      self.parent._children << self
    end

    self
  end

  def add_child(child)
    child.parent = self
  end

  def remove_child(child)
    if child && !self.children.include?(child)
      raise "Tried to remove a node that isn't a child"
    end

    child.parent = nil
  end

  def count
    1 + children.map(&:count).inject(:+)
  end

  protected

  # Protected method to give a node direct access to another node's children.
  def _children
    @children
  end

end
