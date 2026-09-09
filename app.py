# Codex test
from flask import Flask, render_template, request
from advanced import analyze_advanced_complexity
from benchmarker import benchmark_code
import webbrowser
import threading
import time

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    
    print("=" * 60)
    print("ANALYZE REQUEST RECEIVED")
    print(f"Code length: {len(code)} characters")
    print(f"Code preview: {code[:200]}...")
    print("=" * 60)
    
    # Analyze complexity
    time_complexity, space_complexity = analyze_advanced_complexity(code)
    
    # Benchmark the code
    n_values, time_values, graph_image = benchmark_code(code)
    
    print("=" * 60)
    print("RESULTS:")
    print(f"time_complexity: {time_complexity}")
    print(f"space_complexity: {space_complexity}")
    print(f"graph_image exists: {graph_image is not None}")
    print("=" * 60)
    
    return render_template('result.html', 
                           code=code,
                           time=time_complexity,
                           space=space_complexity,
                           graph_image=graph_image,
                           n_values=n_values,
                           time_values=time_values)

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, use_reloader=False)
