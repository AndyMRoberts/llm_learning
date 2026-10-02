import subprocess
import json
import sys
from pathlib import Path

# Path to your manually written MCP server script
SERVER_SCRIPT = Path(__file__).with_name("mcp_server.py")

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

def main():
    # 1. Spawn the MCP Server Process
    # TODO: Use subprocess.Popen to launch 'sys.executable' running 'SERVER_SCRIPT'.
    # TODO: Set stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True (or bufsize=1).
    proc = subprocess.Popen([sys.executable, str(SERVER_SCRIPT)],
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        text=True)
    
    request_id = 1

    try:
        # 2. Handshake Phase: "initialize"
        # Construct a JSON-RPC 2.0 request dictionary for "initialize":
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

        # 4. Tool Discovery: "tools/list"
        # Construct a JSON-RPC 2.0 request dictionary for "tools/list":
        request_dict = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/list"
        }
        # Send the request using send_message().
        send_message(proc, request_dict)
        # Read the server's response using read_message() and extract the list of available tools.
        response = read_message(proc)
        tools = response["result"]["tools"][0]
        print(f"Tools response\n {tools}")
        request_id += 1

        # 5. Tool Execution: "tools/call"
        # Simulate the LLM deciding to call the tool based on a prompt (e.g., "Press the button to Destroy All Humans"):
        # Construct a JSON-RPC 2.0 request dictionary for "tools/call":
        request_dict = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": "press_button",  # or whatever tool name you defined in server.py
                "arguments": {"button_name": "yes"}
            }
        }
        # Send the request using send_message().
        send_message(proc, request_dict)
        # Read the server's response using read_message() and verify the result.
        response = read_message(proc)
        print(f"Call response\n {response}")

    finally:
        # 6. Clean Up
        # Terminate or kill the server process using proc.terminate() or proc.kill().
        proc.terminate()

if __name__ == "__main__":
    main()