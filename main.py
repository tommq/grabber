import grabber
import uuid
import sys
import processor

#   todo add sound processing - removing pauses

unique_id = str(uuid.uuid4())[:8]
print(unique_id)

try:

    processor = processor.Processor("5f8da151")
    processor.extract_key_presses()
    grabber = grabber.Grabber(unique_id)
    grabber.build_ui()

except Exception:
    sys.exit(0)

