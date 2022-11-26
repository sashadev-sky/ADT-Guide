# naive Queue implementation using an array. (Linear time complexity)

class NaiveArrayQueue
  def initialize
    @queue_arr = []
  end

  def enqueue(el)
    queue_arr.push(el)
    el
  end

  def dequeue
    queue_arr.shift
  end

  def first
    queue_arr.first
  end

  def is_empty
    queue_arr.empty?
  end

  private

  attr_reader :queue_arr
end

# clever Queue implementation using an array. Constant time complexity (amortized)

class StackQueue
  def initialize
    @queue_arr1 = []
    @queue_arr2 = []
  end

  def enqueue(el)
    queue_arr1.push(el)
    el
  end

  def dequeue
    if queue_arr2.empty?
      queue_arr2.push(queue_arr1.pop) until queue_arr1.empty?
    end
    queue_arr2.pop
  end

  def first
    if queue_arr2.length
      queue_arr2.last
    elsif queue_arr1.length
      queue_arr1.first
    else
      []
    end
  end

  def is_empty
    queue_arr1.empty? && queue_arr2.empty?
  end

  private

  attr_reader :queue_arr1, :queue_arr2
end
