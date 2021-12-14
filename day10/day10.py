OPEN = list("{[(<")
CLOSE = list("}])>")
def validate(str):
    closing = {
        '(' : ')',
        '{' : '}',
        '[' : ']',
        '<' : '>'
    }
    missing = []
    for ch in str:
        if ch in OPEN:
            missing.append(closing[ch])
        elif ch in CLOSE:
            close = missing.pop()
            if close != ch:
                return ch
        else:
            assert "huh?"
    return missing

#with open("test.txt", "rt") as file:
with open("day10.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]
    pts = {
        ")": 3 ,
        "]": 57 ,
        "}": 1197 ,
        ">": 25137
    }

    corrupt = []
    incomplete = []
    sum = 0
    for line in data:
        result = validate(line)
        if isinstance(result, list):
            incomplete.append(result)
            #print(line, result)
        else:
            corrupt.append(line)
            sum += pts[result]

    print (f"part 1 = {sum}")


    scores = []
    pts = {
        ")": 1 ,
        "]": 2 ,
        "}": 3 ,
        ">": 4
    }
    for line in incomplete:
        score = 0
        for ch in line[::-1]:
            score *= 5
            score += pts[ch]
        scores.append(score)
    scores.sort()
    #print(scores)
    print (f"part 2 = {scores[len(scores)//2]}")

exit(1)
print(validate("()"))
print(validate("{}"))
print(validate("{}"))
for x in ["([])", "{()()()}", "<([{}])>", "[<>({}){}[([])<>]]", "(((((((((())))))))))"]:
    assert validate(x)