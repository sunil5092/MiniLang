🌟 MiniLang – A Lightweight Programming Language in Python

A custom-designed experimental language featuring dynamic scoping, lazy evaluation, pattern matching, recursion, list mutation, exceptions, and more.

🚀 Features Overview

MiniLang is a small but powerful interpreter built in Python, designed for academic learning, language design exploration, and demonstration of modern programming-language concepts.

✨ Core Features
Feature	Supported	Description
Dynamic Scoping	✅	Variables are resolved at runtime from the caller environment
Lazy Evaluation	✅	Expressions can be delayed using lazy (expr) and executed with force()
Pattern Matching	✅	Supports tuple, list, wildcard, literals, variable binding
Recursion	✅	Full support through user-defined functions
List Mutation	✅	Indexed assignment like xs[1] = 42
Exception Handling	✅	try: / except: blocks
String Methods	✅	"abc".upper(), "XYZ".lower(), etc.
Functions	✅	User-defined functions via def name(args):
📂 Project Structure
MiniLang/
│
├── main.py                      # Entry point for running MiniLang programs
├── README.md                    # Project documentation
│
├── mini/
│   ├── interpreter/
│   │   ├── core.py             # Main interpreter logic (scopes, blocks, match, loops)
│   │   ├── evaluator.py        # Expression evaluator (lazy values, function calls)
│   │   ├── functions.py        # Function system with dynamic scoping
│   │   ├── errors.py           # Custom exceptions: MiniLangError, ReturnValue, LazyValue
│   │   └── __init__.py
│   │
│   └── tests/
│       ├── mega_test.ml        # Full project demonstration
│       ├── factorial.ml
│       ├── pattern.ml
│       ├── lazy.ml
│       ├── dynamic.ml
│       ├── list.ml
│       ├── errorhandling.ml
│       └── demo.ml
│
└── final_report.pdf            # IEEE-format academic report (if included)

🛠 Installation
1. Clone the Repo
git clone https://github.com/YOUR-USERNAME/MiniLang.git
cd MiniLang

2. Run Any MiniLang Program
python main.py mini/tests/mega_test.ml

🖥 Running Example Programs
Run Mega Test
python main.py mini/tests/mega_test.ml

Run Lazy Evaluation Test
python main.py mini/tests/lazy.ml

Run Pattern Match Test
python main.py mini/tests/pattern.ml

Run Recursion (Factorial)
python main.py mini/tests/factorial.ml

🧪 Example MiniLang Code
Function + Recursion
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)

print(fact(6))

Pattern Matching
let t = (1, (2, 3))

match t:
    case (1, (x, y)):
        print(x + y)
    case _:
        print("no match")

Lazy Evaluation
let x = lazy ( 10 / 0 )

try:
    print(force(x))
except:
    print("Error caught!")

📊 Screenshots / Output Demonstration

(Replace these placeholders with your actual screenshots)

▶ Interpreter Architecture

▶ Mega Test Output

▶ Pattern Matching

▶ Lazy Evaluation

🧩 Technical Highlights
🌀 Dynamic Scoping

Functions automatically inherit the caller’s environment.

💤 Lazy Evaluation

lazy (expr) creates a suspended computation evaluated ONLY when force(lazy_value) is called.

🎯 Pattern Matching

Supports:

literals

variables

tuple patterns

list patterns

wildcard _

🧱 Manual Block Parsing

Uses indentation-based parsing (Python-style) without external tools like Lark or ANTLR.

📚 Academic Contribution

This language demonstrates:

Alternative scoping models

Lazy semantics

Declarative pattern-based computation

Hand-built interpreter design

Error handling in domain-specific languages

It aligns with the Language Design & Implementation track.
