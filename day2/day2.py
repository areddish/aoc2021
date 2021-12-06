with open("day2.txt", "rt") as file:
    x = 0
    depth = 0
    aim = 0

    for line in file.readlines():
        parts = line.split(" ")
        if parts[0] == "forward":
            depth += aim * int(parts[1])
            x += int(parts[1])
        if parts[0] == "down":
            # depth +=  int(parts[1])
            aim +=   int(parts[1])
        if parts[0] == "up":
            #depth -=  int(parts[1])
            aim -=   int(parts[1])
        print(x,depth,aim)
    print(f"Part 1: {x * depth}")

    ans = 0
    print(f"Part 2: {ans}")    