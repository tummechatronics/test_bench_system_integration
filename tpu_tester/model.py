import time
from typing import AnyStr

import paramiko
import serial

from tpu_tester.file_handler import log_file_parser

MAX_ATTEMP = 5
TPU_LOG_ADD = "/toposens/logs/logs.txt"


class CommunicationUsb:

    def __init__(self, port: str) -> None:
        self.port = port

    def _connect(self) -> None:
        self.ser = serial.Serial(self.port, 9600, timeout=1)

        "Flush the com port to remove start"
        self.__command_send("")
        self.__command_receiver()

    def __command_receiver(self) -> str:
        i = 0
        while i < MAX_ATTEMP:
            m = self.ser.readlines()
            m_decoded = [todec.decode().strip() for todec in m]
            for m_deco in m_decoded:
                if m_deco.startswith(("START", "PASS", "FAIL", "ri")):
                    # Debug
                    print(f"decoded {m_deco}")
                    return m_deco
            i += 1

    def __command_send(self, command: str) -> None:
        self.ser.write(command.encode("utf-8"))
        time.sleep(1)

    def __check_connection(self):
        return self.ser.is_open

    def check_can(self) -> str:
        msg = "ccan"
        self.__command_send(msg)
        return self.__command_receiver()

    def start_reset(self):
        msg = "reset"
        self.__command_send(msg)
        return self.__command_receiver()

    def read_i(self) -> str:
        msg = "ri"
        self.__command_send(msg)
        return self.__command_receiver()

    def write_o(self, outputs: str) -> None:
        """

        :param outputs: can only be can be a bin combination of for digits 0000 upto 1111
        :return:
        """
        msg = "so" + outputs
        self.__command_send(msg)


class TPUCommunication:

    def __init__(self, user: str, address: str):
        self.usr = user
        self.addr = address
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.connected = False

    def tpu_connect(self):
        try:
            self.ssh.connect(f"{self.addr}", username=f"{self.usr}")
            self.sftp_client = self.ssh.open_sftp()
            self.connected = True
        except paramiko.ssh_exception.NoValidConnectionsError as tpu_error:
            print(f"TPU does not have any software \n Please flash it \n {tpu_error}")
        except paramiko.ssh_exception.AuthenticationException as wrong_usr:
            print(
                f"Please verify user: {self.usr} and address: {self.addr} \n error: {wrong_usr}"
            )
        return self

    def tpu_disconnect(self):
        try:
            self.sftp_client.close()
            self.ssh.close()
        finally:
            self.connected = False

    def _get_log_file(self) -> list[AnyStr]:
        return [line.strip() for line in self.sftp_client.open(TPU_LOG_ADD).readlines()]

    def get_logfile(self) -> dict[str, str]:
        return log_file_parser(self._get_log_file())


if __name__ == "__main__":
    com = CommunicationUsb("/dev/ttyUSB0")
    print("scan TPU\n")
    s = input()
    print(s)

    while 1:
        com.check_can()
        com.read_i()
        com.write_o("1011")
        com.start_reset()
