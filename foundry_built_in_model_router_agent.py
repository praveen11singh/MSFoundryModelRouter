import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()


my_endpoint = os.environ["AI_PROJECT_DEPLOYMENT_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=my_endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "pk-modelrouter-agent"
my_version = "1"

openai_client = project_client.get_openai_client()

# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

response1 = openai_client.responses.create(
    input=[{"role": "user", "content": "A train leaves London at 09:00 travelling at 120 mph. "
            "Another leaves Edinburgh (400 miles away) at 10:00 travelling at 80 mph toward London. "
            "At what time do they meet, and how far from London?"}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

response2 = openai_client.responses.create(
    input=[{"role": "user", "content": "Write a two-paragraph short story about an astronaut who discovers a library on Mars."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

#print(f"Response output: {response.output_text}")

#print(f"Response output: {response1.output_text}")

print(f"Model used output: {response1.model} and {response2.model} and {response.model}")



