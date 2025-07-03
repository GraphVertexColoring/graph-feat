# graph_feature/file_processor.py
# Copyright (c) 2025 Frederik M. Dam
# This file is licensed under the GNU License.
# See the LICENSE file in the project root for full license text.
import os
import shutil
import gzip

def unzip_gz_files(path):
    unzipped_files = []
    for file_name in os.listdir(path):
        if file_name.endswith('.gz'):
            gz_path = os.path.join(path, file_name)
            col_file_name = file_name[:-3]  # remove .gz extension
            col_path = os.path.join(path, col_file_name)

            with gzip.open(gz_path, 'rb') as f_in:
                with open(col_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            unzipped_files.append(col_path)
    return unzipped_files

def read_col_file(file_path):
    edges = []
    dimension = 0

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("p "):
                parts = line.split()
                dimension = int(parts[2])
            elif line.startswith("e "):
                n1, n2 = map(int, line.split()[1:])
                edges.append((n1-1, n2-1))  # Convert to 0-based index

    return edges, dimension


def process_col_files(path):
    unzipped_files = unzip_gz_files(path)
    results = []

    for file_path in unzipped_files:
        edges, dimension = read_col_file(file_path)
        results.append((file_path, edges, dimension))
        os.remove(file_path)  # Clean up unzipped file

    return results