import sys
import os

# Add the current directory to sys.path from where the script is run
sys.path.append(os.getcwd())

from backend.utils import compile_latex_to_pdf

latex = r"""
\documentclass{article}
\begin{document}
Hello World - Regression Fix Test
\end{document}
"""
print("Attempting to compile simple LaTeX with restored absolute path...")
result = compile_latex_to_pdf(latex)
if result:
    print(f"Success! PDF generated at: {result}")
else:
    print("Failure: compile_latex_to_pdf returned None")
