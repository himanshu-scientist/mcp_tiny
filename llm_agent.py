import boto3
import json
import re
import ast
import asyncio
from starlette.responses import JSONResponse



def llm_get_expected_tool_and_format(prompt: str, tools: list,region_name="us-east-1"):
    tools_description = "\n".join([f"- {tool}" for tool in tools])
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI assistant. You received this prompt: "{prompt}"
            and tools:
            {tools_description}
            if you can not answer the question directly check in "tools_description"
            if any tool can be used to answer this.
            If yes then respond the tool name and arguments in below format **only**:
            ("tool_name", {{"arg1": "value1", "arg2": "value2"}})
            refer below examples.:
            example 1:
            question : find consine similarity btween "hello" and hi
            response: ("compare_texts", {{"text1": "hello", "text2": "hi"}})
            example 2: 
            question : can you embed the text "i am good"
            response : ("embed_text", {{"text": "i am a good}})

            note : response should not have any other charcher, because that response will be parsed to call the tool.
            note2 : Based on the given tools and their descriptions if none of them seem directly relevant to answering the question you are free to use your knowledge to answer the question. in that case :
                your answer should start with : --- NO_Tool_Used ----
                then your answer
                example :
                question : what is the capital of india
                response : --- NO_Tool_Used ----
                The capital of India is New Delhi.
            """.strip()
        }
    ]

    print("llm_agnet-final prompt for Claude model responding to user as", messages)

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
    print("llm_agent final Claude Response:", final_response)
    return final_response





def llm_get_expected_tool_and_format_1(prompt: str, tools: list,region_name="us-east-1"):


    tools_description = "\n".join([f"- {tool}" for tool in tools])
    full_prompt = f"""You are an AI assistant. You can use the following tools:
    {tools_description}

    - check if you need any help from tools to answer the question.
    - to answer, respond **only** in **below** accepted format by respected tools
    refer below examples.:
    Example 1: ("add", {{"a": 8, "b": 13}})
    example 2: ("compare_texts", {{"text1": "hello", "text2": "hi"}})
    example 3: ("embed_text", {{"text": "i am a good}})
    example 4: ("multiply", {{"a": 10, "b": 22}})
    example 5: ("reverse_string", {{"s": "Hello, World!"}})
    example 6: ("count_words", {{"s": "This is a test string."}})
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
    print("llm_agent initial response from titan: ", result['results'][0]['outputText'])
    return result['results'][0]['outputText']




region_name = "us-east-1"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"  # Better for chat

def llm_respond_user(prompt: str, tool_info="information from called tools"):
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI assistant. You received this prompt: "{prompt}"
            Then you called one of the tools and received the following result:
            {tool_info}
            Based on prompt received from user and tool result, respond to the user.
            """.strip()
        }
    ]

    print("llm_agnet-final prompt for Claude model responding to user as", messages)

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
    print("llm_agent final Claude Response:", final_response)
    return final_response

