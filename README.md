# progbook

Use mdBook/MkDocs/Docsify to generate a book from my programming notes.

This repository is used for learning how to use [mdBook](https://github.com/rust-lang/mdBook)/MkDocs to generate a nice online book.
The content sources are not contained in this repository.

About writing in [Markdown](https://www.markdownguide.org/).

## Preparation

### Configure the Source

Make sure all referred Markdown documents in `src/SUMMARY.md` (mdBook) or `mkdocs.yml` (MkDocs) are put into the `src` folder, or softly linked from the `src` folder.
We use a `sources.conf` file to track the real path of our documents, so that no need to move source documents into the `src` folder.

```bash
/path/to/real/source1 # -> ln -sf /path/to/real/source1 src/source1
/path/to/real/source2 # -> ln -sf /path/to/real/source2 src/source2
......
```

### Find Your Documents

List all the markdown files in the folder:

```shell
tree -l -P '*.md' src > mydocs.$(date +%F).txt
```

Then, add them to your book specification files.
You can save the result, and then next time compare it with new results to find what changes.

### Install Python Runtime Environment

```shell
condapack --file requirements.pip progbook
```

## Usage of mdBook

### Install mdBook

```bash
version="v0.4.36"
REPO='https://github.com/rust-lang/mdBook'
wget "${REPO}/releases/download/${version}/mdbook-${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook.tar.gz
mkdir -p ~/bin && tar -xf /tmp/mdbook.tar.gz -C ~/bin
mdbook --version
version="v0.5.9"
REPO='https://github.com/lzanini/mdbook-katex'
wget "${REPO}/releases/download/${version}/mdbook-katex-${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook-katex.tar.gz
tar -xf /tmp/mdbook-katex.tar.gz -C ~/bin
mdbook-katex --version
version="v0.13.0"
REPO='https://github.com/badboy/mdbook-mermaid'
wget "${REPO}/releases/download/${version}/mdbook-mermaid-${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook-mermaid.tar.gz
tar -xf /tmp/mdbook-mermaid.tar.gz -C ~/bin
mdbook-mermaid --version
mdbook-mermaid install && mv mermaid*.js theme  # install mermaid support
REPO='https://github.com/zjp-CN/mdbook-theme'
wget "${REPO}/releases/download/v0.1.4/mdbook-theme_linux.tar.gz" --continue -O /tmp/mdbook-theme_linux.tar.gz
tar -xf /tmp/mdbook-theme_linux.tar.gz -C ~/bin
# mdbook-theme has no version info
```

### Build the Book

run html service locally to serve documents:

```shell
conda run --name progbook --no-capture-output python bin/checksource.py > src/SUMMARY.gen.md
./linksrc.sh  # if some files cannot be find by the above command
mv src/SUMMARY.gen.md src/SUMMARY.md  # compare the index file
mdbook serve
```

or output html files and then put it on other web servers.

```shell
mdbook build
```

## Usage of MkDocs

Make sure all referred Markdown documents are put into the `docs` folder, or softly linked from the `docs` folder.

run html service locally to serve documents:

```shell
mkdocs serve
```

or output html files and then put it on other web servers.

```shell
mkdocs build
```

### [MkDocs Plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#navigation--page-building)

```bash
pip install mkdocs-foo-plugin
```

> [Third party extensions](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions).

## Usage of Docsify

### Install Docsify

```shell
npm i docsify-cli -g
```

### Compile Document Source via Docsify

```shell
python bin/checksource.py --style docsify > docs/README.gen.md
python bin/checksource.py --style docsify_sidebar > docs/_sidebar.gen.md
export SOURCE_DIR=docs 
./linksrc.sh
./bin/docsify-compile.py --clean --offline
docsify serve .build
```

## Issues

### Current Issues of Using mdbook

1. Cannot render math equations with `$...$` notations.
   solved with [`mdbook-katex`](https://github.com/lzanini/mdbook-katex), 
   replacing MathJax.

1. KaTeX cannot properly render **display equations in quote text**.

1. KaTeX missing support for some latex commands, such as `\abs`, `\label`.

   See [Supported Functions](https://katex.org/docs/supported) for
   supported LaTeX commands.

   subscripts including commands should be put into `{...}` block.

1. KaTeX not support `\label` and `\ref`.
   - https://github.com/KaTeX/KaTeX/issues/2798
   - https://github.com/KaTeX/KaTeX/issues/2003
  
   > does not include `_` (underscore) in label string.

1. Does not support text highlight with `==...==`.

### Current Issues of Using MkDocs

1. 引用块中包含的代码块不能正确被渲染。

### Current Issues of Using Docsify

1. `Error: Diagram mindmap already registered.`.