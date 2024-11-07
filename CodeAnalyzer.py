import ast
import os
import re
import tokenize
from pathlib import Path

class CodeAnalyzer:
    def __init__(self, code_path):
        self.code_path = code_path
        self.pep8_violations = []
        self.security_warnings = []
        self.performance_issues = []

    def analyze_pep8(self):
        with tokenize.open(self.code_path) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token_type, token_string, start, end, line in tokens:
                if token_type == tokenize.NAME:
                    if len(token_string) > 79:
                        self.pep8_violations.append(
                            f"Line {start[0]}: Line length exceeds 79 characters"
                        )

    def analyze_security(self):
        with open(self.code_path, 'r') as file:
            content = file.read()
            if re.search(r'eval\(.*\)', content):
                self.security_warnings.append("Usage of 'eval()' detected, potential security risk.")

            if re.search(r'exec\(.*\)', content):
                self.security_warnings.append("Usage of 'exec()' detected, potential security risk.")

    def analyze_performance(self):
        with open(self.code_path, 'r') as file:
            content = file.read()
            if 'for' in content and '.append' in content:
                self.performance_issues.append("Consider using list comprehension for better performance.")

    def analyze_ast(self):
        with open(self.code_path, 'r') as source:
            tree = ast.parse(source.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'id') and node.func.id in ('eval', 'exec'):
                        self.security_warnings.append(
                            f"Line {node.lineno}: Usage of '{node.func.id}()' detected, potential security risk."
                        )
                    if hasattr(node.func, 'attr') and node.func.attr == 'append':
                        self.performance_issues.append(
                            f"Line {node.lineno}: Consider using list comprehension for better performance."
                        )

    def run_analysis(self):
        print("Running PEP8 Analysis...")
        self.analyze_pep8()
        print("Running Security Analysis...")
        self.analyze_security()
        print("Running Performance Analysis...")
        self.analyze_performance()
        print("Running AST Analysis...")
        self.analyze_ast()

        print("\nPEP8 Violations:")
        for violation in self.pep8_violations:
            print(violation)

        print("\nSecurity Warnings:")
        for warning in self.security_warnings:
            print(warning)

        print("\nPerformance Issues:")
        for issue in self.performance_issues:
            print(issue)

if __name__ == "__main__":
    code_file_path = input("Enter the path to the Python file to analyze: ")
    if not os.path.isfile(code_file_path):
        print("Invalid file path.")
    else:
        analyzer = CodeAnalyzer(code_file_path)
        analyzer.run_analysis()
