# name tuple
from collections import namedtuple

def custom_divmod(x, y):
    DivMod = namedtuple("Divmod", "quotient remainder")
    div_mod = DivMod(*divmod(x,y))
    return div_mod
x_custom = custom_divmod(45,6)
print(x_custom.quotient)


# handling missing key in dict

x = {"pet":"Dog", "animal": "lion"}
# x["fruit"] ==> this will not work

x.setdefault("fruit", "grapes")
x.setdefault("fruit", "apple") # ==> find key if not  present then add in dict with given value
print(x)

# ordered dictionary
from collections import OrderedDict
a = OrderedDict()
a["hi"]="hello"
a["hi1"]="hello"
a["hi2"]="hello"
a["hi3"]="helloe"

print(a)

for key,val in a.items():
    print(key, val)
y = dict()
y["a"]="2"
y["b"]="2"
y["c"]="2"
y["d"]="2"
y["e"]="2"
y["f"]="2"
print(y)


for key,val in y.items():
    print(key, val)

# count letter in word

word  = "Deepak"

count_dict = {}
for i in word:

    if i  in count_dict:  
        count_dict[i]+=1

    else:

        count_dict[i]=1

print(count_dict)

from collections import Counter

counted_dcitionary = Counter(word)
print(counted_dcitionary)


from collections import ChainMap
numbers = {"one": 1, "two": 2}
letters = {"a": "A", "b": "B"}

gp_dict = ChainMap(numbers,letters)
print(gp_dict['a'], "gp_dict")


def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        print("hhjkljhbhjk")
        count += 1

# This doesn't execute the function body immediately
counter = count_up_to(5)  
print(next(counter), "counter")
print(counter.__next__())
print(next(counter))

class CountUpto:
    def __init__(self,max):
        self.max=max
    def __iter__(self):
        self.count=0
        return self
        # return self
    def __next__(self):
        self.count+=1
        if self.count > self.max:
            raise StopIteration
        return self.count
    




# counter = CountUpto(7)
for i in counter:
    print(i)
ls = [56,7,33]

multiply = tuple(map(lambda x: x*8, ls))

print(multiply)

# list comprehension
ls_comp = [x for x in multiply if x < 400]
dict_comp = {x:str(x) for x in multiply if x < 400}
print(dict_comp)


# zip function 
names = ['Alice', 'Bob']
scores = [85, 92, 78]

zipped = list(zip(names,scores))
names, scores =zip(*zipped) # * unpacking operator
print(names,scores)




x = {"pet":"Dog", "animal": "lion"}
y = {"pet1":"Dog", "animal1": "lion"}

print(list(zip(x,y)))

def gen():

    a = 0
    for i in range(7,90):
        yield i

a = gen()

print(a.__next__())
        


#  filter and redcue
scores = [85, 90, 88]
from functools import reduce
print(reduce(lambda x,y : x+y,scores))
print(list(filter(lambda x :x%5==0, scores)))


from itertools import zip_longest

names = ['Alice', 'Bob']
scores = [85, 92, 78]

for name, score in zip_longest(names, scores, fillvalue='N/A'):
    print(f"{name} scored {score}")



import asyncio 

async def intro():
    await  asyncio.sleep(2)
    return "task 1 completed"
x = asyncio.run(intro())
print(x)