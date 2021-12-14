def fold_up(board, n):
    temp_board = []

    for j in range(n):
        folded_j = len(board) - j - 1
        row = []
        for i in range(len(board[0])):
            folded = board[folded_j][i]
            existing = board[j][i]
            if existing == folded:
                row.append(existing)
            elif existing == "#" or folded == "#":
                row.append("#")
            else:
                row.append(".")
        temp_board.append(row)

    return temp_board

def fold_left(board, n):
    temp_board = []

    # establish current
    for j in range(len(board)):
        row = []
        for i in range(n):
            folded_i = len(board[0]) - i - 1
            #print(i, len(board[0]) - i - 1)            
            folded = board[j][folded_i]
            existing = board[j][i]
            if existing == folded:
                row.append(existing)
            elif existing == "#" or folded == "#":
                row.append("#")
            else:
                row.append(".")
        temp_board.append(row)

    return temp_board

def print_b(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            print(board[y][x], end="")
        print()

#with open("test.txt", "rt") as file:
with open("day13.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    points = set()
    pts = True
    max_x = 0
    max_y = 0

    index = 0
    for line in data:
        index += 1
        if not line:
            break
        pt = tuple([int(x) for x in line.split(",")])
        points.add(pt)
        max_x = max(max_x, pt[0])
        max_y = max(max_y, pt[1])

    board =[]
    for y in range(max_y+1):
        row = []
        for x in range(max_x+1):
            row.append("#" if (x,y) in points else ".")
        board.append(row)

    part_1 = None
    for i in range(index, len(data)):
        val = int(data[i].split("=")[1])
        if "x=" in data[i]:
            board = fold_left(board, val)
        else:
            assert "y=" in data[i]
            board = fold_up(board, val)
        
        if not part_1:
            part_1 = True
            ans = 0
            for r in board:
                for c in r:
                    ans += (1 if c == "#" else 0)
            print (f"part 1 = {ans}")

    print (f"part 2 = ")
    print_b(board)



# could be faster by just transposing the points then graphing.