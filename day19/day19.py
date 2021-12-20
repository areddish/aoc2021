from collections import defaultdict

#with open("test.txt", "rt") as file:
with open("day19.txt", "rt") as file:
   data = [x.strip() for x in file.readlines()]

   scanner_num = -1
   scanner_points = defaultdict(list)
   for line in data:
        if not line:
            scanner_num = -1
            continue

        if "scanner" in line:
            scanner_num = int(line.split("scanner ")[1].split(" ")[0])
            print("scanner: ", scanner_num)
        else:
            pts = [int(x) for x in line.split(",")]
            scanner_points[scanner_num].append(pts)

# print(scanner_points)