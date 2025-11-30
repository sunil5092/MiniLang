############################################################
# Dynamic Scoping Test
############################################################

let x = 10

def print_x():
    print("print_x sees x =", x)

def level2():
    let x = 222
    print_x()   # should print 222

def level1():
    let x = 111
    level2()    # dynamic scoping → still 222

print("=== Dynamic Scoping Demo ===")
print_x()       # 10
level1()        # 222
print("")