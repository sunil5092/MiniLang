###############################################################
#                    MINI LANG — MEGA TEST                    #
#  Complete demonstration of all implemented features          #
###############################################################

print("=== MINI LANG MEGA TEST START ===")

###############################################################
# 1. VARIABLES + ARITHMETIC
###############################################################

print("\n[1] VARIABLES & ARITHMETIC TEST")

let a = 10
let b = 32
let c = a + b * 2

print("Expected 74 →")
print(c)
print("\n")

###############################################################
# 2. LISTS + MUTATION
###############################################################

print("\n[2] LISTS & MUTATION TEST")

let xs = [1, 2, 3]
print("Original list:")
print(xs)

xs[1] = 42
print("After mutation:")
print(xs)

let nested = [10, [20, 30], 40]
print("Nested list:")
print(nested)
print("\n")

###############################################################
# 3. STRING OPERATIONS
###############################################################

print("\n[3] STRING OPERATIONS TEST")

let msg = "hello world"
print(msg.upper())

print("ABC".lower())
print("\n")

###############################################################
# 4. DYNAMIC SCOPING
###############################################################

print("\n[4] DYNAMIC SCOPING TEST")

let x = 5

def show():
    print("show() sees →")
    print(x)

def change():
    let x = 777
    show()     # dynamic scoping → should use 777

change()
print("\n")

###############################################################
# 5. LAZY EVALUATION
###############################################################

print("\n[5] LAZY EVALUATION TEST")

def compute():
    print("compute() executed!")
    return 999

let lazyv = lazy ( compute() )

print("Lazy not evaluated yet.")
print("Force #1:")
print(force(lazyv))

print("Force #2 (no re-execution):")
print(force(lazyv))

let risky = lazy ( 10 / 0 )
print("Lazy risky created (no crash yet)")

try:
    print(force(risky))
except:
    print("Caught error from lazy!")
print("\n")

###############################################################
# 6. PATTERN MATCHING
###############################################################

print("\n[6] PATTERN MATCHING TESTS")

print("\n--- Tuple Match ---")
let t = (1, (2, (3, 4)))

match t:
    case (1, (2, (3, x))):
        print("Matched nested x =")
        print(x)
    case _:
        print("Tuple match failed")


print("\n--- List Match ---")
let ls = [5, 10, 20]

match ls:
    case [5, y, z]:
        print("List matched sum:")
        print(y + z)
    case _:
        print("List match failed")


print("\n--- Mixed Match ---")
let m = (10, [1, 2, 3])

match m:
    case (10, [a, b, _]):
        print("Mixed match a+b =")
        print(a + b)
    case _:
        print("Mixed match failed")
print("\n")

###############################################################
# 7. RECURSION — FACTORIAL
###############################################################

print("\n[7] RECURSION TEST (FACTORIAL)")

def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)

print("fact(6) =")
print(fact(6))    # Expect 720
print("\n")

###############################################################
# 8. TRY / EXCEPT — ERROR HANDLING
###############################################################

print("\n[8] EXCEPTION HANDLING TEST")

try:
    raise "boom!"
except:
    print("Recovered from exception!")
print("\n")

###############################################################
# 9. FULL INTEGRATION TEST — EVERYTHING COMBINED
###############################################################

print("\n[9] FULL INTEGRATION TEST")

let data = (10, [20, 30], fact(5))

match data:
    case (10, [a, b], lv):
        print("a + b =")
        print(a + b)
        print("factorial 5 =")
        print(fact(lv))
    case _:
        print("Integration match failed")
print("\n")

###############################################################
# END
###############################################################

print("\n=== MINI LANG MEGA TEST COMPLETE ===")
