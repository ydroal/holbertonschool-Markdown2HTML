#!/usr/bin/python3
'''
This module is a script to convert a Markdown file to an HTML file.

Args:
  The name of the Markdown file to convert
  The name of the output HTML file
'''
import hashlib
import os
import re
import sys


def convert_bold(markdown_content):
    converted_content = markdown_content
    if converted_content.count('**') >= 2:
        converted_content = converted_content.replace('**', '<b>', 1)
        converted_content = converted_content.replace('**', '</b>', 1)

    if converted_content.count('__') >= 2:
        converted_content = converted_content.replace('__', '<em>', 1)
        converted_content = converted_content.replace('__', '</em>', 1)
    
    return converted_content

def hashing(match):
    original_text = match.group(1)
    hashed_text = hashlib.md5(original_text.encode()).hexdigest()
    
    return hashed_text

def convert_md5(markdown_content):
    converted_content = markdown_content
    # re.sub関数はhashing関数をコールバック関数として呼び出す際、
    # マッチした部分の情報を持つre.Matchオブジェクトをmatch引数として渡す
    hashed_text = re.sub(r'\[\[(.*?)\]\]', hashing, converted_content)
    return hashed_text

def remove_c(markdown_content):
    extracted_contents = re.findall(r'\(\(.*?\)\)', markdown_content)
    for extracted_content in extracted_contents:
        replaced_content = re.sub(r'[cC()]', '', extracted_content)
        markdown_content = markdown_content.replace(extracted_content, replaced_content)
        print (markdown_content)
    
    return markdown_content

if __name__ == '__main__':
    args = sys.argv
    list_exists = False
    ordered_list_exists = False
    paragraph_exists = False
    
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
                    line = convert_bold(lines[i].strip())
                    line = convert_md5(line)
                    line = remove_c(line)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                    else:
                        next_line = ''
                    level = line.count('#')
                    if level != 0:
                        if paragraph_exists:
                            out_f.write('\n</p>\n')
                            paragraph_exists = False
                        line = line.replace('#', '')
                        html_content = f'<h{level}>{line}</h{level}>\n'
                    elif line.startswith('- '):
                        if paragraph_exists:
                            out_f.write('\n</p>\n')
                            paragraph_exists = False
                        line = line.replace('- ', '<li>', 1) + '</li>'
                        if not list_exists:
                            line = f'<ul>\n{line}'
                            list_exists = True    
                        if not next_line.startswith('- '):
                            line += '\n</ul>'
                            list_exists = False
                        html_content = f'{line}\n'
                    elif line.startswith('* '):
                        if paragraph_exists:
                            out_f.write('\n</p>\n')
                            paragraph_exists = False
                        line = line.replace('* ', '<li>', 1) + '</li>'
                        if not ordered_list_exists:
                            line = f'<ol>\n{line}'
                            ordered_list_exists = True    
                        if not next_line.startswith('* '):
                            line += '\n</ol>'
                            ordered_list_exists = False
                        html_content = f'{line}\n'
                    elif not line.startswith(('#','- ','* ')) and line.strip() != '':
                        if not paragraph_exists:
                            line = f'<p>\n{line}'
                            paragraph_exists = True
                        if not next_line.strip() or next_line.startswith(('#','- ','* ')):
                            line += '\n</p>'
                            paragraph_exists = False
                        else:
                            line += '\n<br/>'
                        html_content = f'{line}\n'
                    else:
                        html_content = line
                    out_f.write(html_content)
                if paragraph_exists:
                    out_f.write('\n</p>\n')
    sys.exit(0)
