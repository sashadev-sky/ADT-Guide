require_relative './node'

class DoublyLinkedList
  include Enumerable

  # initializing sentinal nodes as placeholders
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

    current_node
  end

  def empty?
    head.next_node == tail
  end

  def first
    empty? ? nil : head.next_node
  end

  def last
    empty? ? nil : tail.prev_node
  end

  def get(key)
    each { |node| return node.val if node.key == key }
    nil
  end

  def update(key, value)
    each do |node|
      if node.key == key
        node.val = value
        return node
      end
    end
  end

  def include?(key)
    node_scan1 = head.next_node

    until node_scan1 == tail
      return true if node_scan1.key == key

      node_scan1 = node_scan1.next_node
    end
    false
  end

  def append(key, value)
    el = Node.new(key, value, tail)
    last_node = tail.prev_node
    last_node.next_node = el
    el.prev_node = last_node
    tail.prev_node = el
    el
  end

  def prepend(key, value)
    el = Node.new(key, value, nil, head)
    first_node = head.next_node
    first_node.prev_node = el
    el.next_node = first_node
    head.next_node = el
    el
  end

  def remove(key)
    current_node = head.next_node

    until current_node == tail
      if current_node.key == key
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
    inject([]) { |acc, node| acc << "[#{node.key}, #{node.val}]" }.join(', ')
  end

  private

  attr_reader :head, :tail
end

# run these tests to see how the list works

if $PROGRAM_NAME == __FILE__
  list = DoublyLinkedList.new
  list.append('link1', 3)
  list.append('link2', 0)
  list.append('link3', 2)
  list.append('link4', 5)
  list.append('link5', 5)
  puts list[1]
  puts list[3]
  puts list # [link1, 3], [link2, 0], [link3, 2], [link4, 5], [link5, 5]
  puts list.first
  puts list.last
  p list.include?('link9')
  p list.include?('randomtext')
  p list.include?('link3')
  list.remove('link5')
  list.remove('link4')
  list.remove('link1')
  p list.empty?
  puts list.get('link2')
  puts list.update('link35', 12)
  puts list.update('link2', 9)
  puts list.get('link2')
  list.remove('link2')
  list.remove('link3')
  p list.empty?
end
