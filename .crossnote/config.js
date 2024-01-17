({
    katexConfig: {
        macros: { // for katex, sync: latex-macros.txt
            "\\abs": "\\left|#1\\right|",
            "\\b": "\\bold{#1}",
            "\\d": "\\frac{\\partial #1}{\\partial 2}",
            "\\l": "\\left",
            "\\label": "~~[\\#\\textrm{#1}]",
            "\\laplacian": "\\mathcal{L}(#1)",
            "\\mb": "\\mathbf{#1}",
            "\\mr": "\\mathrm{#1}",
            "\\opl": "\\operatornamewithlimits{#1}",
            "\\opn": "\\operatorname{#1}",
            "\\r": "\\right",
            "\\t": "{#1}^{\\top}",
            "\\textdash": "\\text{\\textendash}",
        }
    },

    mathjaxConfig: {
        tex: { // for mathjax
            tags: 'ams',
            macros: { // sync: typora https://gist.github.com/garylavayou/97fa124dec4ad15bbe7c9bf800f98f5a
                // macro that simply replace command can be specified simply specified with the replaced command
                abs: ["\\left|#1\\right|", 1],
                b: "\\bold",
                bm: "\\boldsymbol",
                d: ["\\frac{\\partial #1}{\\partial #2}", 2],
                l: "\\left",
                laplacian: ["\\mathcal{L}(#1)", 1],
                mb: "\\mathbf",
                mr: "\\mathrm",
                opl: ["\\operatorname*{#1}", 1],
                opn: "\\operatorname",
                t: ["{#1}^{\\top}", 1],
                r: "\\right",
            }
        },
        "options": {},
        "loader": {}
    },

    mermaidConfig: {
        "startOnLoad": false
    },
})