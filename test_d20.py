import d20

res = d20.roll("1d20+2")
print(f"Type: {type(res)}")
print(f"Dir: {dir(res)}")
print(f"Result String: {res.result}")
print(f"Total: {res.total}")
# Check commonly used attributes
try:
    print(f"Crit: {res.crit}")
except Exception as e:
    print(f"No crit attr: {e}")

try:
    print(f"Fumble: {res.fumble}")
except Exception as e:
    print(f"No fumble attr: {e}")
    
# Inspect the expression tree to find the die
print(f"Expr: {res.expr}")
print(f"Expr Type: {type(res.expr)}")
print(f"Expr Dir: {dir(res.expr)}")
