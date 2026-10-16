import subprocess
import json
import sys
import ollama
import argparse

# Path to your manually written MCP server script
SERVER_SCRIPT = "mcp_server.py"
GUI_SCRIPT = "button_gui.py"
OLLAMA_MODEL = "qwen3:8B" # qwen3:8B, llama3.2

# You can reuse your send_message and read_message functions from the previous client script here
def send_message(proc, message_dict):
    """
    Helper function to serialize and send a JSON-RPC message to the server's stdin.
    """
    # Convert 'message_dict' into a JSON string using json.dumps().
    # Write the string to proc.stdin.
    # Append a newline character ('\n').
    # CRITICAL: Call proc.stdin.flush() so the server receives the data immediately.
    json_string = json.dumps(message_dict)
    proc.stdin.write(json_string + "\n")
    proc.stdin.flush()

def read_message(proc):
    """
    Helper function to read and deserialize a JSON-RPC response from the server's stdout.
    """
    # Read a single line from proc.stdout using readline().
    # If line is empty, return None.
    # Parse the line into a Python dictionary using json.loads() and return it.
    new_line = proc.stdout.readline()
    if new_line == '':
        return None
    else:
        return json.loads(new_line)

def mcp_handshake(proc, request_id):
    """
    Send the 'initialize' request and the 'notifications/initialized' confirmation.
    Return the request_id counter so subsequent calls stay synchronized.
    """
    request_dict = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "custom-client", "version": "1.0"}}
        }
    # Send the request using send_message().
    send_message(proc, request_dict)
    # Read the server's response using read_message(). Print or inspect the result.
    response = read_message(proc)
    if VERBOSE:
        print(f"Initialise response\n {response}")
    request_id += 1 

    # 3. Handshake Confirmation: "notifications/initialized"
    # Construct a JSON-RPC 2.0 notification dictionary (NO 'id' field):
    request_dict = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    # Send the notification using send_message().
    send_message(proc, request_dict)
    return request_id + 1

def fetch_and_translate_tools(proc, request_id):
    """
    Fetches the tool schema from the MCP server and translates it for the LLM.
    """
    # 1. Fetch Tools from MCP Server
    request_dict = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/list"
        }
    # Send the request using send_message().
    send_message(proc, request_dict)
    # Read the server's response using read_message() and extract the list of available tools.
    response = read_message(proc)
    tools = response["result"]["tools"]
    if VERBOSE:
        print(f"Tools response\n {tools}")


    # 2. Translate to Ollama Format
    ollama_tools = []
    # Iterate through the tools returned by your MCP server.
    # For each tool, construct a dictionary that matches Ollama's expected tool format:
    # Append the translated dictionary to the ollama_tools list and return it.
    for tool in tools:
        ollama_tools.append({
            "type": "function",
            "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["inputSchema"],
            }        
        }) 
    
    return ollama_tools, request_id + 1

def execute_tool_on_server(proc, request_id, tool_name, tool_arguments):
    """
    Passes the LLM's chosen tool and arguments back down to the MCP server.
    """
    # Construct a JSON-RPC "tools/call" request.
    # Place 'tool_name' and 'tool_arguments' into the "params" dictionary.
    # Send the request to the server and read the response.
    # Extract and return the actual text content from the server's success response.
    request_dict = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,  # or whatever tool name you defined in server.py
                "arguments": tool_arguments
            }
        }
    # Send the request using send_message().
    send_message(proc, request_dict)
    # Read the server's response using read_message() and verify the result.
    return read_message(proc), request_id + 1
   

def main():
    # 0. Launch GUI that LLM will control
    gui_proc = subprocess.Popen([sys.executable, str(GUI_SCRIPT)])
    print("Launched GUI")

    # 1. Start the MCP Server Subprocess
    proc = subprocess.Popen([sys.executable, str(SERVER_SCRIPT)],
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        text=True)
    print("Launched MCP Server")
    request_id = 1
    
    try:
        # 2. Initialize connection and fetch tools
        # Call mcp_handshake(proc).
        print("Initialising MCP Server")
        request_id = mcp_handshake(proc, request_id)
        # TODO: Call fetch_and_translate_tools(proc) to get the list of available tools.
        available_tools, request_id = fetch_and_translate_tools(proc, request_id)
        print("MCP Server Initialised")
        if VERBOSE:
            print(request_id, available_tools)


        # 3. Setup the Chat Loop
        messages = [
            {"role": "system", "content": "You are a helpful AI. You have access to tools. You may only communicate your responses to prompts to the user via the available tools. The user will not be able to see your text response."}
        ]
        
        print("Agent Harness Ready. Type 'exit' to quit.")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
                
            messages.append({"role": "user", "content": user_input})
            
            # 4. Prompt the Local LLM
            # Call ollama.chat(). 
            # Pass your chosen model (e.g., 'llama3.2' or 'qwen2.5'), the 'messages' list, and the 'tools' list you fetched earlier.
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages, 
                tools=available_tools,
            )
            if VERBOSE:
                print(request_id, response)

            
            # 5. Handle the LLM Response
            # Append the LLM's response message object to your 'messages' list.
            # This maintains the agents "Memory" of past events
            messages.append(response.message)

            
            # 6. Check for Tool Calls
            # Check if the LLM's response contains 'tool_calls' (e.g., if response.message.tool_calls exists).
            # TODO: If it DOES contain tool calls:
            #   - Iterate through the tool calls.
            #   - Extract the function name and arguments the LLM wants to use.
            #   - Call execute_tool_on_server() passing those details to your MCP subprocess.
            #   - Build a new dictionary representing the tool's result: {"role": "tool", "content": <the result text from the server>}
            #   - Append this tool result dictionary to your 'messages' list.
            #   - Call ollama.chat() a SECOND time (without passing the user input again) so the LLM can read the tool result and generate a final text response.
            #   - Append this final response to the 'messages' list and print it to the console.
            
            if response.message.tool_calls != None:
                for tool_call in response.message.tool_calls:
                    print(f'Model is using tool: "{tool_call.function.name}", value={tool_call.function.arguments["button_name"]}')
                    tool_name = tool_call.function.name
                    tool_arguments = tool_call.function.arguments
                    response, request_id = execute_tool_on_server(proc, request_id, tool_name=tool_name, tool_arguments=tool_arguments) 
                    if VERBOSE:
                        print(request_id, response)
                    response_tool_dict = {
                        "role": "tool", 
                        "content": response["result"]["content"][0]["text"]
                        }
                    messages.append(response_tool_dict)
                response = ollama.chat(
                    OLLAMA_MODEL,
                    messages
                )
                if VERBOSE:
                    print("tool call was invoked", response.message.content)
                else:
                    print(f'tool call was invoked: {response.message.content}')

                messages.append(response.message)


            # If it DOES NOT contain tool calls:
            #   - Simply print the LLM's text response to the console.
            else:
                print(request_id, response.message.content)
                messages.append(response.message)

    finally:
        # Cleanly terminate the subprocess when exiting.
        print("Full message history: ", messages)
        proc.terminate()
        gui_proc.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='harness',
        description='A custom LLM harness with simple MCP integration',
        epilog='Text'
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    VERBOSE = args.verbose
    main()
