import heapq

#with open("test.txt", "rt") as file:
with open("day15.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    board = []
    for line in data:
        board.append([int(x) for x in line])
    
    w = len(board[0])
    h = len(board)

    def dijkstra_algorithm(start, board):
        w = len(board[0])
        h = len(board)

        visited = set()
        nodes = [(0, *start)]

        while nodes:
            cur_risk,x,y = heapq.heappop(nodes)

            if (x,y) in visited:
                continue
            visited.add((x,y))

            if x == w-1 and y == h-1:
                return cur_risk

            for offset in [(0,1), (1,0), (-1, 0), (0, -1)]:
                dx,dy = offset
                nx = x + dx
                ny = y + dy

                if 0 <= ny < h and 0 <= nx < w and (nx,ny) not in visited:
                    heapq.heappush(nodes, (cur_risk + board[ny][nx], nx,ny))

    risk = dijkstra_algorithm((0,0), board)
    print(f"Part 1 = {risk}")

    # expand board
    replicated_board = []
    for i in range(5):
        for row in board:
            new_row = []
            for j in range(5):
                for val in row:
                    new_val = (val + j + i) % 9
                    if new_val == 0:
                        new_val = 9
                    new_row.append(new_val)
            replicated_board.append(new_row)

    risk = dijkstra_algorithm((0,0), replicated_board)
    print(f"Part 2 = {risk}")


