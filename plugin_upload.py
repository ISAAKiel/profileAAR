#!/usr/bin/env python
# coding=utf-8
"""Deprecated helper script retained for compatibility.

The original generated uploader script had indentation errors after Python 3 conversion.
For QGIS 4 compatibility packaging it is intentionally kept as a harmless stub;
use the QGIS plugin repository web interface or current QGIS packaging tools to upload.
"""


def main(*args, **kwargs):
    raise RuntimeError(
        "plugin_upload.py is deprecated. Upload the packaged ZIP via the QGIS plugin repository web interface."
    )


if __name__ == "__main__":
    main()
