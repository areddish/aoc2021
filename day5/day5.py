#with open("test.txt", "rt") as file:
with open("day5.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    lines = []
    w = 0
    h = 0
    for line in data:
        l = []
        for pair in line.split(" -> "):
            coords = [int(x) for x in pair.split(",")]
            l.append(coords)            
            w = max(w, coords[0])
            h = max(h, coords[1])
        lines.append(l)

    w+=1
    h+=1
    print(w,h)

    board = []
    for y in range(h):
        row = []
        for x in range(w):
            row.append(0)
        board.append(row)

    def draw_horiz_line(board, pair):
        assert pair[0][1] == pair[1][1]
        step = -1 if pair[0][0] > pair[1][0] else 1
        for x in range(pair[0][0], pair[1][0]+step, step):
            board[pair[0][1]][x] += 1

    def draw_vert_line(board, pair):
        assert pair[0][0] == pair[1][0]
        step = -1 if pair[0][1] > pair[1][1] else 1
        for y in range(pair[0][1], pair[1][1]+step, step):
            board[y][pair[0][0]] += 1

    def draw_diag_line(board, pair):
        stepy = -1 if pair[0][1] > pair[1][1] else 1
        stepx = -1 if pair[0][0] > pair[1][0] else 1
        x = pair[0][0]
        for y in range(pair[0][1], pair[1][1]+stepy, stepy):
            board[y][x] += 1
            x += stepx

    def draw_line(board, pair):
        if isVertOrHoriz(pair):
            if pair[0][0] == pair[1][0]:
                draw_vert_line(board, pair)
            else:
                draw_horiz_line(board, pair)
        else:
            draw_diag_line(board, pair)
    
    def isVertOrHoriz(line):
        return line[0][0] == line[1][0] or line[0][1] == line[1][1]

    board_part2 = [row.copy() for row in board]
    for line in lines:
        if isVertOrHoriz(line):
            draw_line(board, line)
        draw_line(board_part2, line)

    # print board
    # for y in range(h):
    #     for x in range(w):
    #         print(board[y][x], end="")
    #     print()

    sum = 0
    sum_part2 = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] >= 2:
                sum += 1
            if board_part2[y][x] >= 2:
                sum_part2 += 1
    print(f"p1 = {sum}")
    print(f"p2 = {sum_part2}")
