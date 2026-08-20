<img width="2874" height="1654" alt="IsRoniAround" src="https://github.com/user-attachments/assets/40f76dee-bf1c-443b-b2e6-bd9c017f26e6" />
<img alt="IsRoniAround" src="https://github.com/user-attachments/assets/24dcbfb4-39d6-431a-8aba-2282d74662c6"/>
# 👁️🤖 HuskyLens2MCP

**Command-line AI interface for the HUSKYLENS 2 MCP Server using Python and Google Gemini.**

HuskyLens2MCP connects a **DFRobot HUSKYLENS 2 AI Vision Sensor** directly to **Google Gemini** through the camera's built-in **Model Context Protocol (MCP) Server**.

The project provides a lightweight Python command-line client that can query the camera, switch vision algorithms, capture photos, retrieve recognition results, and combine those results with an LLM for natural-language visual reasoning.

Instead of sending the complete camera stream to Gemini, the client retrieves **structured recognition data from HUSKYLENS 2** and gives that information to Gemini for interpretation.

---

## ✨ Features

* 👁️ Connects directly to the HUSKYLENS 2 MCP Server
* 🤖 Google Gemini integration
* 🧠 Uses `gemini-2.5-flash` for reasoning
* 📡 Network communication over Wi-Fi
* 🔌 MCP over SSE and JSON-RPC
* 📋 Lists available HUSKYLENS algorithms
* 🔎 Shows the currently active algorithm
* 🔄 Switches vision algorithms from the terminal
* 👀 Retrieves real-time recognition results
* 💬 Ask natural-language questions about what the sensor sees
* 📝 Generate natural-language descriptions of recognition data
* 📸 Trigger photo capture remotely
* 🐍 Pure Python client
* 📜 MIT licensed

---

## 🧠 Why MCP?

**MCP — Model Context Protocol** provides a standardized way for AI applications to interact with external tools and data sources.

HUSKYLENS 2 includes an MCP Server that exposes parts of the camera as callable tools.

Instead of building a custom API for every vision feature, an external program can interact with operations such as:

```text
get_recognition_result
manage_applications
multimedia_control
task_scheduler
```

This project implements a Python client for that server and adds Gemini as a reasoning layer.

---

## ⚙️ Architecture

```text
┌──────────────────────────────┐
│       HUSKYLENS 2            │
│                              │
│ • Object Recognition         │
│ • Face Recognition           │
│ • Object Tracking            │
│ • OCR                        │
│ • Pose Recognition           │
│ • Custom models              │
│ • Other vision algorithms    │
│                              │
│        MCP Server            │
└──────────────┬───────────────┘
               │
               │ Wi-Fi
               │ SSE + JSON-RPC
               ▼
┌──────────────────────────────┐
│     huskyMcpChat.py          │
│                              │
│ • MCP client                 │
│ • Algorithm control          │
│ • Recognition retrieval      │
│ • Photo commands             │
│ • CLI                        │
└──────────────┬───────────────┘
               │
               │ Recognition JSON
               ▼
┌──────────────────────────────┐
│      Google Gemini           │
│      gemini-2.5-flash        │
│                              │
│ • Interpretation             │
│ • Natural-language answers   │
│ • Contextual reasoning       │
└──────────────────────────────┘
```

This architecture combines two different types of AI:

**HUSKYLENS 2**

```text
Specialized computer vision
↓
Detects what is in the scene
```

**Gemini**

```text
Language + reasoning
↓
Interprets what the detections mean
```

---

## 👁️ Recognition + reasoning

For a command such as:

```text
ask Is there anything dangerous on the table?
```

the workflow is:

```text
Camera
  ↓
HUSKYLENS recognition algorithm
  ↓
Structured recognition data
  ↓
Python MCP client
  ↓
Gemini
  ↓
Natural-language answer
```

The Python client explicitly instructs Gemini to answer based on the sensor evidence provided to it.

This makes it possible to transform low-level recognition output into more useful questions such as:

```text
ask Is there a person?
```

```text
ask What objects are visible?
```

```text
ask Is the person standing near the table?
```

The quality of the answer ultimately depends on the recognition data returned by the currently selected HUSKYLENS algorithm.

