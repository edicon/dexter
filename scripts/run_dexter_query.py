import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

from dexter.agent import Agent

def main():
    query = "What was Apple's revenue growth over the last 4 quarters?"
    print(f"Running query: {query}")
    agent = Agent()
    agent.run(query)

if __name__ == "__main__":
    main()
