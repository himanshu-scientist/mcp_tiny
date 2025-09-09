import boto3
import json


def llm_get_expected_tool_and_format(prompt: str, tools: list,region_name : str,MODEL_ID: str):
    """
    Calls the Claude LLM via Bedrock to determine which tool (if any) should be used to answer the prompt.
    Returns either a tool call in the format ("tool_name", {args}) or a direct answer.
    Args:
        prompt (str): The user's question or instruction.
        tools (list): List of available tool descriptions.
        region_name (str): AWS region for Bedrock.
        MODEL_ID (str): Bedrock model ID for Claude.
    Returns:
        str: LLM response indicating tool call or direct answer.
    """
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


def llm_respond_user(prompt: str, MODEL_ID : str, region_name: str, tool_info="information from called tools" ):
    """
    Calls the Claude LLM via Bedrock to generate a final user-facing response
    based on the original prompt and the result from a tool call.
    Args:
        prompt (str): The user's original question or instruction.
        MODEL_ID (str): Bedrock model ID for Claude.
        region_name (str): AWS region for Bedrock.
        tool_info (str): Information or result from the tool call.
    Returns:
        str: LLM-generated response to the user.
    """
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
