## Usage

### 1. Configuration 
Create your configuration file from the example:
```shell
cp resume.yaml.example resume.yaml
# Edit resume.yaml with your details
```

### 2. Installation

Install TexLive: https://tug.org/texlive/quickinstall.html

```shell
pip install .

tlmgr init-usertree
tlmgr install --usermode fontawesome7
```

### 2. Build Resume
Run the builder with your YAML file:

```shell
resume-builder resume.yaml [OPTIONS]
```

**Options:**
- `-n, --name NAME` : Custom output filename
- `-t, --template`  : Template to choose from (default: `basic`)
- `-d, --dir PATH`  : Parent output directory (default: `output/`)
- `--debug`         : Enable verbose logs

**Example:**
```shell
resume-builder resume.yaml
```

### 3. Manual PDF Generation
If you want to compile a `.tex` file manually (e.g., after editing the generated LaTeX):

```shell
pdflatex -output-directory=DEST_DIR SOURCE_FILE.tex
```

*Note: You may need to run this command twice to ensure links and references are resolved correctly.*