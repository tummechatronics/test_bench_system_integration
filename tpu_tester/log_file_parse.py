def log_file_parser(log_list: list[str]) -> dict[str, str]:
    log_dict = {}
    for line in log_list:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        log_dict |= {key: value}
    return log_dict
