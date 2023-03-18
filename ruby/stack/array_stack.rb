class ArrayStack
  def initialize
    @stack_arr = []
  end

  def push(el)
    stack_arr.push(el)
  end

  def pop
    stack_arr.pop
  end

  def peek
    stack_arr.last
  end

  private

  attr_reader :stack_arr
end
