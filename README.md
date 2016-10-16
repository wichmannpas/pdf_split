PDF split
=========

split
-----

split_half.py splits all pages of a pdf document (except for the first) in the middle to make reading on small screens (like ebook readers) easier.


Usage
-----

To split all pages except for the title page to halfs:

    ./split.py example.pdf example.splitted.pdf

To split all pages except for the title page in three parts:

    ./split.py example.pdf example.splitted.pdf --splits 3

To split all pages except for the title page in four parts and use a margin of 20:

    ./split.py example.pdf example.splitted.pdf --splits 4 --margin 20

To get all available parameters, use:

    ./split.py --help