---

## 🧰 Requirements

### Hardware

* **DFRobot HUSKYLENS 2**
* Computer capable of running Python
* Wi-Fi network accessible by both devices

HUSKYLENS 2 product information:

**[DFRobot HUSKYLENS 2](https://www.dfrobot.com/product-2995.html)**

Official documentation:

**[HUSKYLENS 2 Wiki](https://wiki.dfrobot.com/sen0638/)**

---

### Software

* Python 3
* `aiohttp`
* `google-genai`
* Google Gemini API key

Install the Python dependencies:

```bash
pip install aiohttp google-genai
```

---

## 🔑 Gemini API key

Create a Gemini API key using Google AI Studio:

**[Google AI Studio — API Keys](https://aistudio.google.com/app/api-keys)**

The current script expects the key in:

```python
GEMINI_API_KEY = ""
```

Example:

```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

> 🔐 Do not publish or commit a real API key to a public repository.

---

## 📡 Configure HUSKYLENS 2

### 1. Update the firmware

The original project was developed using MCP-capable HUSKYLENS 2 firmware starting with version:

```text
1.1.6
```

The latest firmware and update instructions are available from:

**[HUSKYLENS 2 Firmware / Documentation](https://wiki.dfrobot.com/sen0638/)**

### Firmware compatibility note

DFRobot community reports later identified MCP problems with firmware `1.2.1`, including algorithm-switching and recognition-data errors.

DFRobot subsequently stated that **firmware 1.2.2 fixes MCP instability issues and adds additional tools**.

If you encounter unexpected MCP errors, update to a current firmware release and consult the latest DFRobot documentation.

---

### 2. Connect HUSKYLENS 2 to Wi-Fi

On the camera:

1. Open **Settings**.
2. Configure Wi-Fi.
3. Connect to your local network.
4. Enable the **MCP Server**.

Official MCP documentation:

**[HUSKYLENS 2 MCP Server — DFRobot Wiki](https://wiki.dfrobot.com/sen0638/docs/22605)**

---

### 3. Get the MCP Server address

When MCP is enabled, HUSKYLENS displays the server address.

It typically uses port:

```text
3000
```

For example:

```text
http://192.168.1.100:3000
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/ronibandini/HuskyLens2MCP.git
cd HuskyLens2MCP
```

Install dependencies:

```bash
pip install aiohttp google-genai
```

Open:

```text
huskyMcpChat.py
```

and configure:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
SERVER_URL = "http://192.168.1.100:3000"
```

Replace the IP address with the address displayed by your HUSKYLENS 2.

Then run:

```bash
python huskyMcpChat.py
```

---

## 💻 Command-line interface

After connecting successfully, the client displays:

```text
========================================
 Huskylens2 MCP Command Line
 Roni Bandini 11/2025
 MIT License
========================================
 1. list : List algorithms
 2. current : Show active algorithm
 3. switch <Algorithm> : Switch algorithm
 4. ask <Question> : Ask AI about the view
 5. see : General AI description
 6. photo : Take photo
 7. exit : Quit
----------------------------------------
```

---

## 📋 Commands

### `list`

Retrieve the algorithms available on HUSKYLENS 2:

```text
list
```

Internally this calls:

```text
manage_applications
operation: application_list
```

---

### `current`

Show the active vision algorithm:

```text
current
```

Internally:

```text
manage_applications
operation: current_application
```

---

### `switch`

Switch the active computer-vision algorithm:

```text
switch FaceRecognition
```

Internally:

```text
manage_applications
operation: switch_application
```

The exact algorithm name should match one returned by:

```text
list
```

---

### `ask`

Ask Gemini a question using the current HUSKYLENS recognition results as context:

```text
ask Is there a person?
```

Another example:

```text
ask Is there anything dangerous on the table?
```

The client first calls:

```text
get_recognition_result
operation: get_result
```

and then passes the returned recognition data together with the question to Gemini.

---

### `see`

Generate a short natural-language description of the current recognition result:

```text
see
```

or:

```text
look
```

The script retrieves the current sensor data and asks Gemini to briefly describe what is visible.

---

### `photo`

Trigger a photo capture:

```text
photo
```

or:

```text
snap
```

Internally:

```text
multimedia_control
operation: take_photo
```

The image is stored in the **HUSKYLENS internal memory**.

---

### `exit`

Close the MCP connection and terminate the client:

```text
exit
```

or:

```text
quit
```

---

## 🔌 MCP implementation

The project does not require a third-party MCP client library.

`huskyMcpChat.py` implements the required communication directly using `aiohttp`.

It opens the HUSKYLENS SSE endpoint:

```text
/sse
```

The server responds with a session-specific message endpoint similar to:

```text
/message?session_id=...
```

Requests are then sent as JSON-RPC messages.

The client initializes the MCP session using protocol version:

```text
2024-11-05
```

with:

```json
{
  "method": "initialize",
  "clientInfo": {
    "name": "HuskyLens-Py",
    "version": "1.2.0"
  }
}
```

This makes the repository useful not only as a HUSKYLENS example but also as a compact reference for implementing a simple MCP client manually.

---

## 🛠️ HUSKYLENS MCP tools

The original project documents four important MCP tools.

### `get_recognition_result`

Retrieves real-time recognition data.

Typical operation:

```text
get_result
```

Useful for:

* object recognition
* face recognition
* visual reasoning
* natural-language descriptions

---

### `manage_applications`

Controls the computer-vision algorithms running on HUSKYLENS.

Operations documented by the project include:

```text
current_application
application_list
switch_application
```

---

### `multimedia_control`

Controls multimedia functions.

The project currently uses:

```text
take_photo
```

---

### `task_scheduler`

HUSKYLENS also exposes scheduled or triggered tasks.

Examples include concepts such as:

```text
Take a picture after 3 seconds
```

or:

```text
Take a picture when you see a keyboard
```

The current command-line interface does not expose a dedicated scheduler command, but the MCP tool is documented by the project and provides an interesting path for future development.

> HUSKYLENS firmware has continued evolving since this project's original release, so newer versions may expose additional MCP capabilities.

---

## 🤖 Gemini integration

The project uses:

```text
gemini-2.5-flash
```

through Google's current Python SDK:

```python
from google import genai
```

The basic flow is:

```python
self.client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)
```

For `ask`, Gemini receives:

```text
SENSOR DATA
+
USER QUESTION
+
INSTRUCTIONS
```

For `see`, it receives:

```text
SENSOR DATA
+
DESCRIPTION INSTRUCTIONS
```

The prompt tells Gemini to rely on the supplied sensor evidence and to mention cases where the data is empty or confidence is low.

---

## 📁 Repository structure

```text
HuskyLens2MCP/
├── LICENSE
├── README.md
└── huskyMcpChat.py
```

### `huskyMcpChat.py`

Contains:

* asynchronous HTTP communication
* SSE listener
* JSON-RPC handling
* MCP session initialization
* MCP tool calls
* recognition-data extraction
* Gemini API integration
* interactive command-line interface

---

## 🔬 Ideas for extending the project

1. **🖼️ Multimodal image reasoning** — retrieve captured images and optionally send the actual frame to a multimodal model alongside HUSKYLENS structured recognition data.

2. **⏰ Expose `task_scheduler` in the CLI** — add commands for conditional and scheduled actions such as capturing a photo when a particular object or person is recognized.

3. **🔐 Externalize configuration** — load the Gemini key and MCP address from environment variables or a `.env` file instead of storing credentials inside the Python source.

---

# 📰 External references

HuskyLens2MCP has been documented, indexed, and discussed outside GitHub.

## 🛠️ Project tutorials

### Hackster.io

**[HuskyLens 2 Model Context Protocol (MCP)](https://www.hackster.io/roni-bandini/huskylens-2-model-context-protocol-mcp-3675ac)**

The complete Hackster tutorial explains the motivation for connecting the HUSKYLENS 2 MCP Server directly to Gemini from Python.

It covers:

* firmware setup
* MCP activation
* Gemini configuration
* Python client setup
* algorithm switching
* photo capture
* visual queries
* combined LLM reasoning
* HUSKYLENS MCP tools

The Hackster project links directly to this GitHub repository.

---

### DFRobot Maker Community

**[Huskylens2 MCP with Python and Gemini LLM](https://community.dfrobot.com/makelog-318304.html)**

DFRobot's Maker Community hosts a complete version of the project tutorial.

It covers the HUSKYLENS 2 firmware setup, Gemini API configuration, MCP Server, command-line client, visual reasoning examples, and MCP tools.

The article explicitly links to:

**[github.com/ronibandini/HuskyLens2MCP](https://github.com/ronibandini/HuskyLens2MCP)**

---

### DFRobot HUSKYLENS project collection

**[HUSKYLENS Projects — DFRobot Maker Community](https://community.dfrobot.com/projects-HUSKYLENS-2.html)**

The project is also indexed in DFRobot's HUSKYLENS project collection as:

> **Huskylens2 MCP with Python and Gemini LLM**

---

## ✍️ Medium

### Roni Bandini

**[Línea de comandos para el MCP de la cámara Huskylens2](https://bandini.medium.com/l%C3%ADnea-de-comandos-para-el-mcp-de-la-c%C3%A1mara-huskylens2-332132998317)**

Spanish-language article about interacting with the HUSKYLENS 2 MCP Server through a command-line Python client and Gemini.

This is also the article linked from the GitHub repository's **About** section.

---

## 📚 Useful documentation

* **[HUSKYLENS 2 Official Wiki](https://wiki.dfrobot.com/sen0638/)**
* **[HUSKYLENS 2 MCP Server Guide](https://wiki.dfrobot.com/sen0638/docs/22605)**
* **[HUSKYLENS 2 Product Page](https://www.dfrobot.com/product-2995.html)**
* **[Google AI Studio](https://aistudio.google.com/)**
* **[Model Context Protocol](https://modelcontextprotocol.io/)**

---

# 🔗 You may also be interested in...

Other projects by **Roni Bandini** involving AI interfaces, computer vision, LLMs, and physical computing.

### 📚🤖 Gemini for Kindle

**Run Google Gemini directly from a jailbroken Kindle Paperwhite.**

Another minimalist command-line interface for Gemini, implemented using BusyBox, Bash, KTerm, `curl`, and the Gemini API.

**[github.com/ronibandini/GeminiForKindle](https://github.com/ronibandini/GeminiForKindle)**

---

### 🗂️👁️ PunchedCards

**Punched-card recognition with computer vision, Edge Impulse, and LattePanda IOTA.**

Like HuskyLens2MCP, this project combines a dedicated computer-vision system with a lightweight software layer for interpreting physical objects.

**[github.com/ronibandini/PunchedCards](https://github.com/ronibandini/PunchedCards)**

---

### 🖥️🤖 n8n Terminal

**Physical buttons and a dedicated screen for n8n workflows and AI agents.**

Another experiment in moving AI interactions away from conventional desktop interfaces and into dedicated physical hardware.

**[github.com/ronibandini/n8nTerminal](https://github.com/ronibandini/n8nTerminal)**

---

## 🔐 Security

The current implementation stores the Gemini API key directly in the Python script:

```python
GEMINI_API_KEY = ""
```

For private experiments this is simple, but avoid committing a configured key to GitHub.

For a more robust implementation, use:

* environment variables
* `.env` files excluded through `.gitignore`
* an operating-system credential store

The HUSKYLENS MCP Server should also be treated as a network-accessible control interface. Use it on networks you trust and review the current DFRobot security guidance before exposing the service beyond a local LAN.

---

## 📜 License

HuskyLens2MCP is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

## 👤 Author

**Roni Bandini**

Maker, AI developer, electronic artist and writer.

* 🐙 GitHub: **[@ronibandini](https://github.com/ronibandini)**
* 📸 Instagram: **[@ronibandini](https://www.instagram.com/ronibandini/)**
* 🐦 X: **[@RoniBandini](https://x.com/RoniBandini)**
* ✍️ Medium: **[bandini.medium.com](https://bandini.medium.com/)**
* 🛠️ Hackster: **[Roni Bandini](https://www.hackster.io/roni-bandini)**

Contributions, forks, MCP experiments, alternative LLM integrations, and new HUSKYLENS tools are welcome.
