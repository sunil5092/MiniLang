############################################################
# Advanced Lazy Evaluation
############################################################

print("=== Lazy Evaluation Test ===")

def heavy():
    print("heavy() executed!")
    return 999

let lv = lazy ( heavy() )

print("Before forcing lv")
print(lv)

print("Force1:")
print(force(lv))

print("Force2 (cached):")
print(force(lv))

# Laziness prevents errors
let risky = lazy ( 10 / 0 )

print("risky created (no crash)")
try:
    print(force(risky))
except:
    print("Caught divide-by-zero lazily!")

# Nested lazy
let deep = lazy ( lazy ( lazy (5 + 5) ) )
print("Nested lazy result:")
print(force(force(force(deep))))
