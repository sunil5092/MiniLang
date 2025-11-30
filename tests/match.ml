print("=== MATCH LIST ===")

let xs = [1, 10, 20]

match xs:
    case [1, y, z]:
        print("Matched list sum:")
        print(y + z)
    case _:
        print("List match failed")
