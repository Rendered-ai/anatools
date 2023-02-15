"""anatools is Rendered.ai’s SDK for connecting to the Platform API. 

- The ``anatools.anaclient`` package exposes the Platform API to the User. Everything that a user can do through the Platform Web Interface can be done via the SDK through the ``anatools.anaclient`` package.
- The ``anatools.annotations`` package allows a User to generate annotations locally without the need for the Platform.
- The ``anatools.lib`` package and ``anatools.nodes`` package are used for Channel developers. More info to come!

The SDK's submodule methods are all exposed to the user, so the full path is not required to call a specific method. 

View the `Introduction to Rendered.ai Documentation`_ to learn more.

.. _Introduction to Rendered.ai Documentation:
        https://support.rendered.ai/gc/Introduction-to-Rendered.ai.1577812005.html

"""

from .anaclient.anaclient import client
from .annotations.annotations import annotations

__version__ = '2.2.0.4'
