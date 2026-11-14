import copy, functools 
from collections import defaultdict

def add_item(x, bag=None):
    if bag is None:
        bag = []
    bag.append(x)
    return bag
    
print(add_item(10))  # [10]
print(add_item(20))  # [20]

my_list = [1, 2]
print(add_item(3, my_list))  # [1, 2, 3]
print(my_list)               # [1, 2, 3]

#-----

def group_by(pairs):
    g = defaultdict(list)
    for k,v in pairs:
        g[k].append(v)
    return dict(g)

pairs = [
    ("fruit", "apple"),
    ("fruit", "banana"),
    ("vegetable", "carrot"),
    ("fruit", "mango")
]

print(group_by(pairs))
# output: {
#    'fruit': ['apple', 'banana', 'mango'],
#   'vegetable': ['carrot']
#}

# -----

def chunks(seq, n):
    for i in range(0, len(seq),n):
        yield seq[i:i+n]
        
numbers = [1, 2, 3, 4, 5, 6, 7]

print(list(chunks(numbers, 3)))

# output: [[1, 2, 3], [4, 5, 6], [7]]

# ------

def counted(fn):
    @functools.wraps(fn)
    def wrap(*a, **k):
        wrap.calls +=1
        return fn(*a,**k)
    wrap.calls = 0
    return wrap
    
@counted
def greet(name):
    print("Hello", name)

greet("John")
greet("Alex")
greet("Sam")

print(greet.calls)

# output:
# Hello John
# Hello Alex
# Hello Sam
# 3

# ------
a = [[1, 2], [3]]
shallow, deep = copy.copy(a), copy.deepcopy(a)
a[0].append(99)       

print(a)
print(shallow)
print(deep)

# ------
'''
Note: 
2. group_by() — Grouping values by key
Explanation (2 lines):
- defaultdict(list) automatically creates an empty list whenever a new key appears.
- g[k].append(v) adds each value to its corresponding key, grouping duplicate keys together.

4. counted() — Decorators
Explanation (2 lines):
- A decorator wraps another function and adds functionality without modifying its original code.
- wrap.calls tracks how many times the decorated function has been called.

5. copy.copy() vs copy.deepcopy()
Explanation (2 lines):
- copy.copy() creates a shallow copy: the outer list is copied, but nested objects are shared.
- copy.deepcopy() creates an independent copy, including nested objects. (add the image next)

add_item()	Correctly avoids mutable defaults.
group_by()	Works with an empty iterable; returns {}.
chunks()	n=0 raises ValueError; ideally validate that n > 0.

yield returns a value one at a time from a function without ending the function permanently. It makes the function a generator.

Difference between return and yield
return	yield
Returns a value and ends the function.	Returns a value and pauses the function.
Cannot resume execution.	Resumes from where it paused.
Returns normally.	Creates a generator.

Remember: yield = Return a value + Pause + Resume later.
'''