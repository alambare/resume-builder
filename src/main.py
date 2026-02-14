import argparse
import sys
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
from .latex_generator import LatexGenerator

def main():
    parser = argparse.ArgumentParser(description='Build Resume PDF from YAML.')
    parser.add_argument('input_file', help='Input YAML file path')
    parser.add_argument('--template', '-t', default='basic', choices=['basic', 'two_column'], help='Resume template style (basic: 1-col, two_column: 2-col)')
    parser.add_argument('--name', '-n', help='Custom output name (without extension)')
    parser.add_argument('--dir', '-d', default='output', help='Parent output directory')
    parser.add_argument('--debug', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    template_path = Path(f"templates/{args.template}.tex.jinja2")
    
    # Check if user provided a custom path (if logic ever expands) or fallback check
    if not template_path.exists():
        print(f"Error: Template file '{template_path}' not found.")
        sys.exit(1)

    # Load Data
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        sys.exit(1)

    # Determine Filename
    if args.name:
        base_name = args.name
    else:
        name_val = data.get('name', 'resume').replace(' ', '_').replace('é', 'e')
        date_str = datetime.now().strftime('%Y-%m-%d')
        base_name = f"{name_val}_{date_str}"

    # Setup Output Directory
    parent_dir = Path(args.dir)
    output_dir = parent_dir / base_name
    
    # Handle unique directory name
    counter = 1
    original_output_dir = output_dir
    while output_dir.exists():
        output_dir = Path(f"{original_output_dir}.{counter}")
        counter += 1
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {output_dir}")

    # Generate LaTeX
    generator = LatexGenerator(template_path)
    tex_filename = f"{base_name}.tex"
    tex_path = output_dir / tex_filename
    
    try:
        generator.generate(data, tex_path)
        print(f"✅ Generated LaTeX: {tex_path}")
    except Exception as e:
        print(f"Error generating LaTeX: {e}")
        sys.exit(1)

    # Compile PDF
    print("Compiling PDF...")
    
    # We use pdflatex. 
    # -output-directory must be the directory where the .tex file is to keep artifacts together.
    # The input file path passed to pdflatex must be relative to the cwd or absolute.
    
    compile_cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir}",
        str(tex_path)
    ]

    # Run compilation twice for references
    for run_num in range(1, 3):
        if args.debug:
            print(f"--- Compilation Run {run_num} ---")
            result = subprocess.run(compile_cmd)
        else:
            result = subprocess.run(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if result.returncode != 0:
            print(f"❌ Error during PDF compilation (Run {run_num}).")
            if not args.debug:
                print("Try running with --debug to see details.")
            sys.exit(1)

    pdf_path = output_dir / f"{base_name}.pdf"
    if pdf_path.exists():
        print(f"✅ Success! PDF generated at: {pdf_path}")
    else:
        print("❌ Error: PDF file was not found after compilation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
