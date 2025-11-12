def is_leap_year(year):
    if not year % 4 == 0:
        print("No leap year")
        return False
    elif not year % 100 == 0:
        print("Leap year1")
        return True
    elif year % 100 == 0 and year % 400 == 0:
        print("Leap year2")
        return True
    else:
        return False

# is_leap_year(2400)
# is_leap_year(1989)
print(is_leap_year(2000))
