import os
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
from .file_processor import process_col_files
from .feature_extractor import extract_features

def calc_features(path):
    feature_dict = {}
    lock = threading.Lock()

    def process_instance(file_path, edges, dimension):
        file_name = os.path.basename(file_path)
        features = extract_features(file_name, edges, dimension)
        return {file_name: features}

    def thread_safe_update(features):
        with lock:
            feature_dict.update(features)

    col_data = process_col_files(path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_instance, file_path, edges, dimensions): file_path for file_path, edges, dimensions in col_data}
        for future in futures:
            thread_safe_update(future.result())

    return feature_dict

def generate_feature_file(path, output_filename="InstanceFeatures.csv"):
    features = calc_features(path)

    if not features:
        print("No new instances to process.")
        return

    header = list(next(iter(features.values())).keys())

    with open(output_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for feature_values in features.values():
            writer.writerow(list(feature_values.values()))

    print(f"Feature file saved as {output_filename}")

#to be made more generic
def run():
    path = "./Instances"
    output_filename = "./InstanceFeatures.csv"
    generate_feature_file(path, output_filename)
