import csv
from datetime import datetime
from pathlib import Path


def log_file_parser(log_list: list[str]) -> dict[str, str]:
    log_dict = {}

    for line in log_list:
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.replace(" ", "_").lower().strip()
        value = value.strip()

        if "version" in key and "git hash" in value.lower():
            version, git_hash = value.split("Git Hash:", 1)
            log_dict |= {key: version.strip()}
            git_hash_key = key.replace("version", "git_hash")
            log_dict |= {git_hash_key: git_hash.strip()}
        else:
            log_dict |= {key: value}

    return log_dict


def csv_generator(results_data: dict[str, str], tpu_serial_number: str) -> None:
    parent_path = Path().parent
    results_directory = parent_path / "results"
    results_directory.mkdir(parents=True, exist_ok=True)
    test_date_time = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
    # Extract the keys as column headers
    headers = results_data.keys()

    # Extract the values as a single row
    values = results_data.values()
    with open(
        results_directory.absolute()
        / f"test_result_{test_date_time}_{tpu_serial_number}.csv",
        "w",
        newline="",
    ) as file:
        writer = csv.writer(file, delimiter=",")

        # Write headers
        writer.writerow(headers)

        # Write values
        writer.writerow(values)
