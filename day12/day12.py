from collections import defaultdict

graph = defaultdict(set)

#with open("test.txt", "rt") as file:
#with open("test2.txt", "rt") as file:
with open("day12.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]
    for line in data:
        parts = line.split("-")
        graph[parts[0]].add(parts[1])
        graph[parts[1]].add(parts[0])

    print(graph)


# def find_path(graph, node_start, touched_small_cave=False, visited):
#     print(node_start)
#     cur = graph[node_start]
#     path = 0 
#     for node in cur:
#         if node == "start":
#             continue

#         if node == "end":
#             path += 1
#             continue

#         if node.lower() == node:
#             if touched_small_cave:
#                 continue

#         path += find_path(graph, node, node.lower() == node)
            
#     return path
    
def any2(dict):
    for x in dict:
        if dict[x] >= 2:
            return True
    return False

def find_path2(graph, start, small_caves_visited):
    paths = set()
    destinations = graph[start]
    current_path = start
    for node in destinations:
        iteration_small_cavs_visited = small_caves_visited.copy()
        if node == "start":
            continue

        if node == "end":
            #print("FOUND:", current_path+","+node)
            paths.add(current_path+","+node)
            continue

        if node.lower() == node:
            visit = small_caves_visited[node]
            if visit >= 2 or (visit == 1 and any2(iteration_small_cavs_visited)):
                continue
            iteration_small_cavs_visited[node] += 1

        for p in find_path2(graph, node, iteration_small_cavs_visited):
            paths.add(current_path+","+p)
            
    return paths

paths = find_path2(graph,'start', defaultdict(int))
# for p in sorted(paths):
#     print(p)
print(f"Answer = {len(paths)}")
