import time

import ui
import uuid
import sys
import soundextractor

#   todo add sound processing - removing pauses

unique_id = str(uuid.uuid4())[:8]
print("Generated id: ", unique_id)

try:

    grabber = ui.UI(unique_id)
    grabber.build_ui()
    time.sleep(0.5)
    processor = soundextractor.SoundExtractor(unique_id)
    processor.extract_key_presses()

except Exception as ex:
    print("Silly me", ex)
    sys.exit(0)

