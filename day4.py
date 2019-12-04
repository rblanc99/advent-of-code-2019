def isOk(number) :
    if len(str(number)) != 6 :
        return False
    if number > 785961 or number < 271973 :
        return False
    adjacent_digits = False
    is_order_correct = True
    digits = [int(n) for n in str(number)]
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1] :
            adjacent_digits = True
        if digits[i+1] < digits[i] :
            is_order_correct = False
    if (not adjacent_digits) or (not is_order_correct) :
        return False
    return True

def isOk2(number) :
    if len(str(number)) != 6 :
        return False
    if number > 785961 or number < 271973 :
        return False
    are_digits_adjacent = False
    adjacent_digits = []
    is_order_correct = True
    digits = [int(n) for n in str(number)]
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1] :
            are_digits_adjacent = True
            adjacent_digits.append(digits[i])
        if digits[i+1] < digits[i] :
            is_order_correct = False
    if (not are_digits_adjacent) or (not is_order_correct) :
        return False
    while len(adjacent_digits) > 0 :
        x = adjacent_digits[0]
        adjacent_digits.remove(x)
        if x not in adjacent_digits :
            return True
        while x in adjacent_digits :
            adjacent_digits.remove(x)
    return False


count = 0
for x in range(271973,785961) :
    if isOk(x):
        count+=1

print(count)

count2 = 0
for x in range(271973,785961) :
    if isOk2(x):
        count2+=1

print(count2)




