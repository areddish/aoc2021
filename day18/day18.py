import ast

def bfs(node, check_fn, op_fn, level = 0):
   if not isinstance(node, Node):
      return False

   if isinstance(node.left, Node):
      if check_fn(node.left, level):
         op_fn(node.left)
         return True
      res = bfs(node.left, check_fn, op_fn, level + 1)
      if res:
         return res
   if isinstance(node.right, Node):
      if check_fn(node.right, level):
         op_fn(node.right)
         return True
      res = bfs(node.right, check_fn, op_fn, level + 1)
      return res

def right_most(node, val):
   # base case, this is a number
   if not isinstance(node, Node):
      return node

   if isinstance(node.right, Node):
      if node.right.left_val() != -1:
         node.right.left += val
         return True
      if node.right.right_val() != -1:
         node.right.right += val
         return True
      if right_most(node.right, val):
         return True
   elif isinstance(node.left, Node):
      if node.left.left_val() != -1:
         node.left.left += val
         return True
      if node.left.right_val() != -1:
         node.left.right += val
         return True
      if right_most(node.left, val):
         return True
   else:
      node.left += val
      return True

   return None

def left_most(node, val):
   # base case, this is a number
   if not isinstance(node, Node):
      return True

   if isinstance(node.left, Node):
      if node.left.left_val() != -1:
         node.left.left += val
         return True
      if node.left.right_val() != -1:
         node.left.right += val
         return True
      if left_most(node.left, val):
         return True
   elif isinstance(node.right, Node):
      if node.right.left_val() != -1:
         node.right.left += val
         return True
      if node.right.right_val() != -1:
         node.right.right += val
         return True
      if left_most(node.left, val):
         return True
   else:
      node.left += val
      return True
   return None
   
