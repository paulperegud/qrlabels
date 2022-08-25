Quick and dirty tool capable of generating pages of qrcodes. Tested on Linux only.

Written in python, uses poetry. Immediate output is tex files. To obtain pdf files, consider using `pdflatex`.

To add anything extra to QR codes, or customize number of qr codes on a page, modify `priv/page.tex` file.

Input file (or stdin) should contain one url per line.

Example execution:
```
$ poetry run python3 qrlabels/labels.py -t priv/page.tex -o test/ urls.raw
```

## generating tokens / urls

```bash
for i in $(seq 1 1 100); do ./gentoken.sh ; done > tokens.raw

echo "qr_code" > tokens.csv
cat tokens.raw >> tokens.csv

cat tokens.raw | while read line; do echo "https://example.com/?id=$line"; done > urls.raw
```
