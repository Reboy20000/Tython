import tokenize, io
import sys
def count_var(code, name):
    tokens = tokenize.generate_tokens(io.StringIO(code).readline)
    return sum(1 for t in tokens if t.type == tokenize.NAME and t.string == name)

def tython_to_python(line: str) -> str:
    line = line.strip()

    is_const = False
    if line.startswith("const "):
        is_const = True
        line = line[len("const "):].strip()

    # Expect: int: x = "10"
    type_part, rest = line.split(":", 1)
    var_part, value_part = rest.split("=", 1)

    var_name = var_part.strip()
    value = value_part.strip()

    # Strip quotes
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    t = type_part.strip()

    if t == "int":
        value = str(int(value))
    elif t == "float":
        value = str(float(value))
    elif t == "bool":
        if value.lower() == "true":
            value = "True"
        elif value.lower() == "false":
            value = "False"
        else:
            raise ValueError("Invalid boolean value")
    elif t == "str":
        value = f'"{value}"'
    return f"{var_name} = {value}"

if len(sys.argv) != 2:
    print("Usage: tyc <tython_file>")
    sys.exit(1)
tython_file = sys.argv[1]
with open(tython_file, "r") as f:
    lines = f.readlines()
    python_lines = []
    for line in lines:
        if line.strip() == "":
            python_lines.append("")
            continue
        python_line = tython_to_python(line)
        python_lines.append(python_line)
    python_code = "\n".join(python_lines)
    with open(tython_file.replace(".ty", ".py"), "w") as out_f:
        out_f.write(python_code)