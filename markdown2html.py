#!/usr/bin/python3
'''
This module is a script to convert a Markdown file to an HTML file.

Args:
  The name of the Markdown file to convert
  The name of the output HTML file
'''
import os
import sys


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)
    elif not os.path.isfile(args[1]):
        print(f'Missing {args[1]}', file=sys.stderr)
        sys.exit(1)
    else:
        with open(args[2], mode='w') as out_f:
            with open(args[1]) as in_f:
                for line in in_f:
                    level = line.count('#')
                    if level != 0:
                        line = line.replace('#', '').strip()
                        converted_heading = f'<h{level}>{line}</h{level}>\n'
                    out_f.write(converted_heading)
        sys.exit(0)
