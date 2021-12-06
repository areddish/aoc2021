
class BingoBoard:
    def __init__(self):
        self.board = []
        self.is_winner = False

    def add_row(self, rowStr):
        vals = filter(lambda x: x, rowStr.split(' '))
        nums = [[int(x), False] for x in vals]
        self.board.append(nums)

    def mark_value(self, val):
        #if self.is_winner:
         #   return

        for row in self.board:
            for col in row:
                if col[0] == val:
                    col[1] = True

        self.checkWin()

    def checkWin(self):
        cols = [True, True, True, True, True]
        for row in self.board:
            r = True
            for i, col in enumerate(row):
                r &= col[1]
                cols[i] &= col[1]
            if r:
                self.is_winner = True
                return
        for c in cols:
            if c:
                self.is_winner = True
                return

    def sumFalse(self):
        sum = 0
        for row in self.board:
            for col in row:
                if not col[1]:
                    sum += col[0]
        return sum

#with open("test.txt", "rt") as file:
with open("day4.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    # read nums
    nums = [int(x) for x in data[0].split(",")]
    boards = []
    for x in range(2, len(data), 6):
        board = BingoBoard()
        board.add_row(data[x])
        board.add_row(data[x+1])
        board.add_row(data[x+2])
        board.add_row(data[x+3])
        board.add_row(data[x+4])
        boards.append(board)

    first_winner = None
    winners = []
    for num in nums:
        # mark on all boards
        for board in boards:
            board.mark_value(num)
            if board.is_winner:
                skip = False
                for x in winners:
                    if board == x[0]:
                        skip = True

                if skip:
                    continue
                winners.append([board, num])
                if not first_winner:
                    print (f"part 1 = ", board.sumFalse() * num)
                    first_winner = True
            if len(winners) == len(boards):               
                val = winners[-1]
                print (f"part 2 = ", val[0].sumFalse() * val[1])

