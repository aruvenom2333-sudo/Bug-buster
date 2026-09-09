import ast
from collections import defaultdict

class AdvancedComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        # Function stack for nested functions
        self.function_stack = []
        self.current_function = None
        
        # Loop tracking
        self.loop_stack = []
        self.max_loop_depth = 0
        self.has_nested_loops = False
        
        # Recursion detection
        self.call_graph = defaultdict(list)
        self.recursive_functions = set()
        self.recursive_call_count = 0
        
        # Memory tracking
        self.allocates_memory = False
        self.memory_structures = []
        
        # Track function arguments
        self.function_args = {}
        self.arg_names = []
        
        # Track break statements
        self.break_detected = False

    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.current_function = node.name
        self.arg_names = [arg.arg for arg in node.args.args]
        self.function_args[node.name] = self.arg_names
        
        self.generic_visit(node)
        
        self.function_stack.pop()
        self.current_function = self.function_stack[-1] if self.function_stack else None

    def _determine_loop_variant(self, node):
        """Check if a loop divides/multiplies its control variable (Logarithmic)."""
        for child in ast.walk(node):
            if isinstance(child, ast.AugAssign):
                if isinstance(child.op, (ast.Mult, ast.Div, ast.FloorDiv, ast.RShift, ast.LShift)):
                    return 'log'
            elif isinstance(child, ast.Assign):
                if isinstance(child.value, ast.BinOp):
                    if isinstance(child.value.op, (ast.Mult, ast.Div, ast.FloorDiv, ast.RShift, ast.LShift)):
                        return 'log'
        return 'linear'

    def visit_For(self, node):
        self.loop_stack.append('for')
        current_depth = len(self.loop_stack)
        if current_depth > self.max_loop_depth:
            self.max_loop_depth = current_depth
            if current_depth >= 2:
                self.has_nested_loops = True
        
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_While(self, node):
        self.loop_stack.append('while')
        current_depth = len(self.loop_stack)
        if current_depth > self.max_loop_depth:
            self.max_loop_depth = current_depth
            if current_depth >= 2:
                self.has_nested_loops = True
        
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_ListComp(self, node):
        self.loop_stack.append('for')
        current_depth = len(self.loop_stack)
        if current_depth > self.max_loop_depth:
            self.max_loop_depth = current_depth
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_GeneratorExp(self, node):
        self.loop_stack.append('for')
        current_depth = len(self.loop_stack)
        if current_depth > self.max_loop_depth:
            self.max_loop_depth = current_depth
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            if self.current_function:
                self.call_graph[self.current_function].append(func_name)
            
            if func_name == self.current_function:
                self.recursive_functions.add(self.current_function)
                self.recursive_call_count += 1
            
            if func_name in ['list', 'dict', 'set', 'tuple']:
                self.allocates_memory = True
                self.memory_structures.append(f"{func_name}()")
        
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            self.allocates_memory = True
            self.memory_structures.append(type(node.value).__name__.lower())
        self.generic_visit(node)

    def visit_Break(self, node):
        self.break_detected = True
        self.generic_visit(node)

    def _detect_mutual_recursion(self):
        """Detect cycles in the call graph (mutual recursion)."""
        visited = set()
        path = set()
        
        # Create a copy of the keys to iterate over
        # This prevents "dictionary changed size during iteration" error
        function_names = list(self.call_graph.keys())
        
        def dfs(node):
            if node in path:
                return True
            if node in visited:
                return False
            visited.add(node)
            path.add(node)
            for neighbor in self.call_graph.get(node, []):
                if dfs(neighbor):
                    return True
            path.remove(node)
            return False
        
        for func in function_names:
            if dfs(func):
                self.recursive_functions.add(func)

    def analyze(self, code_string):
        try:
            tree = ast.parse(code_string)
        except SyntaxError as e:
            return f"Syntax Error: {e}", "Unknown"

        # Reset state
        self.__init__()
        
        # Parse the code
        self.visit(tree)
        
        # Check for mutual recursion
        self._detect_mutual_recursion()
        
        # Determine Time Complexity
        if self.recursive_functions:
            if self.recursive_call_count >= 2:
                time_complexity = "O(2^n) - Exponential (Multiple Recursion)"
            else:
                time_complexity = "O(n) - Linear Recursion"
        elif self.max_loop_depth == 0:
            time_complexity = "O(1) - Constant"
        elif self.max_loop_depth == 1:
            time_complexity = "O(n) - Linear"
        elif self.max_loop_depth == 2:
            time_complexity = "O(n²) - Quadratic"
        elif self.max_loop_depth == 3:
            time_complexity = "O(n³) - Cubic"
        elif self.max_loop_depth == 4:
            time_complexity = "O(n⁴) - Quartic"
        else:
            time_complexity = f"O(n^{self.max_loop_depth}) - Polynomial (Depth {self.max_loop_depth})"
        
        # Determine Space Complexity
        if self.recursive_functions:
            space_complexity = "O(n) - Auxiliary Stack Space"
        elif self.allocates_memory:
            space_complexity = "O(n) - Dynamic Data Structure allocation"
        else:
            space_complexity = "O(1) - Constant Space"
        
        return time_complexity, space_complexity


def analyze_advanced_complexity(code_string):
    analyzer = AdvancedComplexityAnalyzer()
    return analyzer.analyze(code_string)