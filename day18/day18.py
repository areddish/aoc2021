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
   assert isinstance(node, Node)
   # # base case, this is a number
   # if not isinstance(node, Node):
   #    return node

   if not isinstance(node.right, Node):
      node.right += val
      return True

   return right_most(node.right, val)

def left_most(node, val):
   assert isinstance(node, Node)
   # # base case, this is a number
   # if not isinstance(node, Node):
   #    return True

   if not isinstance(node.left, Node):
      node.left += val
      return True

   return left_most(node.left, val)
   
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
         #print("split left:", val)
         node.left = Node(val//2, (val+1)//2, node)
      else:
         val = node.right
         #print("split right:", val)
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
         #print("BEFORE:",end="")
         #self.print()
         actioned = bfs(self, lambda x,level: isinstance(x, Node) and level == 3, lambda x: x.explode())
         if not actioned:
            actioned = bfs(self, lambda x, level: isinstance(x, Node) and (x.left_val() >= 10 or x.right_val() >= 10), lambda x: Node.split(x, x.left_val() >= 10))
         #print("AFTER:",end="")
         #self.print()
         if run_once:
            return

   def explode(self):
      #print("explode", self.left, self.right)

      # something is still wrong here. jsut swapped left_most an right_most
      cur = self
      par = self.parent
      while par and par.left == cur:
         cur = par
         par = par.parent
      if par:
         if par.left_val() == -1:
            #print("par", par.print(), "leftmost is ", self.left, "+", right_most(par.left, self.left))
            right_most(par.left, self.left)
         else:
            par.left += self.left

      cur = self
      par = self.parent
      while par and par.right == cur:
         cur = par
         par = par.parent
      if par:
         if par.right_val() == -1:
            #print("right is ", self.right, "+", left_most(par.right, self.right))
            left_most(par.right, self.right)
         else:
            par.right += self.right

      # Find left most
      if self.parent:
         if self.parent.left == self:
            #print ("left")
            self.parent.left = 0
         else:
            assert self.parent.right == self
            #print("right")
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

with open("test3.txt", "rt") as file:
   data = [x.strip() for x in file.readlines()]

   fish = Node.node_from_str(data[0])
   print(fish.print() + " + ")
   print(fish.print())
   for line in data[1:]:
      next_fish = Node.node_from_str(line)
      print(next_fish.print())
      fish = Node.add(fish, next_fish)
      print(" === ", fish.print())
   print(fish.print())
   print(f"Part 1 = {fish.magnitude()}")

exit(-1)

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
   ["[[[[[9,8],1],2],3],4]", str([[[[0,9],2],3],4])], 
   ["[7,[6,[5,[4,[3,2]]]]]", str([7,[6,[5,[7,0]]]])], 
   ["[[6,[5,[4,[3,2]]]],1]",str([[6,[5,[7,0]]],3])], 
   ["[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", str([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])], 
   ["[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", str([[3,[2,[8,0]]],[9,[5,[7,0]]]])]
]
for test in explode_tests:
   node = Node.node_from_str(test[0])
   print(node.print())
   node.reduce(True)
   print(node.print())
   assert node.print() == test[1]



def gen_testcase(n):
   res = []
   for x in range(2,n+1):
      res.append([x,x])
   return res

cur = Node.node_from_list([1,1], None)
for n in gen_testcase(4):
   cur = Node.add(cur, Node.node_from_list(n,None))
assert cur.print() == str([[[[1,1],[2,2]],[3,3]],[4,4]])

cur = Node.node_from_list([1,1], None)
for n in gen_testcase(5):
   cur = Node.add(cur, Node.node_from_list(n,None))
assert cur.print() == str([[[[3,0],[5,3]],[4,4]],[5,5]])

cur = Node.node_from_list([1,1], None)
for n in gen_testcase(6):
   cur = Node.add(cur, Node.node_from_list(n,None))
print(cur.print())
assert cur.print() == str([[[[5,0],[7,4]],[5,5]],[6,6]])