#!/usr/bin/python3
"""
    Parsing bold syntax
"""
if __name__ == "__main__":
    import sys
    from os import path
    import re
    import hashlib

    markD = {"#": "h1", "##": "h2", "###": "h3", "####": "h4", "#####": "h5", "######": "h6", "-": "ul", "*": "ol"}

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    if not path.exists(sys.argv[1]) or not str(sys.argv[1]).endswith(".md"):
        sys.stderr.write("Missing " + sys.argv[1] + '\n')
        exit(1)

    def handleHeadings(pattern):
        tag = markD[lineSplit[0]]
        toWrite = line.replace("{} ".format(lineSplit[0]), "<{}>".format(tag))
        toWrite = toWrite[:-1] + ("</{}>\n".format(tag))
        fw.write(toWrite)

    def inlineMarkdown(line, pattern):
        flag = 0
        while pattern in line:
            if not flag:
                if pattern == "**":
                    line = line.replace(pattern, "<b>", 1)
                    flag = 1
                else:
                    line = line.replace(pattern, "<em>", 1)
                    flag = 1
            else:
                if pattern == "**":
                    line = line.replace(pattern, "</b>", 1)
                    flag = 0
                else: 
                    line = line.replace(pattern, "</em>", 1)
                    flag = 0
        return line

    def md5Markdown(line):
        rep = []
        while "[[" in line and "]]" in line:
            rep = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '[' and line[j + 1] == '[':
                    rep.append(j)
                elif not j == len(line) - 1 and line[j] == "]" and line[j + 1] == ']':
                    rep.append(j)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)
            
            toRep = line[sliceObj]
            toHash = toRep[2:-2]
            md = hashlib.md5(toHash.encode()).hexdigest()
            line = line.replace(toRep, md)
        return line

    def caseMarkdown(line):
        rep = []
        s = ''
        while '((' in line:
            rep = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '(' and line[j + 1] == '(':
                    rep.append(j)
                elif not j == len(line) - 1 and line[j] == ")" and line[j + 1] == ')':
                    rep.append(j)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)
            toRep = line[sliceObj]
            s = toRep
            for char in toRep:
                if char == 'c':
                    toRep = toRep.replace('c', '')
                elif char == 'C':
                    toRep = toRep.replace('C', '')
            line = line.replace(s, toRep[2:-2])
        return line 

    with open(sys.argv[1], mode='r') as fr, open(sys.argv[2], mode='w+') as fw:
        first = 0
        f = 0
        read = fr.readlines()
        for i, line in enumerate(read):
            # For inline markdown
            if "**" in line:
                line = inlineMarkdown(line, "**")
            if "__" in line:
                line = inlineMarkdown(line, "__")
            if "[[" in line and "]]" in line:
                line = md5Markdown(line)
            if "((" in line and "))" in line:
                line = caseMarkdown(line) 
                     
            # split by spaces
            lineSplit = line.split(' ')
            if lineSplit[0] in markD:
                # Headings
                if lineSplit[0].startswith('#'):
                    handleHeadings(lineSplit[0])
                # Lists
                elif lineSplit[0].startswith("-") or lineSplit[0].startswith("*"):
                    tag = markD[lineSplit[0]]
                    #if its the first item list
                    if not first:
                        toWrite = "<{}>\n".format(tag)
                        fw.write(toWrite)
                        first = lineSplit[0]
                    # do every time for '-' or '*'
                    toWrite = line.replace("{} ".format(lineSplit[0]), "<li>")
                    toWrite = toWrite[:-1] + ("</li>\n")
                    fw.write(toWrite)
                    # if its the last item list
                    if i is len(read) - 1 or not read[i + 1].startswith("{} ".format(first)):
                        toWrite = "</{}>\n".format(tag)
                        fw.write(toWrite)
                        first = 0
            else:
                # paragraphs 
                if line[0] != "\n":
                    #first paragraph
                    if not f:
                        fw.write("<p>\n")
                        f = 1
                    fw.write(line)
                    # if next line is part of the paragraph
                    if i != len(read) - 1 and read[i + 1][0] != "\n" and read[i + 1][0] not in markD:
                        fw.write("<br/>\n")
                    else: 
                        fw.write("</p>\n")
                        f = 0
        exit(0)
