############################################################
# Lists
############################################################

print("=== List Pattern Match ===")

let xs = [1, 5, 9]

match xs:
    case [1, a, b]:
        print("a + b =", a + b)
    case _:
        print("Not matched")
