## Usage

### 1. Configuration 
Create your configuration file from the example:
```shell
cp resume.yaml.example resume.yaml
# Edit resume.yaml with your details
```

### 2. Installation
Install the package (requires `pdflatex`):

```shell
# for pdflatex
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

pip install .
```

### 2. Build Resume
Run the builder with your YAML file:

```shell
resume-builder resume.yaml [OPTIONS]
```

**Options:**
- `-n, --name NAME` : Custom output filename
- `-d, --dir PATH`  : Parent output directory (default: `output/`)
- `--debug`         : Enable verbose logs

**Example:**
```shell
resume-builder resume.yaml --name "MyResume" --dir ./dist
```

### 3. Manual PDF Generation
If you want to compile a `.tex` file manually (e.g., after editing the generated LaTeX):

```shell
pdflatex -output-directory=DEST_DIR SOURCE_FILE.tex
```

*Note: You may need to run this command twice to ensure links and references are resolved correctly.*