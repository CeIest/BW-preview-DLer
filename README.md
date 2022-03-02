# BW preview DLer

bookrunner is a Python script that downloads public preview books on [BookWalker](https://bookwalker.jp/). 

Heavily inspired by [Atemu's repository](https://github.com/Atemu/bookwalker-dl).

Disclaimer: this script does ***NOT*** download or rip the paid ebooks from BookWalker. 

## Installation

Install the required dependencies...
```bash
pip install requests urllib3 click
```
... and simply run the script.
```bash
./bookrunner.py --ID [Book ID here]
```

The book ID can be found in its respective url. 
example: `dee3fcbcd2-ee0a-4c27-b944-8b0aa397ea02`

## To-Do:
* Maybe save more metadata about the book
* Write more stuff about how the script works
