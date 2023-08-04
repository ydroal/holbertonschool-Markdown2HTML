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
    list_exists = False
    ordered_list_exists = False
    
    if len(args) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)
    elif not os.path.isfile(args[1]):
        print(f'Missing {args[1]}', file=sys.stderr)
        sys.exit(1)
    else:
        with open(args[2], mode='w') as out_f:
            with open(args[1]) as in_f:
                lines = in_f.readlines()
                for i in range(len(lines)):
                    line = lines[i].strip()
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                    else:
                        next_line = ''
                    level = line.count('#')
                    if level != 0:
                        line = line.replace('#', '')
                        converted_markdown = f'<h{level}>{line}</h{level}>\n'
                    elif line.startswith('- '):
                        line = line.replace('- ', '<li>', 1) + '</li>'
                        if not list_exists:
                            line = f'<ul>\n{line}'
                            list_exists = True    
                        if not next_line.startswith('- '):
                            line += '\n</ul>'
                            list_exists = False
                        converted_markdown = f'{line}\n'
                    elif line.startswith('* '):
                        line = line.replace('* ', '<li>', 1) + '</li>'
                        if not ordered_list_exists:
                            line = f'<ol>\n{line}'
                            ordered_list_exists = True    
                        if not next_line.startswith('* '):
                            line += '\n</ol>'
                            ordered_list_exists = False
                        converted_markdown = f'{line}\n'
                    else:
                        converted_markdown = line + '\n'
                    out_f.write(converted_markdown)
    sys.exit(0)
