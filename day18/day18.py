import ast

# TODO: move this to the node class
# Should recombine these two like before.
def dfs_val_greater_than_10(node):
   assert isinstance(node, Node)
   result = None   
   if isinstance(node.left, Node):
      result = dfs_val_greater_than_10(node.left)
   elif node.left >= 10:
      result = node

   if result:
      return result

   result = None
   if isinstance(node.right, Node):
      result = dfs_val_greater_than_10(node.right)
   elif node.right >= 10:
      result = node

   return result

# TODO: move this to the node class
def dfs(node, level = 0):
   assert isinstance(node, Node)

   if level == 3:
      if isinstance(node.left, Node):
         node.left.explode()
         return True
      elif isinstance(node.right, Node):
         node.right.explode()
         return True

   result = False
   if isinstance(node.left, Node):
      result = dfs(node.left, level + 1)
   if result:
      return result

   if isinstance(node.right, Node):
      return dfs(node.right, level + 1)

   return False

# TODO: move this to the node class
def right_most(node, val):
   assert isinstance(node, Node)
   if not isinstance(node.right, Node):
      node.right += val
      return True

   return right_most(node.right, val)

# TODO: move this to the node class
def left_most(node, val):
   assert isinstance(node, Node)
   if not isinstance(node.left, Node):
      node.left += val
      return True

   return left_most(node.left, val)
   
class Node:
   def __init__(self, left, right, parent=None):
      self.left = left
      self.right = right
      self.parent = parent

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
         #print("BEFORE:", self.print())
         actioned = dfs(self, 0)
         if not actioned:
            node_to_split = dfs_val_greater_than_10(self)
            if node_to_split:
               Node.split(node_to_split, node_to_split.left_val() >= 10)
               actioned = True
         #print("AFTER:",self.print())

         # This is just for testing so I can run a single iteration and examine the output
         if run_once:
            return

   def explode(self):
      #print("explode", self.left, self.right)
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

      # Replace the node with 0
      if self.parent:
         if self.parent.left == self:
            #print ("zero'ing left")
            self.parent.left = 0
         else:
            assert self.parent.right == self
            #print("zero'ing right")
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
      # assert node1.parent == None
      # assert node2.parent == None

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

with open("day18.txt", "rt") as file:
   data = [x.strip() for x in file.readlines()]

   fish = Node.node_from_str(data[0])
   for line in data[1:]:
      #print(" ", fish.print())
      next_fish = Node.node_from_str(line)
      #print("+",next_fish.print())
      fish = Node.add(fish, next_fish)
      #print("=", fish.print())
      #print() 
   print(fish.print())
   print(f"Part 1 = {fish.magnitude()}")

# Part 2, only 100 lines, brute force for the win...
largest_pair_magnitude = 0
for i in range(len(data)-1):
   for j in range(i, len(data)):
      f1 = Node.node_from_str(data[i])
      f2 = Node.node_from_str(data[j])
      m1 = Node.add(f1, f2).magnitude()
      m2 = Node.add(f2, f1).magnitude()
      largest_pair_magnitude = max(largest_pair_magnitude, m1, m2)

print(f"Part 2 = {largest_pair_magnitude}")


## Below here are tests that can be run when making changes to verify nothing is regressing
exit(1)
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
