#!/usr/bin/python3
import os
import re
import subprocess as sp
from argparse import ArgumentParser
import sys
import shutil

parser = ArgumentParser()
parser.add_argument(
    '--offline', action='store_true', 
    help='''prepare documents for offline deployment, which adding
    offline processing logics.'''
)
parser.add_argument(
    '--clean', action='store_true',
    help='clean the output before building.'
)
options = parser.parse_args(args=sys.argv[1:])

source_dir = "docs"
target_dir = ".build"
filters = ["\.(md|png|jpe?g|svg|webp|gif)", r"\.nojekyll"]
if options.offline:
    filters.extend(
        ['docsify-', ]
    )
else:
    filters.extend(
        [r'index\.html', r'sw\.js']
    )
reverse_filters = [
    '/\.~',
    '\.(?:obsidian)',
    '(?:quarto_files|node_modules)'
]
if options.clean and os.path.exists(target_dir):
    shutil.rmtree(target_dir, ignore_errors=False)

error_code = 0
for dirpath, _, filenames in os.walk(source_dir, followlinks=True):
    # for d in dirnames:
    #   print('{0}: '.format(os.path.join(dirpath, d)))

    for f in filenames:
        filepath = os.path.join(dirpath, f)
        tf_skip = False
        for pattern in reverse_filters:
            m = re.search(pattern, filepath)
            if m is not None:
                tf_skip = True
                break
        if tf_skip:
            continue
        tf_match = False
        for pattern in filters:
            m = re.search(pattern, filepath)
            if m is not None:
                print("{0}".format(filepath))
                tf_match = True
                break
        if not tf_match:
            continue
        target_file = filepath.replace(source_dir, target_dir, 1)
        target_file_dir = os.path.dirname(target_file)
        if not os.path.exists(target_file_dir):
            os.makedirs(target_file_dir)
        if filepath.endswith('.md'):
            # prepend path prefix for relative path images
            #   'src = "path/to/image.png"' -> 'src = "{prefix}/path/to/image.png"'
            # exceptions:
            #   'src="http://example.com/path/to/image.png"'
            #   'src = "/path/to/image.png"'
            dir_prefix = os.path.dirname(filepath).replace(source_dir, r'\.', 1).replace('/', r'\/')
            # sed  -E  's/\bsrc\s*=\s*"(?:\.\/)?([^/].*)"/src="{dir_prefix}\/\1"/' '{filepath}' > '{target_file}'
            replace_command = rf'''
              perl -pe 's/\bsrc\s*=\s*"(?!(?:https?:\/)?\/)(?:\.\/)?(.*)"/src="{dir_prefix}\/\1"/' '{filepath}' | tee '{target_file}' | sed -En 's/src=/src=/p'
            '''
            # print(replace_command)
            p = sp.run(replace_command, shell=True)
        else:
            p = sp.run(["rsync", "-ua", '--delete', filepath, target_file])  # -v
        if p.returncode != 0:
            print(f'error: return code [{p.returncode}].')
            error_code = p.returncode
            break
    if error_code != 0:
        sys.exit(error_code)

if options.offline:
    filepath = source_dir+'/index.local.html'
    target_file = target_dir+'/index.html'
    p = sp.run(["rsync", "-ua", filepath, target_file])
    if p.returncode != 0:
        print(f'error: return code [{p.returncode}].')
        sys.exit(p.returncode)
    filepath = target_dir+'/docsify-plugins/package.json'
    if not os.path.exists(filepath):
        raise FileNotFoundError('node package specification does not')
    work_dir = os.path.dirname(filepath)
    os.chdir(work_dir)
    p = sp.run(["npm", "install"])
    if p.returncode != 0:
        print(f'error: return code [{p.returncode}].')
        sys.exit(p.returncode)
