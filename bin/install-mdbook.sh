#!/bin/bash
set -e

function if_install(){
    exec=$1
    version=$2
    if ! command -v "$exec" > /dev/null; then
        return 0
    else
        v=$($exec --version | sed -E "s/$exec (v?.*)/\1/")
        if [[ "$v" != "$version" ]]; then
            return 0
        fi
    fi
    return 1
}

version="v0.4.36"
if if_install mdbook $version; then
    REPO='https://github.com/rust-lang/mdBook'
    wget "${REPO}/releases/download/${version}/mdbook-${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook.tar.gz
    mkdir -p ~/bin && tar -xf /tmp/mdbook.tar.gz -C ~/bin
    mdbook --version
    mkdir -p ~/.local/share/bash-completion/completions
    mdbook completions bash > ~/.local/share/bash-completion/completions/mdbook
else
    echo "info: mdbook version ($version) exist."
fi

version="0.5.9"
if if_install mdbook-katex $version; then
    REPO='https://github.com/lzanini/mdbook-katex'
    wget "${REPO}/releases/download/v${version}/mdbook-katex-v${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook-katex.tar.gz
    tar -xf /tmp/mdbook-katex.tar.gz -C ~/bin
    mdbook-katex --version
else
    echo "info: mdbook-katex version ($version) exist."
fi

version="0.13.0"
if if_install mdbook-mermaid $version; then
    REPO='https://github.com/badboy/mdbook-mermaid'
    wget "${REPO}/releases/download/v${version}/mdbook-mermaid-v${version}-x86_64-unknown-linux-gnu.tar.gz" --continue -O /tmp/mdbook-mermaid.tar.gz
    tar -xf /tmp/mdbook-mermaid.tar.gz -C ~/bin
    mdbook-mermaid --version
    mdbook-mermaid install && mv mermaid*.js theme  # install mermaid support
else
    echo "info: mdbook-mermaid version ($version) exist."
fi

version="v0.1.4"
# mdbook-theme has no version info
for f in ~/bin/mdbook-theme-v*; do
    name=$(basename "$f")
    tf_install=0
    if [ "$name" == "mdbook-theme-v*" ]; then
        echo "info: mdbook-theme has not been installed!"
    elif [ "$name" == "mdbook-theme-$version" ]; then
        tf_install=1
    else
        echo "info removing old versions..."
        rm -vf "$f"
    fi
    if [[ $tf_install -eq 0 ]]; then
        echo "info: install new version ($version)..."
        REPO='https://github.com/zjp-CN/mdbook-theme'
        wget "${REPO}/releases/download/${version}/mdbook-theme_linux.tar.gz" --continue -O /tmp/mdbook-theme_linux.tar.gz
        tar -xf /tmp/mdbook-theme_linux.tar.gz -C ~/bin
        ln -sf ~/bin/mdbook-theme ~/bin/mdbook-theme-$version
    else
        echo "info: mdbook-theme version ($version) exist."
    fi
done
