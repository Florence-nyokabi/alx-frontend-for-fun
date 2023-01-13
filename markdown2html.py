#!/usr/bin/python3

'''
Converts Markdown to HTML
'''

from sys import argv
from sys import stderr
from os import path


def parse_headings(headings_list: list):
    '''
    Parses markdown headings and converts them to HTML heading tags
    '''
    html_headings = []

    # If hash '#' is found, count number of hashes
    for headings in headings_list:
        if len(headings) > 0 and headings[0] == '#':
            number_of_hashes = 0
            while number_of_hashes < len(
                    headings) and headings[number_of_hashes] == '#':
                number_of_hashes += 1
            # If more than 6 hashes, default to h6
            if number_of_hashes > 6:
                number_of_hashes = 6
            html_tag = 'h' + str(number_of_hashes)
            headings = headings.strip('#')
            # Do not create a space between tag and text
            headings = headings.strip(' ')
            headings = '<' + html_tag + '>' + headings + '</' + html_tag + '>'
        html_headings.append(headings)
    return html_headings


def parse_ordered_list(list_item: list):
    '''
    Parses markdown orderedlists and converts them to HTML heading tags
    '''
    html_list = []
    is_ul = False
    # If '-' is found
    for uls in list_item:
        if len(uls) > 0 and uls[0] == '-':
            if is_ul:
                # Create li tags and blank space on left so text comes after
                # tag
                html_list.append('<li>' + uls[1:].lstrip(' ') + '</li>')
            # Create ul with more than one list item
            else:
                is_ul = True
                html_list.append('<ul>')
                html_list.append('<li>' + uls[1:].lstrip(' ') + '</li>')
        # Find end of list items and close tags
        elif (len(uls) == 0 or uls[0] != '-') and is_ul:
            is_ul = False
            html_list.append('</ul>')
            html_list.append(uls)
        else:
            html_list.append(uls)
    return html_list


def parse_unordered_list(list_item: list):
    '''
    Parses markdown unordered lists and converts them to HTML heading tags
    '''
    html_list = []
    is_ol = False
    for ols in list_item:
        if len(ols) > 0 and ols[0] == '*':
            if is_ol:
                html_list.append('<li>' + ols[1:].lstrip(' ') + '</li>')
            else:
                is_ol = True
                html_list.append('<ol>')
                html_list.append('<li>' + ols[1:].lstrip(' ') + '</li>')
        # Find end of list items and close tags
        elif (len(ols) == 0 or ols[0] != '*') and is_ol:
            is_ol = False
            html_list.append('</ol>')
            html_list.append(ols)
        else:
            html_list.append(ols)
    return html_list


def file_read_write():
    '''
    Parses markdown file, makes appropriate method call
    and creates HTML file with correct tags
    '''

    '''
    Error messages
    '''
    if len(argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)
    if not path.exists(argv[1]):
        print('Missing {}'.format(argv[1]), file=stderr)
        exit(1)

    markdown_file = argv[1]
    output_file = argv[2]

    '''
    List of markdown file elements
    '''
    md_parser_list = []

    '''
    Reads markdown file and parses content
    '''

    with open(markdown_file, 'r') as file:
        md_parser_list = file.readlines()
    md_parser_list = ''.join(md_parser_list).split('\n')

    '''
    Call header method and add to parsed markdown list
    '''
    md_parser_list = parse_headings(md_parser_list)
    md_parser_list = '\n'.join(md_parser_list).split('\n')

    '''
    Call ordered list method and add to parsed markdown list
    '''
    md_parser_list = parse_ordered_list(md_parser_list)
    md_parser_list = '\n'.join(md_parser_list).split('\n')

    '''
    Call unordered list method and add to parsed markdown list
    '''
    md_parser_list = parse_unordered_list(md_parser_list)
    md_parser_list = '\n'.join(md_parser_list).split('\n')

    '''
    Create HTML file and write converted markdown to html tags
    '''
    with open(output_file, 'w') as file:
        for md_symbol in md_parser_list:
            file.write(md_symbol + '\n')


if __name__ == "__main__":
    file_read_write()
