# PyFileFinder

Python script to find files in a directory that exceed a specified size.
It is inspired by Unix's `find` command but simplified for ease of use in Python environments.

## Features

- Search files by size with various units (e.g., bytes, kilobytes, megabytes).
- Command-line interface for easy usage.

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/PyFileFinder.git
cd PyFileFinder
```

### Examples
```bash
python find_files.py . "10M"
```
This command will search for files larger than 10 megabytes in the current directory.

### Running Tests
Ensure you have the necessary dependencies installed, and run the tests using:

```bash
python -m unittest test_find_files
```
