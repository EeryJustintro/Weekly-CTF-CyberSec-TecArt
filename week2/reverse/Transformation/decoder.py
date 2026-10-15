for i in range(0, len(enc)):
    currentChar = enc[i]
    
    currentCharNum = ord(currentChar)

    firstCharNum  = currentCharNum >> 8
    secondCharNum = currentCharNum & 0xFF
    
    joinedList.append(chr(firstCharNum))
    joinedList.append(chr(secondCharNum))

flag = ''.join(joinedList)
print(flag)
