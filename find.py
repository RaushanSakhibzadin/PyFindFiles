import argparse
import os


def file_size_over_than(file_path: str, size: str) -> bool:
    """Check if the file at `file_path` exceeds a specified size."""
    size_units = {
        'b': 512,  # 512-byte blocks
        'c': 1,  # bytes
        'w': 2,  # two-byte words
        'k': 1024,  # kilobytes
        'M': 1024 ** 2,  # megabytes
        'G': 1024 ** 3  # gigabytes
    }
    size_value, unit = int(size[:-1]), size[-1]
    if unit in size_units:
        try:
            file_size = os.path.getsize(file_path)
        except OSError as e:
            print(f"Error accessing file {file_path}: {e}")
            return False
        return file_size > size_value * size_units[unit]
    else:
        raise ValueError(f"Invalid size unit. Valid units are: 'b', 'c', 'w', 'k', 'M', 'G'.")


def find_files(start_dir: str, criteria: str) -> list:
    """Find all files in the specified directory that meet the given size criteria."""
    result_files = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if file_size_over_than(full_path, criteria):
                result_files.append(full_path)
    return result_files


def main():
    parser = argparse.ArgumentParser(description='Search for files exceeding a specified size.')
    parser.add_argument('start_dir', type=str, nargs='?', default='.',
                        help='Directory to start searching from. Default is the current directory.')
    parser.add_argument('criteria', type=str, nargs='?', default='1c',
                        help='Size criteria such as 1c, 10k, 5M. Default is 1 byte.')
    args = parser.parse_args()

    files = find_files(args.start_dir, args.criteria)
    if files:
        for file in files:
            print(file)
    else:
        print("No files found that meet the criteria.")


if __name__ == '__main__':
    main()
