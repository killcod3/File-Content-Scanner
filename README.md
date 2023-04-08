# File Content Scanner

This Python script allows you to search for specific text or phrases within a given directory and specified file types. It supports searching in subfolders, case-sensitive search, and searching for multiple queries at once. The script also highlights the searched text in the output.

## Features

- Search for multiple text queries at once
- Specify file types to search in
- Supports searching in subfolders
- Case-sensitive search option
- Highlights the searched text in the output
- Utilizes multithreading for faster search results

## Requirements

- Python 3.6 or higher

## Usage

1. Clone the repo.
2. Open a terminal or command prompt and navigate to the directory containing the `main.py` file.
3. Run the script with `python main.py`.
4. Follow the prompts to enter the directory path, file extensions, search text, and search preferences (subfolders and case-sensitivity).

## Example

```bash
$ python text_search.py
Enter the directory path: /path/to/search
Enter the file extensions (comma-separated for multiple extensions): txt,log
Enter the text to search (comma-separated for multiple queries): error,warning
Search in subfolders? (y/n): y
Case-sensitive search? (y/n): n
```

## License

This project is licensed under the MIT License.
