if __name__ == "__main__":
    with open("test.txt", "rt") as file:
    #with open("day17.txt", "rt") as file:
        data = [x.strip() for x in file.readlines()]
        assert len(data) == 1
        _, _, x, y = data[0].split(' ')
        print(x,y)
        x.split("..")

    x_range=[20,30]
    y_range=[-10,-5]

#nput
    x_range=[96,125]
    y_range=[-144,-98]

    x,y = 0,0

    def sim(x_range, y_range, x_vel, y_vel):
        x,y = 0,0
        max_y = 0
        while True:
           # print(x,y)
            x += x_vel
            y += y_vel
            if y > max_y:
                max_y = y
            if x_vel > 0:
                x_vel -= 1
            elif x_vel < 0:
                x_vel += 1
            y_vel -= 1

            if y_range[0] <= y <= y_range[1]:
                if x_range[0] <= x <= x_range[1]:
                    #print ("success")
                    return True, max_y
            if y < y_range[1]*5:
                #print("fail1",x,y)
                return False, max_y
            if x > x_range[1]*5:
                #print("fail2",x,y)
                return False, max_y

    
    results = []
    print(x_range[1]-x_range[0])
    print(abs(y_range[0]-y_range[1]), -98, -1)
    for x_vel in range(-50,54*(x_range[1]-x_range[0])):
        for y_vel in range(265, -398, -1):
            result, y = sim(x_range, y_range, x_vel, y_vel)
            if result:
                results.append({ "xv": x_vel, "yv": y_vel, "max": y})

    sorted(results, key=lambda x: x["max"])
    print(f"Part 1 = {results[0]}")
    print(f"Part 2 = {len(results)}")

    #print(sim((0,0), x_range, y_range, 7, 2))
    #print(sim((0,0), x_range, y_range, 6, 9))
    #print(sim((0,0), x_range, y_range, 9, 0))
    #print(sim((0,0), x_range, y_range, 17, -4))

