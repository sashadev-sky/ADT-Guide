# The provided implementation is a basic hash set that uses separate
# chaining for handling hash collisions.
class HashSet
  attr_reader :count

  def initialize(num_buckets = 8)
    @store = Array.new(num_buckets) { [] }
    @count = 0
    @load_factor = 0.75
  end

  def insert(key)
    return false if include?(key)

    self[bucket_index(key)] << key
    @count += 1
    resize! if needs_resizing?

    key
  end

  def include?(key)
    self[bucket_index(key)].include?(key)
  end

  def remove(key)
    return nil unless include?(key)

    self[bucket_index(key)].delete(key)
    @count -= 1
  end

  private

  def num_buckets
    @store.length
  end

  def needs_resizing?
    @count.to_f / num_buckets >= @load_factor
  end

  def resize!
    old_store = @store
    @count = 0
    @store = Array.new(num_buckets * 2) { [] }

    old_store.flatten.each { |key| insert(key) }
  end

  def bucket_index(key)
    key.hash % num_buckets
  end

  def [](num)
    @store[num]
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
