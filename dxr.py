#!/usr/bin/env python
"""Run a search against DXR.

Usage: dxr [options] <query>...

Options:
  --case-insensitive  Perform a case-insensitive search (searches are
                      case-sensitive by default).
  -h --help           Show this screen.
  --limit=LIMIT       Maximum number of matches [default: 50]
  --pager=PROGRAM     Direct output through PROGRAM.
  --server=DOMAIN     DXR instance to send the search request to.
                      [default: https://dxr.mozilla.org]
  --tree=TREE         Code tree to search against.
                      [default: mozilla-central]
  -v --version        Show program version.
"""
import subprocess
from HTMLParser import HTMLParser
from math import ceil, log10

import requests
from blessings import Terminal
from docopt import docopt


__version__ = '0.1'


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
        'redirect': False,
        'format': 'json',
        'case': not arguments['--case-insensitive'],
        'limit': limit,
        'offset': 0
    })

    if response.status_code != 200:
        output.append('Search failed: DXR returned {status} {reason}'.format(
            status=response.status_code,
            reason=response.reason,
        ))
    else:
        response_json = response.json()
        for result in response_json['results']:
            output.append(t.green(result['path']))

            # Find maximum line number length so we can line them up.
            max_log = max(log10(l['line_number']) for l in result['lines'])
            lineno_len = int(ceil(max_log))
            line_template = (u'  {t.yellow}{{lineno:>{lineno_len}}}{t.normal} {{line}}'
                             .format(t=t, lineno_len=lineno_len))

            for line_result in result['lines']:
                # Remove HTML entities and underline properly.
                line = html_parser.unescape(line_result['line'])
                line = line.replace('<b>', t.underline).replace('</b>', t.normal)

                output.append(line_template.format(
                    lineno=unicode(line_result['line_number']),
                    line=line
                ))
            output.append('')
        else:
            output.append('No results found.')

    output = '\n'.join(output)
    if arguments['--pager']:
        p = subprocess.Popen(arguments['--pager'], stdin=subprocess.PIPE, shell=True)
        p.communicate(input=output)
        p.wait()
    else:
        print output


if __name__ == '__main__':
    main()
