"""Allow webcamlib to be executable through `python -m webcamlib`."""
from __future__ import absolute_import

from .cli_webcam import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="webcamlib")