from doctr.file_utils import is_tf_available, is_torch_available

from .base import *

if is_torch_available():
    from .pytorch import *  # type: ignore[misc]
elif is_tf_available():
    from .tensorflow import *  # type: ignore[misc]
