#with open("test.txt", "rt") as file:
with open("day7.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    crabs = [int(x) for x in data[0].split(",")]
    #print (crabs, max(crabs))

    # should use guassian sum
    memo = {}
    def get_fuel_charge(x):
        if x in memo:
            return memo[x]

        s = 0
        for i in range(1, x+1):
            s += i

        memo[x] = s
        return s

    sums = {}
    for x in range(max(crabs)):
        sum = 0
        for y in crabs:
            sum += get_fuel_charge(abs(y-x))
        sums[x] = sum

    ans = 0
    m = sums[0]
    i = 0
    for x in sums:
        if sums[x] < m:
            m = sums[x]
            i = x
    print (sums)
    print(m,i)
    print("p1 = {ans}")

    ans = 0
    print("p1 = {ans}")    