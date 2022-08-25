import csv
import re
from pathlib import Path
import tempfile

import qrcode
import click

@click.argument("data")
@click.option("-t", "template", type=click.Path(exists=True, file_okay=True, dir_okay=False), help="Page template to use")
@click.option("-o", "output", type=click.Path(exists=True, file_okay=False, dir_okay=True), help="Output directory")
@click.command()
def main(data, template, output):
    urls = []
    files = []
    splitted = []
    perpage = None
    rootdir = Path(template).parent

    def get_fn(files, i):
        try:
            return files[i]
        except IndexError:
            return rootdir / 'nofile.png'

    dir = Path(tempfile.mkdtemp())
    with open(template) as tf:
        tf = tf.read()
        x = re.findall(r'code.png', tf)
        perpage = len(x)
        print(f'Page will contain {perpage} qr codes per page')
        splitted = re.split(r'code.png', tf)
    with open(data) as f:
        for line in f.readlines():
            line = line.rstrip()
            urls.append(line)
    for c, url in enumerate(urls):
        fn = prepare_qrcode_file(c, dir, url)
        files.append(fn)
    for pageno, chunks in enumerate(divide_chunks(files, perpage)):
        with open(Path(output) / f'page_{str(pageno)}.tex', 'w') as page:
            for i in range(perpage):
                page.write(splitted[i])
                fn = get_fn(chunks, i)
                page.write(str(fn))
            page.write(splitted[perpage])
    print("Done. Consider using pdflatex to convert tex into pdf.")


def prepare_qrcode_file(counter, loc, url):
    img = qrcode.make(url)
    path = Path(loc) / (str(counter) + ".png")
    img.save(path)
    return path

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    main()
