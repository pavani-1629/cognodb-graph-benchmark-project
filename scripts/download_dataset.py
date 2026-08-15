from pathlib import Path
import urllib.request


URL = "https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz"

OUTPUT_DIR = Path("data/raw")
OUTPUT_FILE = OUTPUT_DIR / "soc-pokec-relationships.txt.gz"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        print("Dataset already exists.")
        return

    print("Downloading Pokec dataset...")
    print(URL)

    urllib.request.urlretrieve(URL, OUTPUT_FILE)

    print(f"Downloaded to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()