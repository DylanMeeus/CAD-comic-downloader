CAD-Comic downloader
=====

This is a small tool that will download the CAD-comics from a certain year (or, alternatively, all comics starting from 2002).

My main motivation for writing this was to play around with Python a bit. I do encourage you to support Tim (the author of CAD-comic) on patreon if you like the comics. Downloading them to your hard drive - whilst handy to read when not connected to the internet - does prevent Tim from earning revenue through cad-comic.


Usage of this CLI script: `python main.py [year]`.

For example, to download the archive for 2004: `python main.py 2004`.
If you want to download the entire archive, you can use _all_ instead of a year: `python main.py all`.

In case you want to download all of the comics starting with a certain year, you can append a year after the `all` parameter: `python main.py all 2006`. This will then start downloading all the comics, starting with the archive for 2006.