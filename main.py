import os
import fnmatch
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor


def find_files(path: str, extensions: List[str], search_subfolders: bool) -> List[str]:
    matches = []
    for root, _, files in os.walk(path):
        for extension in extensions:
            for name in fnmatch.filter(files, f'*.{extension}'):
                matches.append(os.path.join(root, name))
        if not search_subfolders:
            break
    return matches


def search_and_highlight(text: str, query: str) -> str:
    highlighted = f'\033[93m{query}\033[0m'
    return text.replace(query, highlighted)


def process_file(file_path: str, queries: List[str], case_sensitive: bool) -> List[Tuple[str, int, str]]:
    results = []
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
            break
        except (UnicodeDecodeError, IOError) as e:
            pass
    else:
        return results

    for line_num, line in enumerate(lines, start=1):
        for query in queries:
            if (case_sensitive and query in line) or (not case_sensitive and query.lower() in line.lower()):
                highlighted_line = search_and_highlight(line, query)
                results.append((file_path, line_num, highlighted_line.strip()))

    return results


def search_files(path: str, extensions: str, search_text: str, search_subfolders: bool, case_sensitive: bool, max_workers: int = 8) -> None:
    queries = [query.strip() for query in search_text.split(',')]
    extensions = [extension.strip() for extension in extensions.split(',')]
    file_paths = find_files(path, extensions, search_subfolders)
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, fp, queries, case_sensitive): fp for fp in file_paths}

        for future in futures:
            result = future.result()
            if result:
                results.extend(result)

    for file_path, line_num, highlighted_line in results:
        print(f'{file_path}:{line_num} - {highlighted_line}')


if __name__ == '__main__':
    try:
        directory = input('Enter the directory path: ').strip()
        extensions = input('Enter the file extensions (comma-separated for multiple extensions): ').strip()
        search_text = input('Enter the text to search (comma-separated for multiple queries): ').strip()
        search_subfolders = input('Search in subfolders? (y/n): ').strip().lower() == 'y'
        case_sensitive = input('Case-sensitive search? (y/n): ').strip().lower() == 'y'

        if not (Path(directory).exists() and Path(directory).is_dir()):
            print("Invalid directory path.")
        else:
            search_files(directory, extensions, search_text, search_subfolders, case_sensitive)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting the program.")
