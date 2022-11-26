class ArrayMap
  def initialize
    @map_array = []
  end

  def set(key, value)
    pair_index = map_array.index { |pair| pair[0] == key }
    pair_index ? map_array[pair_index][1] = value : map_array.push([key, value])
  end

  def get(key)
    map_array.each { |el| return el if el[0] == key }
  end

  def delete(key)
    map_array.each { |el| map_array.delete(el) if key == el[0] }
  end

  def show
    deep_dup(map_array)
  end

  private

  attr_reader :map_array

  def deep_dup(arr)
    arr.map { |el| el.is_a?(Array) ? deep_dup(el) : el }
  end
end
