# BW preview DLer

bookrunner is a Python script that downloads public preview books on [BookWalker](https://bookwalker.jp/). 

Disclaimer: this script does ***NOT*** download or rip the paid ebooks from BookWalker. 

## Installation

Install the required dependencies...
```bash
pip install requests click
```
... and simply run the script.
```bash
./bookrunner.py [Book ID here]
```

The book ID can be found in its respective url. 
example: `dee3fcbcd2-ee0a-4c27-b944-8b0aa397ea02`

## To-Do:
* Detect and download 'whole' free books that doesn't need login
