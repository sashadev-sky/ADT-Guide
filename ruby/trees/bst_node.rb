class BSTNode
  attr_accessor :val, :left, :right

  def initialize(val)
    @val = val
    @left = nil
    @right = nil
  end

  def to_s
    "#{@val}"
  end

  def count(node = self)
    return 0 if node.nil?

    1 + count(node.left) + count(node.right)
  end
end
