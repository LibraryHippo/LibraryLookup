import sys
import flake8.main

sys.argv = ['check', '--max-line-length=120', '--exclude=BeautifulSoup.py,authomatic', '.']


def test_syntax():
    try:
        flake8.main.main()
    except SystemExit, e:
        assert e.code is False


if __name__ == '__main__':
    flake8.main.main()
