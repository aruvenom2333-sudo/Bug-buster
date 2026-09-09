import time
import sys
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import ast
import inspect
import math

def benchmark_code(code_string, max_n=1000, steps=5):
    """
    Runs the user's function with different input sizes (n)
    and measures execution time for each.
    Returns: list of n values, list of execution times, and graph image as base64
    """
    # Check if code is empty
    if not code_string or code_string.strip() == "":
        return None, None, "No code provided"
    
    # Debug: Print the code being analyzed
    print("=" * 50)
    print("CODE RECEIVED BY BENCHMARKER:")
    print(code_string)
    print("=" * 50)
    
    # Extract function name from the code
    try:
        tree = ast.parse(code_string)
        func_name = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                break
        if not func_name:
            return None, None, "No function found in code"
        print(f"Function found: {func_name}")
    except SyntaxError as e:
        return None, None, f"Syntax error in code: {str(e)}"
    except Exception as e:
        return None, None, f"Error parsing code: {str(e)}"
    
    # Create a safe execution environment
    safe_globals = {}
    
    # Execute the code to define the function
    try:
        exec(code_string, safe_globals)
        print(f"Function '{func_name}' defined successfully")
    except Exception as e:
        return None, None, f"Error executing code: {str(e)}"
    
    # Get the function
    if func_name not in safe_globals:
        return None, None, f"Function '{func_name}' not found after execution"
    
    func = safe_globals[func_name]
    
    # Check if it's callable
    if not callable(func):
        return None, None, f"'{func_name}' is not a function"
    
    # Get argument names from the function
    try:
        sig = inspect.signature(func)
        arg_names = list(sig.parameters.keys())
        if not arg_names:
            return None, None, "Function has no arguments"
        n_arg = arg_names[0]
        print(f"Using argument: {n_arg}")
    except Exception as e:
        return None, None, f"Could not inspect function signature: {str(e)}"
    
    # Generate n values (logarithmic scale)
    n_values = []
    time_values = []
    
    try:
        for i in range(steps):
            n = int(10 ** (1 + i * (math.log10(max_n) - 1) / (steps - 1)))
            n_values.append(n)
        print(f"n_values: {n_values}")
    except Exception as e:
        return None, None, f"Error generating n values: {str(e)}"
    
    # Benchmark each n value
    for n in n_values:
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            start_time = time.perf_counter()
            kwargs = {n_arg: n}
            func(**kwargs)
            end_time = time.perf_counter()
            
            sys.stdout = old_stdout
            time_values.append(end_time - start_time)
            print(f"n={n}: time={end_time - start_time:.6f}s")
        except RecursionError:
            time_values.append(float('inf'))
            print(f"n={n}: RecursionError")
            break
        except Exception as e:
            time_values.append(float('inf'))
            print(f"n={n}: Error: {str(e)}")
            break
    
    # If some n values failed, truncate the lists
    if float('inf') in time_values:
        idx = time_values.index(float('inf'))
        n_values = n_values[:idx]
        time_values = time_values[:idx]
    
    if not time_values:
        return None, None, "Function failed to execute for any input size"
    
    # Generate the graph
    graph_image = generate_graph(n_values, time_values)
    
    return n_values, time_values, graph_image


def generate_graph(n_values, time_values):
    """
    Generates a Matplotlib graph and returns it as base64 encoded image
    """
    if not n_values or not time_values:
        return None

    try:
        plt.figure(figsize=(8, 5))
        plt.plot(n_values, time_values, 'o-', color='#f0883e', linewidth=2, markersize=8)
        plt.xlabel('Input Size (n)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.title('Performance Analysis: Time vs Input Size', fontsize=14)
        plt.grid(True, alpha=0.3)

        plt.gca().set_facecolor('#0d1117')
        plt.gcf().set_facecolor('#161b22')
        plt.tick_params(colors='#c9d1d9')
        plt.xlabel('Input Size (n)', color='#c9d1d9')
        plt.ylabel('Execution Time (seconds)', color='#c9d1d9')
        plt.title('Performance Analysis: Time vs Input Size', color='#c9d1d9')

        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor='#161b22', edgecolor='none', bbox_inches='tight')
        buf.seek(0)

        graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return f"data:image/png;base64,{graph_base64}"
    except Exception as e:
        print(f"Graph generation error: {e}")
        return None
