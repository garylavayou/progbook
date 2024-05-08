#!/usr/bin/python3
import os
import re
import shutil
import subprocess as sp
import sys
from argparse import ArgumentParser
from typing import List, Union


def exec(command: Union[str, List[str]], on_error="exit", log:bool=False, **options):
    if log:
        print(f"exec: {command}", file=sys.stderr)
    if isinstance(command, str):
        p = sp.run(command, shell=True, **options)
    else:
        p = sp.run(command, **options)
    if p.returncode != 0:
        print(f"error: return code [{p.returncode}].")
        if on_error == "exit":
            sys.exit(p.returncode)
    return p.returncode


def init_dir(filename: str):
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


parser = ArgumentParser()
parser.add_argument(
    "--offline",
    action="store_true",
    help="""prepare documents for offline deployment, which adding
    offline processing logics.""",
)
parser.add_argument(
    "--clean", action="store_true", help="clean the output before building."
)
parser.add_argument(
    "--source",
    action="store",
    type=str,
    default="docs",
    help="source directory of markdown files.",
)
parser.add_argument(
    "--target",
    action="store",
    type=str,
    default=".build",
    help="target directory to save the processed markdown and related files.",
)
options = parser.parse_args(args=sys.argv[1:])

source_dir = options.source
target_dir = options.target
include_filters = [r"\.(md|png|jpe?g|svg|webp|gif)", r"\.nojekyll", r"sw\.js"]
if options.offline:
    include_filters.extend(["docsify-fonts", "docsify-plugins"])
else:
    include_filters.extend([r"index\.html"])
# exclude_filters have higher priority than include_filters (like rsync)
exclude_filters = [
    r"\.gen\.md$",
    r"/\.~",
    r"\.(?:obsidian)",
    r"(?:quarto_files|node_modules)",  # node_modules not synced, install it in target dir
]
if options.clean and os.path.exists(target_dir):
    shutil.rmtree(target_dir, ignore_errors=False)

for dirpath, _, filenames in os.walk(source_dir, followlinks=True):
    # for d in dirnames:
    #   print('{0}: '.format(os.path.join(dirpath, d)))

    for f in filenames:
        filepath = os.path.join(dirpath, f)
        tf_skip = False
        for pattern in exclude_filters:
            m = re.search(pattern, filepath)
            if m is not None:
                tf_skip = True
                break
        if tf_skip:
            continue
        tf_match = False
        for pattern in include_filters:
            m = re.search(pattern, filepath)
            if m is not None:
                print("{0}".format(filepath))
                tf_match = True
                break
        if not tf_match:
            continue
        target_file = filepath.replace(source_dir, target_dir, 1)
        init_dir(target_file)
        if filepath.endswith(".md"):
            # prepend path prefix for relative path images
            #   'src = "path/to/image.png"' -> 'src = "{prefix}/path/to/image.png"'
            # exceptions:
            #   'src="http://example.com/path/to/image.png"'
            #   'src = "/path/to/image.png"'
            #! only processing new/newer files
            if os.path.exists(target_file) and os.path.getmtime(filepath) <= os.path.getmtime(target_file):
                print(f"info: source <{filepath}> is not updated since the last compile, skip!")
                continue
            dir_prefix = (
                os.path.dirname(filepath)
                .replace(source_dir, ".", 1)
                .replace("/", r"\/")
            )
            #! update file contents and save to target file
            replace_command = rf"""
              perl -pe 's/\bsrc\s*=\s*"(?!(?:https?:\/)?\/)(?:\.\/)?(.*)"/src="{dir_prefix}\/\1"/' '{filepath}' | tee '{target_file}' | sed -En 's/src=/src=/p' | xargs -I {{}} echo "-> {{}}"
            """
            # print(replace_command)
            exec(replace_command)
        else:
            exec(["rsync", "-ua", "--delete", filepath, target_file])  # -v
# TODO: sync all other files at once, need better filter rules.
# wildcard PATTERN MATCHING RULES for include/exclude            
# sync = [
#     "rsync", 
#     "-ua", 
#     "--delete", 
#     source_dir+'/', 
#     target_dir+"/", 
#     "--include", "**.png",
#     "--include", "**.jpg",
#     "--include", "**.jpeg",
#     "--include", "**.webp",
#     "--include", "**.gif",
#     "--include", ".nojekyll",
#     "--include", "sw.js",
#     "--exclude", "*",
#     ]
# exec(sync, log=True)

if options.offline:
    #! sync index.local.html as index.html
    # TODO replace the base URL setting in "/index.local.html" with customized value.
    filepath = source_dir + "/index.local.html"
    target_file = target_dir + "/index.html"
    exec(["rsync", "-uav", filepath, target_file])
    #! use synced node package specification to install node modules in target
    filepath = target_dir + "/docsify-plugins/package.json"
    if not os.path.exists(filepath):
        raise FileNotFoundError("node package specification does not synced to target")
    cur_dir = os.getcwd()
    work_dir = os.path.dirname(filepath)
    os.chdir(work_dir)
    exec(["npm", "install"])
    os.chdir(cur_dir)
    #! sync offline font resources
    if not os.path.exists(os.path.join(source_dir, "docsify-themes", "fonts")):
        os.environ['THEME_DIR'] = os.path.join(source_dir, "docsify-themes")
        os.environ['DOCSIFY_DIR'] = os.path.join(source_dir, "docsify-plugins/node_modules/docsify")
        os.environ['TARGET_DIR'] = os.path.join(source_dir)
        exec(["./bin/docsify-fonts.sh"])
    for dirpath, _, filenames in os.walk(
        source_dir + "/docsify-themes", followlinks=True
    ):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            target_file = filepath.replace(source_dir, target_dir, 1)
            init_dir(target_file)
            if filepath.find("fonts") == -1:
                # the main css files
                replace_dir_prefix = (
                    rf".\/fonts\/{f}"  # relative to the main theme files
                )
                # replace_dir_prefix = rf'\/docsify-themes\/fonts\/{f}'
                replace_command = rf"""
                sed -E 's/@import\s+url\(".*"\)/@import url("{replace_dir_prefix}")/' '{filepath}' | tee '{target_file}' | sed -En 's/@import url/@import url/p'
                """
            else:
                # css files of fonts, 
                # font url inside should be specifies relative to the css file.
                # `../..` will be removed to generate the synthesized URL for the request by browser.
                replace_dir_prefix = rf"..\/..\/docsify-fonts"
                replace_command = rf"""
                sed -E 's/(src:\s*url)\(https?:\/\/.*.com\/(.*)\)\s*(format\(.*\))/\1({replace_dir_prefix}\/\2) \3/' '{filepath}' | tee '{target_file}' | sed -En 's/src: url/src: url/p'
                """
            print(f"{filepath} -> {target_file}")
            exec(replace_command)
else:
    # sync the extra local JS files.
    # target directory will be automatically created.
    exec(f"rsync -uav {source_dir}/docsify-plugins/*.js {target_dir}/docsify-plugins/")