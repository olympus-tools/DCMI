r"""
________________________________________________________________________
|                                                                      |
|               $$$$$$$\   $$$$$$\  $$\      $$\ $$$$$$\               |
|               $$  __$$\ $$  __$$\ $$$\    $$$ |\_$$  _|              |
|               $$ |  $$ |$$ /  \__|$$$$\  $$$$ |  $$ |                |
|               $$ |  $$ |$$ |      $$\$$\$$ $$ |  $$ |                |
|               $$ |  $$ |$$ |      $$ \$$$  $$ |  $$ |                |
|               $$ |  $$ |$$ |  $$\ $$ |\$  /$$ |  $$ |                |
|               $$$$$$$  |\$$$$$$  |$$ | \_/ $$ |$$$$$$\               |
|               \_______/  \______/ \__|     \__|\______|              |
|                                                                      |
|                     DCMI (*.dcm file interface) (c)                  |
|______________________________________________________________________|

Copyright 2025 olympus-tools contributors. Dependencies and licenses
are listed in the NOTICE file:

    https://github.com/olympus-tools/DCMI/blob/master/NOTICE

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License:

    https://github.com/olympus-tools/DCMI/blob/master/LICENSE
"""

import os
import sys


def typechecked_dev(func):
    """Applies typeguard's @typechecked only in development mode.

    In production or frozen environments (PyInstaller), this decorator
    does nothing, allowing the code to run without runtime type checking.

    Use ARES_DISABLE_TYPEGUARD=1 to disable type checking explicitly.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function (with or without type checking).
    """
    # Check if we're in a frozen (PyInstaller) environment or if explicitly disabled
    is_frozen = getattr(sys, "frozen", False)
    is_disabled = os.environ.get("ARES_DISABLE_TYPEGUARD", "0") == "1"

    if is_frozen or is_disabled:
        # Return function unchanged
        return func
    else:
        # Apply typeguard in development
        from typeguard import typechecked

        return typechecked(func)
