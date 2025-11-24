import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dexter.tools import TOOLS

def main():
    print(f"Total tools registered: {len(TOOLS)}")
    for tool in TOOLS:
        print(f"- {tool.name}")

if __name__ == "__main__":
    main()
