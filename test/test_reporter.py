#!/usr/bin/env python3
"""
HTML Test Report Generator

Generates professional HTML reports for test execution results with detailed
formatting, statistics, and visual indicators.

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class TestResult:
    """Represents a single test result with all relevant information."""
    
    def __init__(self, test_name: str, status: str, duration: float = 0.0, 
                 output: str = "", error: str = "", details: Dict[str, Any] = None):
        self.test_name = test_name
        self.status = status  # 'PASSED', 'FAILED', 'ERROR', 'SKIPPED'
        self.duration = duration
        self.output = output
        self.error = error
        self.details = details or {}
        self.timestamp = datetime.now()


class TestReportGenerator:
    """Generates professional HTML test reports."""
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        self.start_time = datetime.now()
        self.end_time = None
        self.total_duration = 0.0
        
    def add_test_result(self, result: TestResult):
        """Add a test result to the report."""
        self.test_results.append(result)
        
    def add_test(self, test_name: str, status: str, duration: float = 0.0,
                output: str = "", error: str = "", details: Dict[str, Any] = None):
        """Add a test result with individual parameters."""
        result = TestResult(test_name, status, duration, output, error, details)
        self.add_test_result(result)
        
    def finalize(self):
        """Finalize the report by setting end time and calculating totals."""
        self.end_time = datetime.now()
        self.total_duration = (self.end_time - self.start_time).total_seconds()
        
    def get_statistics(self) -> Dict[str, int]:
        """Calculate test statistics."""
        stats = {
            'total': len(self.test_results),
            'passed': 0,
            'failed': 0,
            'error': 0,
            'skipped': 0
        }
        
        for result in self.test_results:
            status_key = result.status.lower()
            if status_key in stats:
                stats[status_key] += 1
                
        return stats
        
    def get_success_rate(self) -> float:
        """Calculate success rate percentage."""
        stats = self.get_statistics()
        if stats['total'] == 0:
            return 0.0
        return (stats['passed'] / stats['total']) * 100
        
    def generate_html_report(self, output_path: str = None) -> str:
        """Generate comprehensive HTML test report."""
        
        if output_path is None:
            # Create test/results directory structure
            project_root = Path(__file__).parent.parent
            results_dir = project_root / "test" / "results"
            results_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = results_dir / f"test_result_{timestamp}.html"
            
        if self.end_time is None:
            self.finalize()
            
        stats = self.get_statistics()
        success_rate = self.get_success_rate()
        
        html_content = self._generate_html_template(stats, success_rate)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-16') as f:
            f.write(html_content)
            
        return str(output_path)
        
    def _generate_html_template(self, stats: Dict[str, int], success_rate: float) -> str:
        """Generate the complete HTML template."""
        
        # Generate CSS styles
        css_styles = self._generate_css_styles()
        
        # Generate test results HTML
        test_results_html = self._generate_test_results_html()
        
        # Generate summary statistics
        summary_html = self._generate_summary_html(stats, success_rate)
        
        # Generate timeline
        timeline_html = self._generate_timeline_html()
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-16">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results Report - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        {css_styles}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <h1>🧪 Requirement Editor Test Report</h1>
            <div class="report-meta">
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Test Suite:</strong> Requirement Editor v1.0.0</p>
                <p><strong>Duration:</strong> {self.total_duration:.2f} seconds</p>
            </div>
        </header>

        <!-- Summary Statistics -->
        {summary_html}

        <!-- Timeline -->
        {timeline_html}

        <!-- Test Results -->
        <section class="section">
            <h2>📋 Detailed Test Results</h2>
            {test_results_html}
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p>Report generated by Requirement Editor Test Suite</p>
            <p>Author: Attila Gallai &lt;attila@tux-net.hu&gt;</p>
            <p>License: MIT License</p>
        </footer>
    </div>

    <script>
        {self._generate_javascript()}
    </script>
</body>
</html>"""
        
        return html_template
        
    def _generate_css_styles(self) -> str:
        """Generate CSS styles for the report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }

        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 15px;
        }

        .report-meta {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .report-meta p {
            margin: 5px 0;
            color: #6c757d;
        }

        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-card.passed {
            background: linear-gradient(135deg, #27ae60, #229954);
        }

        .stat-card.failed {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }

        .stat-card.error {
            background: linear-gradient(135deg, #f39c12, #e67e22);
        }

        .stat-card.skipped {
            background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        }

        .stat-number {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .success-rate {
            text-align: center;
            margin: 30px 0;
        }

        .success-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
            font-weight: bold;
            color: white;
            background: conic-gradient(#27ae60 var(--percentage), #ecf0f1 0);
        }

        .test-results {
            margin-top: 20px;
        }

        .test-item {
            background: #f8f9fa;
            border-left: 5px solid #3498db;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .test-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }

        .test-item.passed {
            border-left-color: #27ae60;
        }

        .test-item.failed {
            border-left-color: #e74c3c;
        }

        .test-item.error {
            border-left-color: #f39c12;
        }

        .test-item.skipped {
            border-left-color: #95a5a6;
        }

        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .test-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }

        .test-status {
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }

        .test-status.passed {
            background: #27ae60;
        }

        .test-status.failed {
            background: #e74c3c;
        }

        .test-status.error {
            background: #f39c12;
        }

        .test-status.skipped {
            background: #95a5a6;
        }

        .test-details {
            margin-top: 15px;
        }

        .test-output {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }

        .test-error {
            background: #fee;
            color: #c0392b;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            margin-top: 10px;
            border: 1px solid #f5b7b1;
        }

        .timeline {
            margin: 20px 0;
        }

        .timeline-item {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .timeline-time {
            font-family: 'Courier New', monospace;
            color: #6c757d;
            margin-right: 20px;
            min-width: 120px;
        }

        .timeline-content {
            flex: 1;
        }

        .footer {
            text-align: center;
            padding: 30px;
            color: white;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
        }

        .footer p {
            margin: 5px 0;
        }

        .collapsible {
            cursor: pointer;
            user-select: none;
        }

        .collapsible:hover {
            opacity: 0.8;
        }

        .collapsible-content {
            display: none;
        }

        .collapsible-content.active {
            display: block;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .test-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
        """
        
    def _generate_summary_html(self, stats: Dict[str, int], success_rate: float) -> str:
        """Generate summary statistics HTML."""
        return f"""
        <section class="section">
            <h2>📊 Test Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats['total']}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-card passed">
                    <div class="stat-number">{stats['passed']}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-card failed">
                    <div class="stat-number">{stats['failed']}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card error">
                    <div class="stat-number">{stats['error']}</div>
                    <div class="stat-label">Errors</div>
                </div>
                <div class="stat-card skipped">
                    <div class="stat-number">{stats['skipped']}</div>
                    <div class="stat-label">Skipped</div>
                </div>
            </div>
            
            <div class="success-rate">
                <div class="success-circle" style="--percentage: {success_rate * 3.6}deg;">
                    {success_rate:.1f}%
                </div>
                <p><strong>Success Rate</strong></p>
            </div>
        </section>
        """
        
    def _generate_test_results_html(self) -> str:
        """Generate detailed test results HTML."""
        if not self.test_results:
            return "<p>No test results available.</p>"
            
        results_html = '<div class="test-results">'
        
        for i, result in enumerate(self.test_results):
            status_class = result.status.lower()
            test_id = f"test_{i}"
            
            output_section = ""
            if result.output:
                output_section = f'<div class="test-output">{self._escape_html(result.output)}</div>'
                
            error_section = ""
            if result.error:
                error_section = f'<div class="test-error">{self._escape_html(result.error)}</div>'
                
            details_section = ""
            if result.details:
                details_list = []
                for key, value in result.details.items():
                    details_list.append(f"<strong>{key}:</strong> {self._escape_html(str(value))}")
                details_section = f'<div class="test-details">{"<br>".join(details_list)}</div>'
            
            results_html += f"""
            <div class="test-item {status_class}">
                <div class="test-header collapsible" onclick="toggleCollapsible('{test_id}')">
                    <div class="test-name">{self._escape_html(result.test_name)}</div>
                    <div>
                        <span class="test-status {status_class}">{result.status}</span>
                        <span style="margin-left: 15px; color: #6c757d;">{result.duration:.3f}s</span>
                    </div>
                </div>
                <div id="{test_id}" class="collapsible-content">
                    <p><strong>Executed:</strong> {result.timestamp.strftime('%H:%M:%S')}</p>
                    {details_section}
                    {output_section}
                    {error_section}
                </div>
            </div>
            """
            
        results_html += '</div>'
        return results_html
        
    def _generate_timeline_html(self) -> str:
        """Generate test execution timeline HTML."""
        if not self.test_results:
            return ""
            
        timeline_html = '''
        <section class="section">
            <h2>⏱️ Execution Timeline</h2>
            <div class="timeline">
        '''
        
        timeline_html += f'''
            <div class="timeline-item">
                <div class="timeline-time">{self.start_time.strftime('%H:%M:%S')}</div>
                <div class="timeline-content">
                    <strong>🚀 Test Suite Started</strong>
                </div>
            </div>
        '''
        
        for result in self.test_results:
            status_icon = {
                'PASSED': '✅',
                'FAILED': '❌', 
                'ERROR': '⚠️',
                'SKIPPED': '⏭️'
            }.get(result.status, '❓')
            
            timeline_html += f'''
            <div class="timeline-item">
                <div class="timeline-time">{result.timestamp.strftime('%H:%M:%S')}</div>
                <div class="timeline-content">
                    {status_icon} <strong>{self._escape_html(result.test_name)}</strong> 
                    - {result.status} ({result.duration:.3f}s)
                </div>
            </div>
            '''
            
        if self.end_time:
            timeline_html += f'''
            <div class="timeline-item">
                <div class="timeline-time">{self.end_time.strftime('%H:%M:%S')}</div>
                <div class="timeline-content">
                    <strong>🏁 Test Suite Completed</strong>
                </div>
            </div>
            '''
            
        timeline_html += '</div></section>'
        return timeline_html
        
    def _generate_javascript(self) -> str:
        """Generate JavaScript for interactive features."""
        return """
        function toggleCollapsible(elementId) {
            const content = document.getElementById(elementId);
            content.classList.toggle('active');
        }
        
        // Auto-expand failed tests
        document.addEventListener('DOMContentLoaded', function() {
            const failedTests = document.querySelectorAll('.test-item.failed .collapsible-content, .test-item.error .collapsible-content');
            failedTests.forEach(test => {
                test.classList.add('active');
            });
        });
        """
        
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
