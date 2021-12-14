#with open("test.txt", "rt") as file:
with open("day11.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]
    board = []
    for line in data:
        board.append([int(x) for x in line.strip()])

    w = 10
    h = 10

    assert len(board[0]) == w
    assert len(board) == h

    def flash(board, x, y, flashed, w=10, h=10):
        flash_Count = 1
        flashed.add((x,y))
        for offset in [(-1,0), (1,0), (0,-1), (0, 1), (-1,1), (1,-1), (-1, -1), (1,1)]:
            dx,dy = offset
            nx = x + dx
            ny = y + dy
            if (nx,ny) in flashed:
                continue  
            if ny < 0 or ny >= h:
                continue
            if nx < 0 or nx >= w:
                continue

            board[ny][nx] += 1
            if board[ny][nx] > 9:
                flash_Count += flash(board, nx, ny, flashed)

        return flash_Count

    def print_board(board,w=10,h=10):
        for y in range(h):
            for x in range(w):
                print(board[y][x] if board[y][x] != 0 else "*",end="")
            print()

    flashes = 0
    step = 0
    while True:        
        flashed = set()
        for y in range(h):
            for x in range(w):
                if (x,y) in flashed:
                    continue

                board[y][x] += 1
                if board[y][x] > 9:
                    # flash
                    #print(f"Flashing {x}{y}")
                    flashes += flash(board, x, y, flashed)

        if len(flashed) == w * h:
            print(f"Part 2 = {step + 1}")
            exit(1)
        for pt in flashed:
            board[pt[1]][pt[0]] = 0

        if step == 99:
            print(f"Part 1 = {flashes}")


        #print(f"Step {step + 1}")
        step += 1
        #print_board(board)
        #print()

    