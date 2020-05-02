#!/usr/bin/env python3
import ui
import uuid
import sys


unique_id = str(uuid.uuid4())[:8]
print("Generated id: ", unique_id)

try:
    grabber = ui.UI(unique_id)
    grabber.build_ui()
except Exception as ex:
    print("Exception: ", ex)
    sys.exit(0)

