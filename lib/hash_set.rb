# this code is an implementation for a general Set

class HashSet
  def initialize
    @members = {}
  end

  def insert(el)
    members[el] = true
  end

  def include?(el)
    members.include?(el)
  end

  def delete(el)
    members.delete(el)
    members.keys
  end

  def show
    members.keys
  end

  def union(set2)
    new_set = self.class.new
    self.members.each_key { |el| new_set.insert(el) }
    set2.members.each_key { |el| new_set.insert(el) }
    new_set
  end

  def intersection(set2)
    new_set = self.class.new
    self.members.each_key { |el| new_set.insert(el) if set2.include?(el) }
    new_set
  end

  def difference(set2)
    new_set = self.class.new
    self.members.each_key { |el| new_set.insert(el) unless set2.include?(el) }
    new_set
  end

  # `==` returns true if object is a `HashSet`, is the same size as the current set,
  # and each of it members is a member of the current set.
  def ==(object)
    object.is_a?(HashSet) && object.members == self.members
  end

  protected

  attr_reader :members

end
