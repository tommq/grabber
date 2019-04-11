import time

import ui
import uuid
import sys
import soundextractor
import subprocess

unique_id = str(uuid.uuid4())[:8]
print("Generated id: ", unique_id)

try:
    grabber = ui.UI(unique_id)
    grabber.build_ui()
    time.sleep(0.5)
    # processor = soundextractor.SoundExtractor(unique_id)
    # processor.extract_key_presses()
    subprocess.call(["/media/tomek/Windows/Users/Tomek/Documents/DATA/School/Master thesis/Skype-Type/generate_model.py",
                   "/media/tomek/Windows/Users/Tomek/Documents/DATA/School/Master thesis/grabber/resources/recordings/"+ unique_id +".wav",
                   "/media/tomek/Windows/Users/Tomek/Documents/DATA/School/Master thesis/grabber/resources/models/MODEL"])
except Exception as ex:
    print("Silly me", ex)
    sys.exit(0)

