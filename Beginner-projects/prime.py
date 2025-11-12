def is_prime(num):
    divisors = []
    for i in range(1, num + 1):
        print(i)
        if num % i == 0:
            divisors.append(i)
    
    if len(divisors) > 2:
        return False
    elif len(divisors) == 1:
        return False
    else:
        return True

print(is_prime(4))