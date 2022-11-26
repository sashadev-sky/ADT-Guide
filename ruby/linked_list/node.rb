class Node
  attr_accessor :key, :val, :next_node, :prev_node

  def initialize(key = nil, val = nil, next_node = nil, prev_node = nil)
    @key = key
    @val = val
    @next_node = next_node
    @prev_node = prev_node
  end

  def to_s
    "#{@key}: #{@val}"
  end
end
