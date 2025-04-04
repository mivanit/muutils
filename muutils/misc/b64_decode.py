from sys import argv
from pathlib import Path
from base64 import b64decode

if __name__ == "__main__":
    input_file: Path = Path(argv[1])
    out: Path = Path(argv[2])
    input_text: str = input_file.read_text().replace("\n", "")
    out.write_bytes(b64decode(input_text))
