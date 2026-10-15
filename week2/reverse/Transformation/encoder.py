flag = "unknown_"
joinedList = []

# flag = ''.join([chr(ord(c) >> 8) + chr(ord(c) & 0xFF) for c in enc])

for i in range(0, len(flag), 2):
    currentChar = flag[i]
    nextChar = flag[i+1]

    currentCharNum = ord(currentChar)
    nextCharNum = ord(nextChar)

    currentCharNumBitShift = currentCharNum << 8 # or times 256

    joinedList.append(chr(currentCharNumBitShift + nextCharNum))

encrypted = ''.join(joinedList)
print(encrypted)
