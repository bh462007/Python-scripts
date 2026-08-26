def count_num(max_value):
    count=1
    while count<=max_value:
        yield count
        count+=1

my_count=count_num(4)
print(next(my_count))
print(next(my_count))