import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

# Load environment variables
load_dotenv()

from dexter.agent import Agent

def main():
    query = "What is the current price of BTC and how has it performed over the last 7 days?"
    print(f"Running query: {query}")
    agent = Agent()
    agent.run(query)

if __name__ == "__main__":
    main()
