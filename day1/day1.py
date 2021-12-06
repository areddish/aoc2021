with open("day1.txt", "rt") as file:
    data = [int(x) for x in file.readlines()]

    ans = 0
    for x in range(1,len(data)):
        if data[x] > data[x-1]:
            ans += 1
    print(f"Part 1: {ans}")

    ans = 0
    last = None    
    for x in range(2,len(data)):
        curr = data[x] + data[x-1] + data[x-2]
        if last and curr > last:
            ans += 1
        last = curr

    print(f"Part 2: {ans}")    