# This must be outseide the package folder.

# from math_package import arithmetic as arith
from math_package.arithmetic import add, subtract
from math_package.algebra import square, cube

import math_package

print(add(10, 5))  # Output: 15
print(square(4,2))   # Output: 16
print(cube(2,3))     # Output: 27
print(subtract(10, 5))  # Output: 5

print(f" SQUARE from math_package.....: {math_package.algebra.square(3,2)}")   # Output: 16
quit()