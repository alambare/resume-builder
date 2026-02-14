import re
from pathlib import Path
from jinja2 import Template
from datetime import datetime

class LatexGenerator:
    def __init__(self, template_path):
        self.template_path = Path(template_path)

    def generate(self, data, output_path):
        """Generate LaTeX file from data dictionary."""
        escaped_data = self._prepare_data(data)
        
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_str = f.read()

        template = Template(template_str)
        rendered_tex = template.render(escaped_data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_tex)
        
        return output_path

    def _prepare_data(self, data):
        """Prepare data for LaTeX rendering (escaping, formatting)."""
        # Extract display names from URLs if they exist
        if 'linkedin' in data and 'linkedin_display' not in data:
            match = re.search(r'linkedin\.com/in/([^/?]+)', data['linkedin'])
            if match:
                data['linkedin_display'] = match.group(1)

        if 'github' in data and 'github_display' not in data:
            match = re.search(r'github\.com/([^/?]+)', data['github'])
            if match:
                data['github_display'] = match.group(1)

        cv_escaped = data.copy() # Start with all data
        
        # Override complex fields that need specific escaping
        if 'skills' in data:
            cv_escaped['skills'] = {self._escape_latex(k): self._escape_yaml_data(v, escape_keys=True) for k, v in data['skills'].items()}
        
        if 'experience' in data:
            cv_escaped['experience'] = []
            for exp in data['experience']:
                exp_copy = self._escape_yaml_data(exp.copy(), escape_keys=True)
                if 'start' in exp:
                    exp_copy['start'] = self._format_date(exp['start'])
                if 'end' in exp:
                    exp_copy['end'] = self._format_date(exp['end'])
                cv_escaped['experience'].append(exp_copy)

        if 'education' in data:
            cv_escaped['education'] = []
            for edu in data['education']:
                edu_copy = self._escape_yaml_data(edu.copy(), escape_keys=True)
                if 'start' in edu:
                    edu_copy['start'] = self._format_date(edu['start'])
                if 'end' in edu:
                    edu_copy['end'] = self._format_date(edu['end'])
                cv_escaped['education'].append(edu_copy)

        # Process remaining simple fields to ensure they are escaped
        for key, value in data.items():
            if key not in ['skills', 'experience', 'education']:
                cv_escaped[key] = self._escape_yaml_data(value, escape_keys=True)
        
        return cv_escaped

    def _escape_latex(self, text):
        """Escape special LaTeX characters"""
        if not isinstance(text, str):
            return text
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '<': r'$<$',
            '>': r'$>$',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _convert_markdown_to_latex(self, text):
        """Convert markdown bold **text** to LaTeX \\textbf{text}"""
        if not isinstance(text, str):
            return text
        # Replace **text** with \textbf{text}
        text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
        return text

    def _format_date(self, date_str):
        """Convert YYYY-MM format to 'Month YYYY' or handle 'Present'"""
        if not isinstance(date_str, str):
            return date_str
        if date_str.lower() == 'present':
            return 'Present'
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m')
            return date_obj.strftime('%B %Y')
        except ValueError:
            return date_str

    def _escape_yaml_data(self, data, escape_keys=False):
        """Recursively escape LaTeX characters in YAML data"""
        if isinstance(data, dict):
            if not escape_keys:
                return {k: self._escape_yaml_data(v, escape_keys=True) for k, v in data.items()}
            else:
                return {self._escape_latex(k): self._escape_yaml_data(v, escape_keys=True) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._escape_yaml_data(item, escape_keys=True) for item in data]
        elif isinstance(data, str):
            text = self._convert_markdown_to_latex(data)
            return self._escape_latex(text)
        else:
            return data
