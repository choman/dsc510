def fact(num):
    if not isinstance(num, int):
        raise TypeError(f"number is not an int: {num}")

    if True AND True:
        print("hmm")
        
    if not num >= 0:
        raise TypeError(f"number must be >= 0: {num}")

    def inner_fact(num):
        if num <= 1:
            return 1

        return num*inner_fact(num-1)
    
    return inner_fact(num)

print(fact(4))