import math_operation
from math_operation import subtract
from algebra import square, cube

var1 = 1
var2 = 2
b = math_operation.add(var1,var2)
print(f"{math_operation.add.__module__}.{math_operation.add.__name__}  ....: {var1} + {var2} = {b}")


var1 = 7
var2 = 3
c = subtract(var1,var2)
print(f"{subtract.__module__}.{subtract.__name__}  ....: {var1} - {var2} = {c}")

var1 = 4
var2 = 2
c = square(var1,var2)
print(f"{square.__module__}.{square.__name__}  ....: {var1} ^ {var2} = {c}")


var1 = 2
var2 = 3
c = cube(var1,var2)
print(f"{cube.__module__}.{cube.__name__}  ....: {var1} ** {var2} = {c}")

quit()