class Node:
   def __init__(self, left, right, parent=None):
      self.left = left
      self.right = right
      self.parent = parent

   def add(self, pair):
      pass
      
   @staticmethod
   def split(node, is_left):
      if is_left:
         val = node.left
         print("split left:", val)
         node.left = Node(val//2, (val+1)//2, node)
      else:
         val = node.right
         print("split right:", val)
         node.right = Node(val//2, (val+1)//2, node)

   def magnitude(self):
      sum = 0
      if isinstance(self.left, Node):
         sum += 3 * self.left.magnitude()
      else:
         sum += 3 * self.left
      if isinstance(self.right, Node):
         sum += 2 * self.right.magnitude()
      else:
         sum += 2 * self.right
      return sum

   def reduce(self, run_once=False):
      actioned = True
      while actioned:
         print("BEFORE:",end="")
         self.print()
         actioned = bfs(self, lambda x,level: isinstance(x, Node) and level == 3, lambda x: x.explode())
         if not actioned:
            actioned = bfs(self, lambda x, level: isinstance(x, Node) and (x.left_val() > 10 or x.right_val() > 10), lambda x: Node.split(x, x.left_val() > 10))
         print("AFTER:",end="")
         self.print()
         if run_once:
            return

   def explode(self):
      print("expldde", self.left, self.right)

      # something is still wrong here. jsut swapped left_most an right_most
      cur = self
      par = self.parent
      while par and par.left == cur:
         cur = par
         par = par.parent
      if par:
         if par.left_val() != -1:
            par.left += self.left
         else:
            print("leftmost is ", self.left, "+", right_most(par.left, self.left))

      cur = self
      par = self.parent
      while par and par.right == cur:
         cur = par
         par = par.parent
      if par:
         if par.right_val() != -1:
            par.right += self.right
         else:
            print("right is ", self.right, "+", left_most(par.right, self.right))
      
      # Find left most
      if self.parent:
         if self.parent.left == self:
            print ("left")
            self.parent.left = 0
         else:
            assert self.parent.right == self
            print("right")
            self.parent.right = 0

      return self
   
   def left_val(self):
      if isinstance(self.left, Node):
         return -1
      return self.left

   def right_val(self):
      if isinstance(self.right, Node):
         return -1
      return self.right

   def print(self):
      as_str = "["
      if isinstance(self.left, Node):   
         as_str += self.left.print()
      else:
         as_str += str(self.left)
      as_str += ", "
      if isinstance(self.right, Node):   
         as_str += self.right.print()
      else:
         as_str += str(self.right)
      as_str += "]"
      return as_str

   @staticmethod
   def add(node1, node2):
      assert node1.parent == None
      assert node2.parent == None

      n = Node(node1, node2, None)
      node1.parent = n
      node2.parent = n
      n.reduce()
      return n

   @staticmethod
   def node_from_list(l, parent):
      n = Node(None, None, None)
      n.left = Node.node_from_list(l[0], n) if isinstance(l[0], list) else l[0]
      n.right = Node.node_from_list(l[1], n) if isinstance(l[1], list) else l[1]
      n.parent = parent
      return n

   @staticmethod
   def node_from_str(l_str):
      return Node.node_from_list(ast.literal_eval(l_str), None)

class Snailfish:
   def __init__(self, pair):
      self.pair = pair

   def add(self, snailfish):
      self.pair = [ self.pair ] + [ snailfish.pair ]
      self.reduce()

   def explode(self, pair, parents):
      print("exploding: ", pair, parents)

      left = pair[0]
      right = pair[1]

     # assert parents[-1] == pair
# bug is here:
      # add left to the first left
      # starting at the parent above us we look to see if the left node is a list
      i = -2
      p = parents[i]
      while not p[0]:
         i -= 1
         p = parents[i]
      self.post_fix_value(p, left)

      i = -2
      p = parents[i]
      while not p[1]:
         i -= 1
         p = parents[i]
      self.pre_fix_value(p, right)

### POST_FIX/PREFIX aren't adding right, that's last bit

   def post_fix_value(self, root, val):
      if isinstance(root, list):
         return False

      r = self.post_fix_value(root[0], val)
      if not r:
         r = self.post_fix_value(root[1], val)

      if not r and self.num_val(root[1]) != -1:
         root[1] += val
         return True
      return r

   def pre_fix_value(self, root, val):
      if self.num_val(root[0]) != -1:
         root[0] += val
         return True

      if isinstance(root, list):
         return False

      r = self.post_fix_value(root[0], val)
      if not r:
         r = self.post_fix_value(root[1], val)
      return r

   def reduce(self, run_once=False):
      actioned = True
      while actioned:
         print("BEFORE:", self.pair)
         actioned = self.bfs_level(self.pair, [])
         if not actioned:
            actioned = self.bfs_greater_than_10(self.pair)
         print("AFTER:", self.pair)
         if run_once:
            return

   @staticmethod
   def num_val(val):
      if isinstance(val, list):
         return -1
      return val

   def bfs_greater_than_10(self, pair):
      if not pair or not isinstance(pair, list):
         return False

      if Snailfish.num_val(pair[0]) > 10:
         pair[0] = Snailfish.split(pair[0])
         return True
      if Snailfish.num_val(pair[1]) > 10:
         pair[1] = Snailfish.split(pair[1])
         return True
      
      if self.bfs_greater_than_10(pair[0]):
         return True

      return self.bfs_greater_than_10(pair[1])
         
   def bfs_level(self, pair, parents, level=0):
      if not pair or not isinstance(pair, list):
         return False

      parents.append(pair)
      if level == 3:
         if isinstance(pair[0], list):
            self.explode(pair[0], parents)
            pair[0] = 0
            return True
         if isinstance(pair[1], list):
            self.explode(pair[1], parents)
            pair[1] = 0
            return True

      if self.bfs_level(pair[0], parents, level + 1):
         return True

      return self.bfs_level(pair[1], parents, level + 1)

   @staticmethod    
   def split(num):
      print("SPLIT: ", num, [num//2, (num+1)//2])
      return [num//2, (num+1)//2]

   def magnitude(self):
      return self.magnitude_pair(self.pair)
      #return 3*self.magnitude_pair(self.left)+2*self.magnitude_pair(self.right)
   
   def magnitude_pair(self, pair):
      if isinstance(pair, list):
         return 3*self.magnitude_pair(pair[0]) + 2*self.magnitude_pair(pair[1])
      return pair

   # self.bfs(lambda x, level: not isinstance(x, list) and x > 10)
   # self.bfs(lambda x, level: isinstance(x, list) and level > 3)

   # def bfs_explode(self, check, level=0):
   #    left_is_pair = isinstance(self.left, list)
   #    if level == 3:
   #       if isinstance(self.left, list):
   #          self.explode(self.left)
   #       else isinstance(self.right, list):
   #          self.explode(self.right)
   #       return

   #    if 

   #       # go left
   #       return bfs(self.left, check level+=1)
   #    else:
   #       if self.left > 10:
   #          return "split"
   #    if isinstance(self.right, list):
   #       # go right
   #       bfs(right, level+=1)
   #    else:
   #       if self.left > 10:
   #          return "split"
      
   # def get_leftmost(self):
   #    level = 0
   #    cur = self.left
   #    while isinstance(cur, list) and level < 3:
   #       cur = cur[0]
   #       level += 1
   #    return cur, level

   # def get_rightmost(self):
   #    level = 0
   #    cur = self.right
   #    while isinstance(cur, list) and level < 3:
   #       cur = cur[1]
   #       level += 1
   #    return cur, level

   def parse(snailfish_str):
      l = ast.literal_eval(snailfish_str)
      n = Node.node_from_list(l, None)
      return Snailfish(l)

   # def parse_impl(snailfish_str):
   #    left_values = []
   #    right_values = []
   #    level = 0
   #    val = None
   #    parse_left = True
   #    for x in snailfish_str:
   #       if x == "[":
   #          level += 1
   #          parse_left = True
   #       elif x == ",":
   #          parse_left = False
   #       elif x == "]":
   #          level -= 1
   #          parse_left = True
   #          val = [left_values.pop(), right_values.pop()]
   #          if parse_left:
   #             left_values.append(val)
   #          else:
   #             right_values.append(val)
   #       else:
   #          val = int(x)
   #          if parse_left:
   #             left_values.append(val)
   #          else:
   #             right_values.append(val)
   #    assert len(right_values) == 0
   #    l, r = left_values.pop()
   #    return Snailfish(l, r)      

with open("test4.txt", "rt") as file:
   data = [x.strip() for x in file.readlines()]
   # fish = Snailfish.parse(data[0])
   # for line in data[1:]:
   #    next_fish = Snailfish.parse(line)
   #    fish.add(next_fish)
   fish = Node.node_from_str(data[0])
   print(fish.print())
   for line in data[1:]:
      next_fish = Node.node_from_str(line)
      fish = Node.add(fish, next_fish)


   print(f"Part 1 = {fish.magnitude()}")


def explode(pair):
   pass   

def reduce(expr):
   # If any pair is nested inside four pairs, the leftmost such pair explodes.
   # If any regular number is 10 or greater, the leftmost such regular number splits
   return expr

# explosion tests
# assert explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
# assert explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
# assert explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
# assert explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# assert explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

# split tests
assert Snailfish.split(10) == [5, 5]
assert Snailfish.split(11) == [5, 6]
assert Snailfish.split(12) == [6, 6]
assert Snailfish.split(9) == [4, 5]

assert Snailfish.parse("[[1,2],[[3,4],5]]").magnitude() == 143
assert Snailfish.parse("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384
assert Snailfish.parse("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
assert Snailfish.parse("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
assert Snailfish.parse("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
assert Snailfish.parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude() == 3488

assert Node.node_from_str("[[1,2],[[3,4],5]]").magnitude() == 143
assert Node.node_from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384
assert Node.node_from_str("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
assert Node.node_from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
assert Node.node_from_str("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
assert Node.node_from_str("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude() == 3488
assert Node.node_from_str("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]").magnitude() == 4140

assert Node.node_from_str("[[[[[9,8],1],2],3],4]").print() == str([[[[[9,8],1],2],3],4])

explode_tests = [ 
 #  ["[[[[[9,8],1],2],3],4]", str([[[[0,9],2],3],4])], 
 #  ["[7,[6,[5,[4,[3,2]]]]]", str([7,[6,[5,[7,0]]]])], 
 #  ["[[6,[5,[4,[3,2]]]],1]",str([[6,[5,[7,0]]],3])], 
   ["[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", str([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])], 
 # ["[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", str([[3,[2,[8,0]]],[9,[5,[7,0]]]])]
]
for test in explode_tests:
   node = Node.node_from_str(test[0])
   print(node.print())
   node.reduce(True)
   print(node.print())
   assert node.print() == test[1]
