import os
import sys
import warnings
from argparse import ArgumentParser
from typing import Union

import yaml

print_newline = False
# title: str = "Summary"  # title need not to be passed to subroutine
# style: str = 'mdbook'
def check_source(
    specs: Union[dict, list], docs_dir: str, 
    indent: int = 0, 
):
    global print_newline,style,title
    count = 0
    if indent == 0:
        if style == 'docsify':
            print(f"# {title} <!-- {{docsify-ignore-all}} -->\n")
        elif style == 'docsify_sidebar':
            print(f"[{title}](/README.md)\n\n---\n")
        else:
            print(f"# {title}\n")
    if isinstance(specs, list):
        for i, s in enumerate(specs):
            new_count = check_source(s, docs_dir, indent=indent + 2)
            count = count + new_count
            if indent == 0 and i < len(specs) - 1 and new_count > 0: # at the toplevel
                print("---\n")
            if indent >= 2 and i == len(specs) - 1 and print_newline == False:  # at the 2rd+ level
                print("")
                print_newline = True
    else:
        for entry, source in specs.items():
            # The first level in "nav" use as title, which has no indent
            # The second level in "nav" will be the top items, which also has no indent
            # Hence, the real indent will be minus by 4.
            if style =='docsify_sidebar':
                real_indent = indent - 2
            else:
                real_indent = indent - 4
            if isinstance(source, str):
                path = os.path.join(docs_dir, source)
                if not os.path.exists(path):
                    warnings.warn(f"{entry}: <{path}> does not exist!") # warnings goes to stderr
                else:
                    source = source.replace(" ", "%20")
                    if style == 'docsify_sidebar':
                        source = source.replace('./', '/', 1)  # use absolute path
                    if real_indent < 0:
                        if style.startswith('docsify'):
                            return count  # this file is not included in count
                        else:
                            print(f"[{entry}]({source})\n")
                    elif real_indent == 0 and style == 'docsify_sidebar':
                        # first level always used for groups.
                        return count  # count = 0
                    else:
                        print(f"{' '*real_indent}- [{entry}]({source})")
                        print_newline = False
                    count = count + 1
            else:
                if indent == 2 and style != "docsify_sidebar":
                    print(f"## {entry}\n")
                elif style == 'docsify_sidebar':
                    print(f"{' '*real_indent}- {entry}")  # plaintext group name
                else:
                    try:
                        first_subitem_entry, first_subitem_source = tuple(
                            source[0].items()
                        )[0]
                        if first_subitem_entry == entry and isinstance(
                            first_subitem_source, str
                        ):
                            first_subitem_source = first_subitem_source.replace(
                                " ", "%20"
                            )
                            print(
                                f"{' '*real_indent}- [{entry}]({first_subitem_source})"
                            )
                        else:
                            print(f"{' '*real_indent}- [{entry}]()")
                    except:
                        print(f"{' '*real_indent}- [{entry}]()")
                count = count + check_source(source, docs_dir, indent=indent)
    return count

parser = ArgumentParser()
parser.add_argument("--title", "-t", default="Summary")
parser.add_argument("--style", "-s", default="mdbook")
options = parser.parse_args(args=sys.argv[1:])
style = options.style
if style == 'docsify':
    title = '目录'
elif style == 'docsify_sidebar':
    title = '首页'
else:
    title = options.title

with open("mkdocs.yml", mode="r") as f:
    mkdocs: dict = yaml.load(f, yaml.FullLoader)

docs_dir = mkdocs.get("docs_dir", "src")
docs_spec = mkdocs.get("nav", None)
if docs_spec is None:
    warnings.warn("Does not specify navigation structure in <mkdocs.yml>!")
    sys.exit(1)

count = check_source(docs_spec, docs_dir)
print(f"{count} of valid source files found!", file=sys.stderr)

# python checksource.py --style docsify > docs/README.gen.md
# python checksource.py --style docsify_sidebar > docs/_sidebar.gen.md
# python checksource.py [--style mdbook]