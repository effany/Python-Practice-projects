
with open("file1.txt") as file:
    file1 = file.readlines()
    file1_num = [int(num) for num in file1]
    print(file1_num)

with open("file2.txt") as file:
    file2 = file.readlines()
    file2_num = [int(num) for num in file2]
    print(file2_num)

result = [x for x in file1_num if x in file2_num]

print(result)