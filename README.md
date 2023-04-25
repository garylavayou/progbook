# progbook

Use mdBook/MkDocs to generate a book from my programming notes.

This repository is used for learning how to use [mdBook](https://github.com/rust-lang/mdBook)/MkDocs to generate a nice online book.
The content sources are not contained in this repository.

## Configure the Source

Make sure all referred Markdown documents in `src/SUMMARY.md` (mdBook) or `mkdocs.yml` (MkDocs) are put into the `src` folder, or softly linked from the `src` folder.
We use a `sources.conf` file to track the real path of our documents, so that no need to move source documents into the `src` folder.

```
/path/to/real/source1 # -> ln -sf /path/to/real/source1 src/source1
/path/to/real/source2 # -> ln -sf /path/to/real/source2 src/source2
......
```

## Usage of mdBook

### Install mdBook

```bash
version="v0.4.28"
wget "https://github.com/rust-lang/mdBook/releases/download/${version}/mdbook-${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook.tar.gz
mkdir -p ~/bin && tar -xf /tmp/mdbook.tar.gz -C ~/bin
```

### Build the Book

run html service locally to serve documents:

```shell
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

## Issues

### Current Issues of Using mdbook

1. Cannot render math equations with `$...$` notations.

### Current Issues of Using MkDocs

1. 引用块中包含的代码块不能正确被渲染。
2. files in hidden folders, such as ".assets", cannot be accessed.
