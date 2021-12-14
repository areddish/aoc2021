from collections import defaultdict

#with open("test.txt", "rt") as file:
with open("day14.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    polymer = data[0]

    rules = {}    
    for s in data[2:]:
        pair, ch = s.split(" -> ")
        rules[pair] = ch

    ######
    # Original brute force solution, too slow for part 2
    #
    # def run(polymer, rules, limit):
    #     step = 0
    #     while step < limit:
    #         new_polymer = polymer[0]
    #         for i in range(1, len(polymer)):
    #             insertion = rules.get(polymer[i-1:i+1], None)
    #             if insertion:
    #                 new_polymer += insertion
    #             new_polymer += polymer[i]

    #         #print(f"After step {step}, {new_polymer} ")
    #         polymer = new_polymer
    #         step += 1

    #     return polymer

    # new_polymer = run(polymer, rules, 10)
    # counts = defaultdict(int)
    # for ch in new_polymer:
    #     counts[ch] += 1
    # ans = max(counts.values()) - min(counts.values())
    # print(f"part 1 = {ans}")

    pair_counts = defaultdict(int)
    char_counts = defaultdict(int)
    for i in range(len(polymer)-1):
        pair_counts[polymer[i:i+2]] += 1
    
    for ch in polymer:
        char_counts[ch] += 1 

    for steps in range(40):
        prev_counts = pair_counts.copy()
        pair_counts = defaultdict(int)
        for pair in prev_counts:            
            # for each pair, spawn an equal amount of the character and track the new pairs created
            pair_count = prev_counts.get(pair, 0)
            pair_counts[pair[0]+rules[pair]] += pair_count
            pair_counts[rules[pair]+pair[1]] += pair_count
            # each pair spawn's a single character that we track separately to compute the answer
            char_counts[rules[pair]] += pair_count
        if steps == 9:
            count_values = char_counts.values()
            print(f"part 1 = {max(count_values) - min(count_values)}")
        # print(steps, char_counts)

    count_values = char_counts.values()
    print(f"part 2 = {max(count_values) - min(count_values)}")