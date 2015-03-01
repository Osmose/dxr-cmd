DXR Command-line Tool
=====================

A small command-line tool for searching `DXR <https://dxr.mozilla.org/>`_.


Install
-------

::

    pip install https://github.com/Osmose/dxr-cmd.git


Usage
-----

Adds a command called `dxr`:

::

    Run a search against DXR.

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


Developer Setup
---------------

1. Use a `virtualenv <https://virtualenv.pypa.io/en/latest/>`_!
2. Install the package in development mode::

    $ ./setup.py develop


License
-------
This software is licensed under the
`MIT License <http://opensource.org/licenses/MIT>`_. For more information, see
the ``LICENSE`` file.
