from interpreter.core import MiniLang

def run_file(path):
    with open(path, "r") as f:
        MiniLang().run(f.read())

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py program.ml")
    else:
        run_file(sys.argv[1])
