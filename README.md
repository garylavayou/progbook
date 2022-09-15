# progbook

Use mdBook/MkDocs to generate a book from my programming notes.

This repository is used for learning how to use [mdBook](https://github.com/rust-lang/mdBook)/MkDocs to generate a nice online book.
The content sources are not contained in this repository.

## Usage of mdBook

Make sure all referred Markdown documents are put into the `src` folder, or softly linked from the `src` folder.

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
