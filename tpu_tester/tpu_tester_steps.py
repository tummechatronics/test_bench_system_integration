def check_can_module(tpu_value: str) -> bool:
    tpu_can_module = r"MCP2518FD"
    return tpu_value == tpu_can_module


def check_tpu_inputs(inputs: str) -> bool:
    inputs = inputs.split("ri")[1]
    only_ouput_3_ena = "0010"
    return inputs == only_ouput_3_ena
