import sys

def is_balanced(input_string):
    stack = ['Z']  # initialize stack with bottom symbol
    state = 'q0'
    print(f"Processing {input_string}")
    print(f"ID: ({state}, {input_string}, {''.join(stack[::-1])})")  # print stack as list

    for i, char in enumerate(input_string):
        remaining = input_string[i+1:] or 'E'
        top = stack[-1]

        match state: 
            case 'q0':
                if char == '!' and top == 'Z':
                    stack.append('!')
                    state = 'q1'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                else:
                    print(f"Invalid String. Failed at position {i+1}")
                    print(f"Remaining unprocessed input string: {remaining}")
                    return False

            case 'q1':
                if ((char == '<' and top == '!') or
                        (char == '{' and top == '!') or
                        (char == '(' and top == '!') or
                        (char == '[' and top == '!')):
                    stack.append(char) 
                    state = 'q2'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif char == 'x':
                    state = 'q1'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                else:
                    print(top)
                    print(f"Invalid String. Failed at position {i+1}")
                    print(f"Remaining unprocessed input string: {remaining}")
                    return False
            
            case 'q2':
                if ((char == '<' and top == '(') or
                        (char == '<' and top == '[') or
                        (char == '<' and top == '{') or
                        (char == '<' and top == '<') or
                        (char == '<' and top == '!') or ##ALL < POSSIBILITIES FRONT 
                        (char == '{' and top == '(') or
                        (char == '{' and top == '[') or
                        (char == '{' and top == '{') or
                        (char == '{' and top == '<') or
                        (char == '{' and top == '!') or ##ALL { POSSIBILITIES FRONT 
                        (char == '(' and top == '(') or
                        (char == '(' and top == '[') or
                        (char == '(' and top == '{') or
                        (char == '(' and top == '<') or
                        (char == '(' and top == '!') or ##ALL { POSSIBILITIES FRONT 
                        (char == '[' and top == '(') or
                        (char == '[' and top == '[') or
                        (char == '[' and top == '{') or
                        (char == '[' and top == '<') or
                        (char == '[' and top == '!')):
                        stack.append(char) 
                        state = 'q2'
                        print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif ((char == '>' and top == '<') or
                        (char == '}' and top == '{') or
                        (char == ')' and top == '(') or
                        (char == ']' and top == '[')):
                    stack.pop()  
                    state = 'q3'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif char == 'x':
                    state = 'q2'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                else:
                    print(f"Invalid String. Failed at position {i+1}")
                    print(f"Remaining unprocessed input string: {char}{remaining}")
                    return False

            case 'q3':
                if ((char == '>' and top == '<') or
                        (char == '}' and top == '{') or
                        (char == ')' and top == '(') or
                        (char == ']' and top == '[')):
                        stack.pop()  
                        state = 'q3'
                        print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif ((char == '<' and top == '(') or
                        (char == '<' and top == '[') or
                        (char == '<' and top == '{') or
                        (char == '<' and top == '<') or
                        (char == '<' and top == '!') or ##ALL < POSSIBILITIES FRONT 
                        (char == '{' and top == '(') or
                        (char == '{' and top == '[') or
                        (char == '{' and top == '{') or
                        (char == '{' and top == '<') or
                        (char == '{' and top == '!') or ##ALL { POSSIBILITIES FRONT 
                        (char == '(' and top == '(') or
                        (char == '(' and top == '[') or
                        (char == '(' and top == '{') or
                        (char == '(' and top == '<') or
                        (char == '(' and top == '!') or  ##ALL { POSSIBILITIES FRONT 
                        (char == '[' and top == '(') or
                        (char == '[' and top == '[') or
                        (char == '[' and top == '{') or
                        (char == '[' and top == '<') or
                        (char == '[' and top == '!')):
                        stack.append(char) 
                        state = 'q2'
                        print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif char == 'x':
                    state = 'q3'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                elif char == '!' and top == '!':
                    stack.pop()
                    state = 'q4'
                    print(f"ID: ({state}, {remaining}, {''.join(stack[::-1])})")
                    print(f"{state} is a final state.")
                    print(f"{input_string} is valid and has balanced brackets.\n")
                    return True
                else:
                    print(f"Invalid String. Failed at position {i+1}")
                    print(f"Remaining unprocessed input string: {remaining}")
                    return False

            case _:
                print("Rejected: unknown state")
                return False

    if state != 'q4':
        print(f"{state} is not a final state.")
        return False
    

def evaluate(s):
    content = s[1:-1]

    def process(tokens):
        res = ""
        while tokens:
            char = tokens.pop(0)
            if char == 'x':     # Adds x to result 
                res += 'x'
            elif char == '<':   # <S> -> SS
                inner = process(tokens)
                res += (inner + inner)
            elif char == '{':   # {S} ->Sx
                inner = process(tokens)
                res += (inner + 'x')
            elif char == '[':   # [S] -> empty
                process(tokens)
                res += ""
            elif char == '(':   # (xS) -> pop x, return S
                inner = process(tokens)
                if inner.startswith('x'):
                    res += inner[1:]
                else:
                    res += inner
            elif char in '>}])':
                return res
        return res
    
    final_string = process(list(content))
    return len(final_string)



def main1():
    """
    Reads input strings from input.txt and tests them using is_balanced().
    """
    try:
        with open("input.txt", "r") as file:
            lines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("input.txt not found.")
        return

    for line in lines:
        print("\n")
        is_balanced(line)

def main2():
    try:
        with open("input.txt", "r") as file:
            for line in file:
                s = line.strip()
                if not s: continue
                
                # is_balanced prints for main2
                original_stdout = sys.stdout
                sys.stdout = None
                valid = is_balanced(s)
                sys.stdout = original_stdout
                
                if valid:
                    print(f"{s} - Resulting number of x's: {evaluate(s)}")
                else:
                    print(f"{s} - Invalid string.")
    except FileNotFoundError: pass


if __name__ == "__main__":
    main1()
    main2()