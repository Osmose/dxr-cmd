#!/usr/bin/env python
"""Run a search against DXR.

Usage: dxr [options] <query>...

Options:
  --case-insensitive  Perform a case-insensitive search (searches are
                      case-sensitive by default).
  --grep              Grep-style "FILE:LINE" output
  -h --help           Show this screen.
  --limit=LIMIT       Maximum number of matches [default: 50]
  --no-highlight      Disable syntax highlighting.
  --pager=PROGRAM     Direct output through PROGRAM.
  --server=DOMAIN     DXR instance to send the search request to.
                      [default: https://dxr.mozilla.org]
  --style=STYLE       Name of Pygments style for syntax highlighting.
                      [default: paraiso-dark]
  --tree=TREE         Code tree to search against.
                      [default: mozilla-central]
  -v --version        Show program version.
"""
import re
import subprocess
from HTMLParser import HTMLParser
from math import ceil, log10

import requests
from blessings import Terminal
from docopt import docopt
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import Terminal256Formatter
from pygments.util import ClassNotFound


__version__ = '0.2.2'


def main():
    arguments = docopt(__doc__, version=__version__)
    html_parser = HTMLParser()
    t = Terminal()
    output = []

    try:
        limit = int(arguments['--limit'])
    except:
        limit = 50  # Sigh. Numbers are so hard to type.

    url = '{server}/{tree}/search'.format(server=arguments['--server'],
                                          tree=arguments['--tree'])
    response = requests.get(url, params={
        'q': ' '.join(arguments['<query>']),
        'redirect': 'false',
        'case': 'false' if arguments['--case-insensitive'] else 'true',
        'limit': limit,
        'offset': 0
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        output.append('Search failed: DXR returned {status} {reason}'.format(
            status=response.status_code,
            reason=response.reason,
        ))
    else:
        grep_style = arguments['--grep']
        response_json = response.json()
        formatter = Terminal256Formatter(style=arguments['--style'])

        if len(response_json['results']) < 1:
            output.append('No results found.')
        else:
            for result in response_json['results']:
                if not grep_style:
                    output.append(t.green(result['path']))

                # Find maximum line number length so we can line them up.
                max_log = max(log10(l['line_number']) for l in result['lines'])
                lineno_len = int(ceil(max_log))
                if grep_style:
                    line_template = (u'{t.green}{path}:{t.yellow}{{lineno}}{t.normal}:{{line}}'
                                     .format(t=t, path=result['path']))
                else:
                    line_template = (u'  {t.yellow}{{lineno:>{lineno_len}}}{t.normal} {{line}}'
                                     .format(t=t, lineno_len=lineno_len))

                try:
                    lexer = get_lexer_for_filename(result['path'])
                except ClassNotFound:
                    lexer = None  # No highlighting for you!

                for line_result in result['lines']:
                    line = html_parser.unescape(line_result['line'])

                    # Find highlight term and remove <b> tags.
                    match = re.search(r'<b>(?P<term>.+)</b>', line)
                    highlight_term = match.group('term') if match else None
                    line = line.replace('<b>', '').replace('</b>', '')

                    # Highlight normally and add underline.
                    if not arguments['--no-highlight'] and lexer:
                        line = highlight(line, lexer, formatter).strip('\n')
                    line = line.replace(highlight_term, t.underline_bold(highlight_term))

                    output.append(line_template.format(
                        lineno=unicode(line_result['line_number']),
                        line=line
                    ))
                if not grep_style:
                    output.append('')

    output = '\n'.join(output)
    if arguments['--pager']:
        p = subprocess.Popen(arguments['--pager'], stdin=subprocess.PIPE, shell=True)
        p.communicate(input=output)
        p.wait()
    else:
        print output


if __name__ == '__main__':
    main()
