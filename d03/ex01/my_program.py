#!/usr/bin/env python3

from path import Path

def main():
    try:
        Path.mkdir('dir')
    except FileExistsError as e:
        print(e)
    Path.touch('dir/file')
    f = Path('dir/file')
    f.write_text("Hello World!")
    print(f.read_text())

if __name__ == '__main__':
    main()
