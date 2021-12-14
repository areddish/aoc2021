from PIL import Image
import random

#with open("test.txt", "rt") as file:
with open("day9.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]
    grid = []
    for row in data:
        grid.append([int(x) for x in list(row)])
    w = len(grid[0])
    h = len(grid)

    x,y = 0,0
    lows = []
    for y in range(h):
        for x in range(w):
            neighbors = []
            for offset in [(-1,0), (1,0), (0,-1), (0, 1)]:
                dx,dy = offset
                nx = x + dx
                ny = y + dy
                if ny < 0 or ny >= h:
                    continue
                if nx < 0 or nx >= w:
                    continue
                neighbors.append(grid[ny][nx])
            if min(neighbors) > grid[y][x]:
                lows.append((x,y,grid[y][x]))

    ans = 0
    for x in lows:
        ans += x[2] + 1
    print(f"part 1 = {ans}")

    def grow_out(grid, x,y, s=set()):
        val = grid[y][x]
        s.add((x,y,val))
        #print(x,y,val)
        sum = 0
        for offset in [(-1,0), (1,0), (0,-1), (0, 1)]:
            dx,dy = offset
            nx = x + dx
            ny = y + dy
            if ny < 0 or ny >= h:
                continue
            if nx < 0 or nx >= w:
                continue
            if grid[ny][nx] > val and grid[ny][nx] != 9:
                #s.add((nx,ny))
                grow_out(grid, nx, ny, s)

        return s

    def print_basin(w, h, pts):
        for y in range(h):
            for x in range(w):
                if (x,y) in pts:
                    print ("X", end="")
                else:
                    print (".", end="")
        print()

    def render_block(img, x, y, v, size=10):
        for dy in range(size):
            for dx in range(size):
                #img.putpixel((x+dx, y+dy), (0,255-(v*10),0))
                img.putpixel((x+dx, y+dy),(97-(v*5),73 - (v*2),34- (v*2)))

    def render_lava(img, x, y, size=10):
        for dy in range(size):
            for dx in range(size):
                #img.putpixel((x+dx, y+dy), (0,255-(v*10),0))
                img.putpixel((x+dx, y+dy),(136 - random.randint(20,40), 0, 21 - random.randint(0,6)))

    def render_basin(img, w, h, pts):
        for y in range(h):
            for x in range(w):
                for v in range(9):
                    if (x,y,v) in pts:
                        render_block(img, x*10, y*10, v)

    basins = []
    img = Image.new("RGBA", (w*10,h*10), (136, 0, 21))
    for data in lows:
        x,y,_ = data
        pts = grow_out(grid,x,y,set())
        render_basin(img,w,h,pts)
        basins.append(len(pts))
    img.show()

    basins.sort()
    ans = 1
    for x in basins[-3:]:
        ans *= x
    print(f"part 2 = {ans}")