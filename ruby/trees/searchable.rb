# A module with the logic for searching a tree with BFS and DFS algorithms.
# To implement this mixin, a class requires #children and #val.
module Searchable
  def dfs(target = nil, &prc)
    raise 'Method needs a proc or target' if [target, prc].none?

    prc ||= proc { |node| node.val == target }

    return self if prc.call(self)

    children.each do |child|
      search_result = child.dfs(&prc)
      return search_result unless search_result.nil?
    end

    nil
  end

  # bfs uses a local array variable as a Queue
  def bfs(target = nil, &prc)
    raise 'Method needs a proc or target' if [target, prc].none?

    prc ||= proc { |node| node.val == target }

    nodes = [self]
    until nodes.empty?
      node = nodes.shift

      return node if prc.call(node)

      nodes.concat(node.children)
    end

    nil
  end
end
