#!/usr/bin/python3
from tpu_tester.model import CommunicationUsb, TPUCommunication
from tpu_tester.presenter import Presenter
from tpu_tester.view import View


def main() -> None:
    view = View()
    comm = CommunicationUsb("/dev/ttyUSB0")
    tpu = TPUCommunication("********", "###.###.###.###") # Blacked for confi
    presenter = Presenter(comm, tpu, view)
    presenter.run()


if __name__ == "__main__":
    main()
