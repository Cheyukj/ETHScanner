# app/scanner.py
import os
import re
import json
from slither import Slither
from slither.analyzer import Analyzer
from slither.core import ContractDefinition
from slither.core.declarations import FunctionDeclaration, StateVariableDeclaration
from slither.core.expressions import BinaryOperation, Call, Identifier
from slither.core.values import ArrayConcatenation, ArraySlice, ArrayLength, ArrayIndexAccess

class ContractScanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.analyzer = Slither(self.source_code)
        self.issues = []
        self.custom_rules = []

    def run_static_analysis(self):
        self.analyzer.analyze()
        self._process_issues()

    def _process_issues(self):
        for issue in self.analyzer.issues:
            # Process each issue according to its type and severity
            if issue.issue_type == "Reentrancy":
                self._handle_reentrancy_issue(issue)
            elif issue.issue_type == "Timestamp Dependency":
                self._handle_timestamp_dependency_issue(issue)
            # Add more conditions for other issue types

    def _handle_reentrancy_issue(self, issue):
        # Custom logic for handling reentrancy issues
        self.issues.append({
            "contract": issue.contract_name,
            "function": issue.function_signature,
            "description": "Reentrancy vulnerability detected.",
            "severity": issue.severity,
            "location": issue.location,
        })

    def _handle_timestamp_dependency_issue(self, issue):
        # Custom logic for handling timestamp dependency issues
        self.issues.append({
            "contract": issue.contract_name,
            "function": issue.function_signature,
            "description": "Timestamp dependency vulnerability detected.",
            "severity": issue.severity,
            "location": issue.location,
        })

    def add_custom_rule(self, rule):
        self.custom_rules.append(rule)

    def apply_custom_rules(self):
        for rule in self.custom_rules:
            self._apply_custom_rule(rule)

    def _apply_custom_rule(self, rule):
        # Apply the custom rule to the contract's source code
        # This is a placeholder for the actual rule application logic
        pattern = rule["pattern"]
        for match in re.finditer(pattern, self.source_code):
            location = match.start()
            self.issues.append({
                "contract": "Contract",
                "function": "Function",
                "description": rule["description"],
                "severity": "High",
                "location": location,
            })

    def generate_report(self):
        # Generate a report based on the issues found
        report = "Contract Analysis Report\n"
        report += "=================\n\n"
        for issue in self.issues:
            report += f"Issue: {issue['description']}\n"
            report += f"Severity: {issue['severity']}\n"
            report += f"Location: {issue['location']}\n\n"
        return report

# Example usage:
if __name__ == "__main__":
    # Sample Solidity contract source code
    source_code = """
    pragma solidity ^0.8.0;
    contract Example {
        uint public value;
        function updateValue(uint _value) public {
            value = _value;
        }
    }
    """
    scanner = ContractScanner(source_code)
    scanner.run_static_analysis()
    print(scanner.generate_report())