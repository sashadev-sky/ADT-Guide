class HashSet
  attr_reader :count

  def initialize(num_buckets = 8)
    @store = Array.new(num_buckets) { [] }
    @count = 0
  end

  def insert(key)
    return false if include?(key)

    self[key.hash] << key
    @count += 1
    resize! if num_buckets < @count

    key
  end

  def include?(key)
    self[key.hash].include?(key)
  end

  def remove(key)
    return nil unless include?(key)

    self[key.hash].delete(key)
    @count -= 1
  end

  private

  def num_buckets
    @store.length
  end

  def resize!
    old_store = @store
    @count = 0
    @store = Array.new(num_buckets * 2) { [] }

    old_store.flatten.each { |key| insert(key) }
  end

  def [](num)
    @store[num % num_buckets]
  end
end

if $PROGRAM_NAME == __FILE__
  set = HashSet.new
  set.insert(1)
  set.insert('hey')
  puts set.include?(1) # => true
  puts set.include?(2) # => false
  set.insert(-300)
  set.insert(2)
  set.insert(3)
  set.insert(400)
  set.insert(-500)
  set.insert('hi')

  p set
end
