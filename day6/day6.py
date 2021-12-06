# example
# fishes = [3,4,3,1,2]

with open('day6.txt', "rt") as file:
    data = file.readlines()
    fishes = [int(x) for x in data[0].split(',')]
    
memo = {}
def fishes_in_days(start, days):
    if (start, days) in memo:
        return memo[(start , days)]

    if days < start:
        return 0

    # We create one fish now, then start creating more in 6 days, and the fish we created
    # will create more in 8 days.
    next_start = days - start - 1
    fish_count = 1 + fishes_in_days(6, next_start) + fishes_in_days(8, next_start)
    memo[(start, days)] = fish_count
    return fish_count

parts = [80, 256]
for part in range(len(parts)):
    days = parts[part]
    sum = len(fishes)     
    for x in fishes:
        sum += fishes_in_days(x,days - 1)

    print (f"Part {part+1} = {sum}")