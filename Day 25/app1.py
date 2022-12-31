lines = None
with open("Day 25\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

#dec to snafu
#snafu to dec

#dec is 1s 10s 100s 1000s
#snafu is 1s 5s 25s 125s

def snafu_to_dec(snafu):
    total = 0
    for i, v in enumerate(reversed(snafu)):
        worth = 5 ** i
        if v == "-": v = -1
        elif v == "=": v = -2
        else: v = int(v)
        total += (v * worth)
    return total

def dec_to_snafu(dec):
    snafu = ""
    while dec > 0:
        digit = dec % 5
        dec = dec // 5

        #weirdness here to handle = and - being -2 and -1
        if digit == 3:
            dec += 1
            snafu = "=" + snafu
        elif digit == 4:
            dec += 1
            snafu = "-" + snafu
        else:
            snafu = str(digit) + snafu
    return snafu

v = 0
for line in lines:
    v += snafu_to_dec(line)
print(dec_to_snafu(v))