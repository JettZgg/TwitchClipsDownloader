import warnings
import sys
import os
from typing import Any

def suppress_warnings() -> None:
    # Suppress all warnings
    warnings.filterwarnings("ignore")

    # Suppress Qt warnings
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

    # Redirect stderr to devnull to suppress warnings that can't be caught by the warnings module
    class DevNull:
        def write(self, msg: Any) -> None:
            pass

    sys.stderr = DevNull()  # type: ignore

    # Suppress the secure coding warning
    def custom_formatwarning(*args: Any, **kwargs: Any) -> str:
        return ""

    warnings.formatwarning = custom_formatwarning  # type: ignore
