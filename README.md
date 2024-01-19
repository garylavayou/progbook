# ProgBook

Use mdBook/MkDocs/Docsify to generate a book from my programming notes.

This repository is used for learning how to use [mdBook](https://github.com/rust-lang/mdBook)/MkDocs to generate a nice online book.
The content sources are not contained in this repository.

About writing in [Markdown](https://www.markdownguide.org/).

## Preparation

### Install Python Runtime Environment

```shell
condapack --file requirements.pip progbook #*
```

> `*`: condapack is a self-made conda-wrapper. You can create the environment by directly
> call `conda`:
>
> ```shell
> conda create -n progbook --file requirements.pip
> ```

### Configure the Source

All the necessary referred Markdown documents are specified in `mkdocs.yml` (MkDocs), and we 
will convert the content so that it can be referred by other tools.
For example, you can run the following command to generate files that needed by mdBook:

```shell
conda run --name progbook --no-capture-output python bin/checksource.py > src/SUMMARY.gen.md
```

Based on the convert output, you can identify that is some linked source folder is missing in
local file system, and update the `sources.conf` file with the right source folder.
Then, run the following command to link the source folders into the workspace.

```shell
./bin/linksrc.sh
```

And then rerun the `checksource.py`.

### Find Your Documents

List all the markdown files in the folder:

```shell
tree -l -P '*.md' src | grep -v '.gen.md' | head -n -1 > mydocs.$(date +%F).txt
```

Then, add extra items to your book specification files (`mkdocs.yml`).
You can save the above result, and then next time compare it with new results to find what changes.

## Usage of mdBook

### Install mdBook

```bash
./bin/install-mdbook.sh
```

#### Integrated Plugins for mdBook

- [mdbook-katex](https://github.com/lzanini/mdbook-katex)
- [mdbook-mermaid](https://github.com/badboy/mdbook-mermaid)
- [mdbook-theme](https://github.com/zjp-CN/mdbook-theme)
- ...

### Build the Book

run html service locally to serve documents:

```shell
mv src/SUMMARY.gen.md src/SUMMARY.md  # compare the index file
mdbook serve [path/to/book]  # watch file changes*
```

> `*`: `path/to/book` is the folder containing `book.toml`, default is current working
> directory. `.gitignore` files in the root of the book directory specifies the files
> that should be excluded from watch.

or output html files and then put it on other web servers.

```shell
mdbook build
mdbook watch path/to/book  # watch file changes and rebuild the book*
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

#### Integrated Plugins for Docsify

- [docsify-autoHeaders (modified)](https://github.com/garylavayou/docsify-autoHeaders/tree/level-range-auto-number);
- [docsify-mermaid](https://github.com/Leward/mermaid-docsify)
- [docsify-tabs](https://jhildenbiddle.github.io/docsify-tabs/)
- docsify-sidebar-collapse
- [docsify-latex](https://scruel.github.io/docsify-latex/#/) (KaTeX/MathJax)
- [docsify-progress](https://github.com/HerbertHe/docsify-progress)
- [docsify-image-caption](https://h-hg.github.io/docsify-image-caption/#/)
- [prism](https://docsify.js.org/#/language-highlight)

### Compile Document Source via Docsify

```shell
conda run --name progbook --no-capture-output python bin/checksource.py --style docsify > docs/README.gen.md
conda run --name progbook --no-capture-output python bin/checksource.py --style docsify_sidebar > docs/_sidebar.gen.md
SOURCE_DIR=docs ./bin/linksrc.sh
./bin/docsify-compile.py --clean --offline
docsify serve .build
```

#### Deploy as Static Site

Upload the content of `.build` to an HTTP server's static resource path, then the site can be visited via that server.
The resource path on HTTP server should be consistent with the configuration `basePath` in `index.html`.
For example, we set it to be `/docsify/` by default, and the access URL should be `http://server-site:port/docsify/"`。

For demonstration purpose, we can simply link the content into the deploy location:

```shell
mkdir -p ~/usr/share/html && ln -svf --no-dereference $(realpath .build) ~/usr/share/html/docsify
conda run --name progbook --no-capture-output python -m http.server --bind 0.0.0.0 --directory ~/usr/share/html 8000
```

## Issues

### Current Issues of Using mdbook

1. Cannot render math equations with `$...$` notations.

   - Official Notes: [MathJax Support](https://rust-lang.github.io/mdBook/format/mathjax.html)
   - The issue post: [Improve MathJax support by enabling `$$` for math equations (#400)](https://github.com/rust-lang/mdBook/issues/400)

   **Fix**: solved with [`mdbook-katex`](https://github.com/lzanini/mdbook-katex),
   replacing MathJax, but [KaTeX](#common-issues-on-using-katex-to-render-equations) itself has other issues.

1. Does not support text highlight with `==...==`.

### Current Issues of Using MkDocs

1. 引用块中包含的代码块不能正确被渲染。

### Current Issues of Using Docsify

1. Does not support text highlight with `==...==`.
1. Does not support nesting bold and italic text. `***...***`。

### Common Issues on Using KaTeX to Render Equations

1. KaTeX cannot properly render **display equations in quote text** (==no discussion on the internet==).

1. KaTeX missing support for some latex commands, such as `\abs`.

   See [Supported Functions](https://katex.org/docs/supported) for
   supported LaTeX commands.

   **Fix**: using customized latex macros for katex (depends on the renderer who use
   KaTeX, the configuration methods vary).

1. For KaTeX to work properly: Subscripts including commands should be put into `{...}` block.

1. KaTeX not support `\label` and `\ref`/`\eqref`.
   - <https://github.com/KaTeX/KaTeX/issues/2798>
   - <https://github.com/KaTeX/KaTeX/issues/2003>
  
   **Fix**:
   - use customized macro to renew  `\label` and `\ref`/`\eqref`.
   - does not include `_` (underscore) in label string.