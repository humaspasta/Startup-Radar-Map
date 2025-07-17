import pandas as pd

ser = pd.Series([
    "https://www.hadrian.com",                          # Defense manufacturing automation
    "https://www.recursion.com",                        # AI-driven drug discovery
    "https://www.skydio.com",                           # Autonomous drones
    "https://www.perplexity.ai",                        # AI-powered search engine
    "https://cohere.ai",                                # NLP and language models
    "https://deusrobotics.com",                         # Warehouse robotics automation
    "https://graphtx.com",                              # Precision immunotherapy biotech
    "https://www.mistral.ai",                           # European open-source AI models
    "https://pulsetrain.com",                           # Electric powertrain systems
    "https://www.multiversecomputing.com" ]         # Quantum-AI for industry
, name= 'Links')

ser.to_csv('startups.csv')