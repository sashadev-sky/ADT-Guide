class Node

  attr_accessor :val, :next_node, :prev_node

  def initialize(val = nil, next_node = nil, prev_node = nil)
    @val = val
    @next_node = next_node
    @prev_node = prev_node
  end

  def to_s
    "#{@val}"
  end

end

class DoublyLinkedList
  include Enumerable

  # creating sentinal nodes as placeholders
  def initialize
    @head = Node.new
    @tail = Node.new
    @head.next_node = @tail
    @tail.prev_node = @head
  end

  def [](index)
    current_node = head.next_node
    current_index = 0

    until current_index == index
      current_node = current_node.next_node
      current_index += 1
      return nil if current_node == tail
    end

    current_node.val
  end

  def empty?
    head.next_node == tail
  end

  def first
    empty? ? nil : head.next_node.val
  end

  def last
    empty? ? nil : tail.prev_node.val
  end

  def include?(element)
    node_scan1 = head.next_node

    until node_scan1 == tail
      return true if node_scan1.val == element
      node_scan1 = node_scan1.next_node
    end
    false
  end

  def append(element)
    el = Node.new(element, tail)
    last_node = tail.prev_node
    last_node.next_node = el
    el.prev_node = last_node
    tail.prev_node = el
    el.val
  end

  def prepend(element)
    el = Node.new(element, nil, head)
    first_node = head.next_node
    first_node.prev_node = el
    el.next_node = first_node
    head.next_node = el
    el.val
  end

  def delete(element)
    current_node = head.next_node

    until current_node == tail
      if current_node.val == element
        previous_node = current_node.prev_node
        next_next_node = current_node.next_node
        previous_node.next_node = next_next_node
        next_next_node.prev_node = previous_node
        return current_node.val
      end
      current_node = current_node.next_node
    end
    nil
  end

  def each
    current_node = head.next_node
    until current_node == tail
      yield current_node
      current_node = current_node.next_node
    end
  end

  def to_s
    inject([]) { |acc, node| acc << "[#{node.val}]" }.join('->')
  end

  private

  attr_reader :head, :tail

end

# run these tests to see how the list works

if $PROGRAM_NAME == __FILE__
  list = DoublyLinkedList.new
  list.append(3)
  list.append(0)
  list.append(2)
  list.append(5)
  list.append(5)
  puts list[1]
  puts list[3]
  puts list
  puts list.first
  puts list.last
  p list.include?(4)
  p list.include?(1)
  p list.include?(2)
  p list.include?(8)
  list.delete(1)
  list.delete(2)
  list.delete(3)
  list.delete(4)
  p list.empty?
end
