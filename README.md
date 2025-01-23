# Thought Emergence Tree: Unraveling Intention Emergence in Large Language Model based Agent Simulation

This repository is associated with our research paper titled "Thought Emergence Tree: Unraveling Intention Emergence in Large Language Model based Agent Simulation" In this paper, we propose Thought Emergence Tree (TETree), a novel analytical architecture that integrates the thought of LLM-basedagents to analyze the behavioral patterns of multiple agents and provides a deeper explanation of social emergence phenomena. This repository includes models we use in our research, provide a simulation program for the takeaway city and related visual emergence analysis code

## Setting Up the Environment

## Step 1. Prepare

To set up your environment, you need run the simulation program under Linux system.we tested our environment on Ubuntu 22.04 LTS and you need get your OpenAI API key. You can fill in your OPENAI_API_KEY in models/agents/LLMAgent.py.

```
os.environ["AZURE_OPENAI_API_KEY"] = "Your openai api"
os.environ["AZURE_OPENAI_ENDPOINT"] = "your ENDPOINT"
```

<br/>

### Step 2. Install requirements.txt

Install everything listed in the requirements.txt file (I strongly recommend first setting up a virtualenv as usual). A note on Python version: we tested our environment on Python 3.8.0

## Running a Simulation

To run a new simulation, You can directly execute the following code in the SocialInvolution/entity/ directory.

```
python city.py
```

You can modify the relevant experimental configuration directly in city.py. The default configuration is 100 agents to simulate and run 3600 steps. The actual running time is more than 6 hours.

After the run is complete, you can run any visualization code in the SocialInvolution/algorithm/drow_echarts directory and get the corresponding emergence analysis results.
