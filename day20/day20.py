# In the test case the algo[0] is . so the infinite space is always a .
# However in the actual test case alg[0] is # and then algo[511] is .
# so it alternates between filling the infinite space . or #, we pass
# this value in via the default param and calculate it based on which
# iteration we are on.
def get_kernel_set(s, x, y, w, h, default):
    str = ""
    for dy in [-1, 0, 1]:    
        for dx in [-1, 0, 1]:
            if 0 <= x+dx < w and 0 <= y+dy < h:
                if (x+dx, y+dy) in s:
                    str += "1"
                else:
                    str += "0"
            else:
                str += default                    
    return int(str, 2)

def print_image(s, w, h):
    for y in range(h):
        for x in range(w):
            if (x,y) in s:
                print("#",end="")
            else:
                print(".",end="")
        print()

def print_answer(lights, w, h, part):
    ans = 0
    for y in range(0, h):
        for x in range(0, w):
            if (x,y) in lights:
                ans += 1

    print(f"Part {part} = {ans}")

#with open("test.txt", "rt") as file:
with open("day20.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    algo = data[0]

    light_nums = {}
    for i in range(len(algo)):
        if algo[i] == "#":
            light_nums[i] = True

    iters = 50
    border = 6 * iters
    image = []
    for line in data[2:]:
        image.append(list(line))

    lights = set()
    for y in range(len(image)):
        for x in range(len(image[0])):
            if image[y][x] == "#":
                lights.add((x+border,y+border))

    w = len(image[0]) + border*2
    h = len(image) + border*2

    for i in range(1,1+iters):
        new_lights = set()
        for y in range(h):
            for x in range(w):
                index = get_kernel_set(lights, x, y, w, h, "0" if i % 2 == 1 else "1")
                if index in light_nums:
                    new_lights.add((x,y))
        lights = new_lights

        #print_image(lights, w, h)
        if i == 2:
            print_answer(lights, w, h, "1")

    print_answer(lights, w, h, "2")