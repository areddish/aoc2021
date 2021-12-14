#with open("test.txt", "rt") as file:
with open("day8.txt", "rt") as file:
    pre = []
    post = []
    for line in file.readlines():
        parts = line.split("|")
        pre.append([(x,len(x)) for x in parts[0].strip().split(" ")])
        post.append([(x,len(x)) for x in parts[1].strip().split(" ")])

    count = 0
    for post_line in post:
        for digit in post_line:
            if digit[1] in [2,4,3,7]:
                count += 1
    print(f"part 1 = {count}")

    def determine_digit_pattern(digits):
        pattern = {}
        size = {}
        one, four, eight = None, None, None
        for pair in digits:
            digit = pair[0]
            length = pair[1]

            # sort the connections so we don't have to worry about order
            sorted_pattern = "".join(sorted(digit))

            if length == 2:
                one = set(digit)
                pattern[sorted_pattern] = 1
            elif length == 4:
                four = set(digit)
                pattern[sorted_pattern] = 4    
            elif length == 3:
                pattern[sorted_pattern] = 7                
            elif length == 7:                
                eight = set(digit)
                pattern[sorted_pattern] = 8
            else:
                if not length in size:
                    size[length] = []
                size[len(digit)].append(sorted_pattern)

        # 8 - 6 should be in 1
        # 8 - 0 should not be in 1
        # 8 - 9 should not be in 1
        # 0, 6, 9
        assert len(size[6]) == 3
        for digit in size[6]:
            eight_diff = eight.difference(set(digit))
            if eight_diff.issubset(one):
                pattern[digit] = 6
            else:
                if eight_diff.issubset(four):
                    pattern[digit] = 0
                else:
                    pattern[digit] = 9

        # 2, 3, 5
        assert len(size[5]) == 3
        for digit in size[5]:
            if len(set(digit).difference(one)) == 3:
                pattern[digit] = 3
            else:
                if len(set(digit).difference(four)) == 2:
                    pattern[digit] = 5
                else:
                    pattern[digit] = 2
        return pattern

    def get_digit_value(pattern, digits):
        val = 0
        for d in digits:
            val = val * 10 + pattern["".join(sorted(d[0]))]
        return val

    assert(len(pre) == len(post))
    sum = 0
    for i in range(len(pre)):
        digit_pattern = determine_digit_pattern(pre[i])
        v = get_digit_value(digit_pattern, post[i])
        sum += v
    print(f"part 2 = {sum}")
