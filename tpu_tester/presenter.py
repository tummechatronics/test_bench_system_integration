from __future__ import annotations

import re
import time
from typing import Protocol

from tpu_tester.file_handler import csv_generator
from tpu_tester.model import CommunicationUsb, TPUCommunication
from tpu_tester.tpu_tester_steps import check_tpu_inputs, check_can_module

MAX_ATTEMP = 5
tpu_output = "1111"


class View(Protocol):
    # TODO: Add methods

    def __init__(self):
        self.log_widget = None

    def init_ui(self, presenter: Presenter) -> None: ...

    def get_tpu_barcode(self) -> str: ...

    def verify_output_leds(self) -> bool: ...

    def update_log(self, message): ...

    def mainloop(self) -> None: ...

    ...


class Presenter:
    def __init__(
        self, arduino_comm: CommunicationUsb, tpu_comm: TPUCommunication, view: View
    ):
        self.arduino_model = arduino_comm
        self.tpu_model = tpu_comm
        self.view = view

    def _verify_input_tpu_serial_number(self, tpu_serial_number: str) -> bool:
        pattern = r"^\d{7}-\d{5}$"
        if re.match(pattern, tpu_serial_number):
            self.view.update_log(f"{tpu_serial_number}")
            return True
        else:
            self.view.update_log(f"{tpu_serial_number} is not a valid serial number")

    def _validate_results(self, results_data: dict[str, str]) -> str:
        if (
            results_data.get("tpu_inputs_result", "True") == True
            and results_data.get("tpu_outputs_result", "True") == True
        ):
            final_result = "Pass"
        else:
            final_result = "Fail"
        return final_result

    def handle_start_test(self) -> None:
        """
        :return:
        """
        # 1) pop up wait for right TPU Serial Number format
        self.view.update_log(f"Virtual CAN: {self.arduino_model.check_can()}")
        tpu_sn = self.view.get_tpu_barcode()
        while not self._verify_input_tpu_serial_number(tpu_sn):
            tpu_sn = self.view.get_tpu_barcode()
            continue

        # Turn on TPU
        self.view.update_log(f"Turning on TPU")
        time.sleep(3)
        i = 0
        while not self.tpu_model.connected and i < MAX_ATTEMP:
            self.tpu_model.tpu_connect()
            self.view.update_log(f"trying to connect with TPU {i}:{MAX_ATTEMP}")
            i += 1
            time.sleep(0.5)
        # 2) verify tpu can chip number

        tpu_log_file = self.tpu_model.get_logfile()

        if not tpu_log_file["boot_from_internal_storage"]:
            self.tpu_model.tpu_disconnect()
            return self.view.update_log(
                f"TPU booted from USB \n Unplug the USB and restart the test"
            )
        if not tpu_sn == tpu_log_file["serial_number"]:
            self.tpu_model.tpu_disconnect()
            return self.view.update_log(
                f"TPU Serial Number did not match\n"
                f"Given: {tpu_sn} Read from TPU: {tpu_log_file['serial_number']}\n"
                f"Please verify the serial number and restart the test"
            )
        can_module = check_can_module(tpu_log_file["can_module"])
        if can_module:
            self.view.update_log(f"CAN Module: {tpu_log_file['can_module']}")

        # 4) Check TPU inputs
        inputs = self.arduino_model.read_i()
        tpu_inputs_result = check_tpu_inputs(inputs)
        tpu_log_file["tpu_inputs_result"] = tpu_inputs_result
        self.view.update_log(f"TPU inputs: {tpu_inputs_result}")

        # 3) Check TPU outputs
        self.arduino_model.write_o(tpu_output)
        tpu_log_file["tpu_outputs_message"] = tpu_output
        tpu_output_result = self.view.verify_output_leds()
        tpu_log_file["tpu_outputs_result"] = tpu_output_result
        self.view.update_log(f"Output Leds: {tpu_output_result}")
        tpu_log_file["final_result"] = self._validate_results(tpu_log_file)
        csv_generator(tpu_log_file, tpu_sn)
        self.view.update_log(
            f"TPU {tpu_sn}: final result : {tpu_log_file['final_result']}"
        )
        self.view.update_log(f"Teardown")
        self.tpu_model.tpu_disconnect()
        self.arduino_model.start_reset()
        self.view.update_log(f"TPU {tpu_sn} is done \nReady for a new TPU\n")

    def test_result(self, passed):
        if passed:
            self.view.update_result("Pass", "green")
        else:
            self.view.update_result("Fail", "red")

    def run(self) -> None:
        self.view.init_ui(self)
        self.arduino_model._connect()
        self.view.mainloop()
