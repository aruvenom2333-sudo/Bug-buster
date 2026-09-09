import re

def analyze_complexity(code_string):
    """
    The brain of the analyzer.
    Detects loops, recursion, and estimates Time Complexity.
    """
    lines = code_string.split('\n')
    
    max_loop_depth = 0
    is_recursive = False
    function_name = None
    recursive_call_count = 0

    # Step 1: Find the function name
    for line in lines:
        match = re.search(r'def\s+(\w+)\s*\(', line)
        if match:
            function_name = match.group(1)
            break

    # Step 2: Analyze each line for loops and recursion
    for line in lines:
        stripped = line.strip()
        
        # Count indentation (assuming 4 spaces per level)
        indentation = len(line) - len(line.lstrip(' '))
        current_depth = indentation // 4
        
        # Detect loops (for / while)
        if stripped.startswith('for ') or stripped.startswith('while '):
            if current_depth > max_loop_depth:
                max_loop_depth = current_depth
        
        # Detect recursion (only inside the function body)
        if function_name and indentation > 0:
            # Count how many times the function calls itself
            if function_name in line and 'def ' not in line:
                is_recursive = True
                # Count occurrences of the function name in this line
                recursive_call_count += line.count(function_name)

    # Step 3: Determine the final complexity
    if is_recursive:
        # If it calls itself twice (like fib(n-1)+fib(n-2)) -> Exponential
        if recursive_call_count >= 2:
            complexity = "O(2^n) - Exponential (Double Recursion detected)"
        else:
            complexity = "O(n) - Linear Recursion (Single call detected)"
    elif max_loop_depth == 0:
        complexity = "O(1) - Constant (No loops found)"
    elif max_loop_depth == 1:
        complexity = "O(n) - Linear (Single loop)"
    elif max_loop_depth == 2:
        complexity = "O(n²) - Quadratic (Nested loops)"
    else:
        complexity = f"O(n^{max_loop_depth}) - Highly nested loops"

    return complexity, max_loop_depth, is_recursive, recursive_call_count


# ============================================
# TEST YOUR CODE (Run this file)
# ============================================
if __name__ == "__main__":
    
    print("=" * 50)
    print("DSA DEBUGGER - LEVEL 1 (Terminal Version)")
    print("=" * 50)
    print()

    # Test 1: Simple Loop - O(n)
    code1 = """
def print_numbers(n):
    for i in range(n):
        print(i)
"""
    result, depth, rec, count = analyze_complexity(code1)
    print(f"Test 1 (Single Loop):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 2: Nested Loop - O(n²)
    code2 = """
def print_pairs(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
"""
    result, depth, rec, count = analyze_complexity(code2)
    print(f"Test 2 (Nested Loop):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 3: Recursive Fibonacci - O(2^n)
    code3 = """
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
"""
    result, depth, rec, count = analyze_complexity(code3)
    print(f"Test 3 (Fibonacci):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 4: Factorial (Linear Recursion) - O(n)
    code4 = """
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n-1)
"""
    result, depth, rec, count = analyze_complexity(code4)
    print(f"Test 4 (Factorial):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 5: Triple Nested Loop - O(n³)
    code5 = """
def triple_loop(n):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                print(i, j, k)
"""
    result, depth, rec, count = analyze_complexity(code5)
    print(f"Test 5 (Triple Nested Loop):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 6: While Loop - O(n)
    code6 = """
def while_loop(n):
    i = 0
    while i < n:
        print(i)
        i += 1
"""
    result, depth, rec, count = analyze_complexity(code6)
    print(f"Test 6 (While Loop):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    # Test 7: No Loops - O(1)
    code7 = """
def add(a, b):
    return a + b
"""
    result, depth, rec, count = analyze_complexity(code7)
    print(f"Test 7 (No Loops):")
    print(f"  Complexity: {result}")
    print(f"  Loop Depth: {depth}, Recursive: {rec}, Calls: {count}")
    print()

    print("=" * 50)
    print("Analysis Complete!")
    print("=" * 50)
