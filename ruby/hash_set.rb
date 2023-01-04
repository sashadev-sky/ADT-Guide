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
