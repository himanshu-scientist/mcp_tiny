import boto3
import json
import re
import ast
import asyncio
from starlette.responses import JSONResponse

def call_titan_with_tools(prompt: str, tools: list,region_name="us-east-1"):
    tools_description = "\n".join([f"- {tool}" for tool in tools])
    full_prompt = f"""You are an AI assistant. You can use the following tools:
    {tools_description}

- If you know the answer, respond starting with:
Answer: <your answer here>
- If you cannot answer, respond **only** with:
TOOL_CALL: <tool_name>(<json arguments>)
Example:
Question: What is the similarity between "hello" and "hi"?
Response:
TOOL_CALL: compare_texts({{"text1": "hello", "text2": "hi"}})
Now, answer this question:
{prompt}

    """.strip()
    print("Full Prompt to Titan:", full_prompt)
    bedrock = boto3.client("bedrock-runtime", region_name=region_name)
    payload = {
        "inputText": full_prompt
    }
    MODEL_ID = "amazon.titan-text-express-v1"
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )
    result = json.loads(response['body'].read())
    print("initial response from titan: ", result['results'][0]['outputText'])
    return result['results'][0]['outputText']

region_name="us-east-1"
def llm_agent_call(prompt: str,tool_info="information from called tools"):
    full_prompt = f"""You are an AI assistant. You got pprompt as {prompt}
    now you called one of the tool and you got response as {tool_info}
    Now, response to used based on information you got from tool call.
    """.strip()

    print("Full Prompt to Titan:", full_prompt)
    bedrock = boto3.client("bedrock-runtime", region_name=region_name)
    payload = {
        "inputText": full_prompt
    }
    MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

    # MODEL_ID = "amazon.titan-text-express-v1"
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )
    result = json.loads(response['body'].read())
    print("initial response from titan: ", result['results'][0]['outputText'])
    return result['results'][0]['outputText']


import json
import boto3

region_name = "us-east-1"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"  # Better for chat

def llm_agent_call_1(prompt: str, tool_info="information from called tools"):
    messages = [
        {
            "role": "user",
            "content": f"""
You are an AI assistant. You received this prompt: "{prompt}"

Then you called one of the tools and received the following result:
{tool_info}

Based on this tool result, respond to the user.
""".strip()
        }
    ]

    print("🟢 Claude Prompt Messages:", messages)

    payload = {
        "messages": messages,
        "anthropic_version": "bedrock-2023-05-31",  # required for Claude models
        "max_tokens": 1000,
        "temperature": 0.7
    }

    bedrock = boto3.client("bedrock-runtime", region_name=region_name)

    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response['body'].read())
    final_response = result['content'][0]['text']
    print("🧠 Claude Response:", final_response)
    return final_response
