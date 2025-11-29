<img width="2874" height="1654" alt="IsRoniAround" src="https://github.com/user-attachments/assets/40f76dee-bf1c-443b-b2e6-bd9c017f26e6" />
<img width="2874" height="1654" alt="IsRoniAround" src="https://github.com/user-attachments/assets/24dcbfb4-39d6-431a-8aba-2282d74662c6"/>


# HuskyLens2MCP
Command line interface with Huskylens2 MCP Server using Google Gemini AI

# Requirements
DFRobot Huskylens2 with 1.1.6 firmware or later
Google Gemini API Key
Python

# Instructions
Enable WiFi and connect
Enable MCP server and get the IP
Open the .py, enter your Google API key and the MCP server IP
Run with python HuskyMCPChat.py

# Huskylens MCP Tools
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_recognition_result",
        "description": "Get recognition result support operation method [get_result], Obtain the real-time recognition result from HuskyLens. This includes both image data and recognized labels (e.g., person name or object type). Useful for visual reasoning or generating natural-language descriptions of what the camera sees",
        "inputSchema": {
          "properties": {
            "operation": {
              "type": "string",
              "description": "Operation to perform (get_result [What did you see? Get real-time result with photo])"
            }
          },
          "type": "object",
          "required": [
            "operation"
          ]
        }
      },
      {
        "name": "manage_applications",
        "description": "Manage all internal applications(algorithms) of the Huskylens",
        "inputSchema": {
          "properties": {
            "operation": {
              "type": "string",
              "description": "Operation to perform (current_application, switch_application, application_list). To switch algorithms, you must first call this tool with operation='application_list' to retrieve the valid algorithm names, then use the exact English name from that list. This step is required even if you think you already know the name. If you skip listing first, the switch may fail. "
            },
            "algorithm": {
              "type": "string",
              "description": "application(algorithm) english name"
            }
          },
          "type": "object",
          "required": [
            "operation"
          ]
        }
      },
      {
        "name": "multimedia_control",
        "description": "Control the HuskyLens multimedia components, such as the camera",
        "inputSchema": {
          "properties": {
            "operation": {
              "type": "string",
              "description": "Operation to perform (take_photo)"
            }
          },
          "type": "object",
          "required": [
            "operation"
          ]
        }
      },
      {
        "name": "task_scheduler",
        "description": "Manage scheduled tasks, call this tool when you need to create a task, e.g. 'Take a picture when you see the keyboard' 'Take a picture after 3 seconds' 'Take a picture after 5 seconds when you see the keyboard'. operation: create / list. tasks: array of objects, each object has:trigger (string, optional, trigger name, e.g., 'tiger') handler (string, required, function to execute, only support take_photo)time (string, optional, HH:MM:SS for scheduled time).example:  \"operation\": \"create\",  \"tasks\": [    [\"trigger\", \"tiger\"],    [\"handler\", \"take_photo\"]  ]}",
        "inputSchema": {
          "properties": {
            "operation": {
              "type": "string",
              "description": "Operation to perform (create/list)"
            },
            "tasks": {
              "type": "array",
              "description": "List of tasks to execute. Each task object has:  trigger (string, optional), handler (string, required),   timestamp (string[UTC format or 'now'], optional).For example, if the system recognizes 'Lily', the trigger should be 'Lily', not 'lily' or 'LILY'.When the user says 'Take a photo when you see a kEyboArd', the trigger should be 'kEyboArd',not 'kEyboArd_detected' or 'kEyboArd_recognized'. Always use the simplest, exact trigger name as recognized by the system (e.g., 'face', 'cat', 'person', 'Lily')",
              "items": {
                "type": "json"
              }
            }
          },
          "type": "object",
          "required": [
            "operation",
            "tasks"
          ]
        }
      }
    ]
  }
}

# Contact
@ronibandini Buenos Aires, Argentina
