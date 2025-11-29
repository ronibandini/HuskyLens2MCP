#!/usr/bin/env python3
"""
Interactive Command Line for Huskylens 2 MCP Server
Author: Roni Bandini
Date: Nov 29, 2025
MIT License

"""

import asyncio
import aiohttp
import json
import re
import logging
import sys
from typing import Optional
import os

os.system('cls')

# --- Gemini SDK section ---
try:
    from google import genai
except ImportError:
    class GeminiImportError(Exception): pass
    def genai(): raise GeminiImportError("Please install google-genai: 'pip install google-genai'")

# --- Configuration ---
# Logging to WARNING in order to keep the console clean for the chat 
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Settings
GEMINI_API_KEY = "" # Get your free tier API key at https://aistudio.google.com/app/api-keys
SERVER_URL = "http://0.0.0.0.:3000" # get this from Huskylens MCP section


class HuskyLensClient:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.session = None
        self.request_id = 0
        self.message_url = None
        self.pending_responses = {}
        self.initialized = False
        self.sse_task = None
        
    async def connect(self):
        self.session = aiohttp.ClientSession()
        print(f"🔌 Connecting to SSE at {self.server_url}...")
        self.sse_task = asyncio.create_task(self._listen_sse())
        
        # Wait for session URL
        for _ in range(50):
            if self.message_url: break
            await asyncio.sleep(0.1)
        
        if not self.message_url:
            raise Exception("Failed to get session URL from MCP server :(")
        
        await self._initialize()
    
    async def _initialize(self):
        await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "HuskyLens-Py", "version": "1.2.0"}
        })
        self.initialized = True
        await self._send_notification("notifications/initialized")
    
    async def _listen_sse(self):
        """Background task to listen for server events"""
        try:
            async with self.session.get(f"{self.server_url}/sse") as response:
                async for line in response.content:
                    line_text = line.decode('utf-8').strip()
                    if line_text.startswith('data: '):
                        data = line_text[6:]
                        
                        # Extract Session URL
                        if 'session_id=' in data:
                            match = re.search(r'(/message\?session_id=[a-f0-9-]+)', data)
                            if match: self.message_url = f"{self.server_url}{match.group(1)}"
                            continue
                        elif data.startswith('/message'):
                            self.message_url = f"{self.server_url}{data}"
                            continue
                        
                        if data == '[DONE]': continue
                        
                        # Handle JSON-RPC Responses
                        try:
                            json_data = json.loads(data)
                            if isinstance(json_data, dict) and 'id' in json_data:
                                if json_data['id'] in self.pending_responses:
                                    self.pending_responses[json_data['id']].set_result(json_data)
                        except: pass
        except Exception as e:
            logger.error(f"SSE Error: {e}")
    
    async def _send_request(self, method: str, params: dict = None, timeout: float = 15.0):
        if not self.message_url: raise Exception("Not connected.")
        
        self.request_id += 1
        req_id = self.request_id
        fut = asyncio.Future()
        self.pending_responses[req_id] = fut
        
        try:
            payload = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}
            async with self.session.post(self.message_url, json=payload) as resp:
                await resp.text()
            return await asyncio.wait_for(fut, timeout=timeout)
        except Exception as e:
            if req_id in self.pending_responses: del self.pending_responses[req_id]
            return {"error": str(e)}
            
    async def _send_notification(self, method: str, params: dict = None):
        if self.message_url:
            async with self.session.post(self.message_url, json={"jsonrpc": "2.0", "method": method, "params": params or {}}): pass

    async def call_tool(self, tool, args=None):
        return await self._send_request("tools/call", {"name": tool, "arguments": args or {}})

    async def close(self):
        if self.sse_task: self.sse_task.cancel()
        if self.session: await self.session.close()

    @staticmethod
    def extract_content(response: dict) -> str:
        if not response or "result" not in response or "content" not in response["result"]:
            return ""
        return "\n".join([b.get("text", "") for b in response["result"]["content"] if b.get("type") == "text"])


class GeminiBrain:
    def __init__(self, api_key: str):
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            self.client = None
            print(f"⚠️ Gemini Error auch: {e}")

    async def analyze_data(self, json_data: str, user_query: str = None) -> str:
        if not self.client: return "Gemini is not configured."

        # System Prompt
        base_instruction = "You are a computer vision brain. You analyze raw JSON data from a HuskyLens 2 cammera."
        
        if user_query:
            # Mode: Interrogation ('ask')
            prompt = f'''
            {base_instruction}
            
            SENSOR DATA (JSON):
            {json_data}
            
            USER QUESTION: "{user_query}"
            
            INSTRUCTION:
            Answer the user's question based ONLY on the evidence in the JSON data.
            If the JSON is empty or confidence (conf) is low, state that clearly.
            Keep the answer concise.
            '''
        else:
            # Mode: Description ('see')
            prompt = f'''
            {base_instruction}
            
            SENSOR DATA (JSON):
            {json_data}
            
            INSTRUCTION:
            Briefly describe what is currently visible based on the data. Translate coordinates or IDs into natural language.
            '''

        loop = asyncio.get_running_loop()
        try:
            print("  🧠 Processing with Gemini...", end="\r")
            resp = await loop.run_in_executor(None, lambda: self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt))
            return resp.text
        except Exception as e:
            return f"API Error: {e}"

async def main_loop(client: HuskyLensClient, brain: GeminiBrain):
    print("\n" + "="*40)
    print("      Huskylens2 MCP Command Line      ")
    print("      Roni Bandini 11/2025      ")
    print("      MIT License      ")
    print("="*40)
    print(" 1. list                 : List algorithms")
    print(" 2. current              : Show active algorithm")
    print(" 3. switch <Algorithm>   : Switch algorithm (e.g., 'switch FaceRecognition')")
    print(" 4. ask <Question>       : Ask AI about the view")
    print(" 5. see                  : General AI description")
    print(" 6. photo                : Take photo (to internal memory)")
    print(" 7. exit                 : Quit")
    print("-" * 40)

    while True:
        try:
            raw_input = await asyncio.get_event_loop().run_in_executor(None, input, "\nUser > ")
            parts = raw_input.strip().split(maxsplit=1)
            if not parts: continue
            
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None

            if cmd in ['exit', 'quit', '7']: 
                break

            # ---------------------------------------------------------
            # 1. LIST ALGORITHMS
            # ---------------------------------------------------------
            elif cmd in ['list', 'ls', '1']:
                print("📡 Fetching algorithm list...")
                res = await client.call_tool("manage_applications", {"operation": "application_list"})
                print(client.extract_content(res))

            # ---------------------------------------------------------
            # 2. CURRENT ALGORITHM 
            # ---------------------------------------------------------
            elif cmd in ['current', 'status', '2']:
                print("📡 Checking active algorithm...")
                res = await client.call_tool("manage_applications", {"operation": "current_application"})
                content = client.extract_content(res)
                print(f"✅ Active Algorithm: {content}")

            # ---------------------------------------------------------
            # 3. SWITCH ALGORITHM
            # ---------------------------------------------------------
            elif cmd in ['switch', '3']:
                if not arg:
                    arg = input("  Enter algorithm name (e.g., ObjectTracking) > ").strip()
                
                if arg:
                    print(f"🔄 Switching to '{arg}'...")
                    res = await client.call_tool("manage_applications", {
                        "operation": "switch_application", 
                        "algorithm": arg
                    })
                    print(f"✅ {client.extract_content(res)}")

            # ---------------------------------------------------------
            # 4. ASK (Prompt with Context)
            # ---------------------------------------------------------
            elif cmd in ['ask', '4']:
                if not arg:
                    print("⚠️ Please provide a question. Example: 'ask Is there a person?'")
                    continue
                
                print("👀 Asking Huskylens2...")
                res = await client.call_tool("get_recognition_result", {"operation": "get_result"})
                json_data = client.extract_content(res)
                
                print(f"📄 Raw Data:\n{json_data}")
                
                answer = await brain.analyze_data(json_data, user_query=arg)
                print(f"\n🤖 AI ANSWER: {answer}")

            # ---------------------------------------------------------
            # 5. SEE (General Description)
            # ---------------------------------------------------------
            elif cmd in ['see', 'look', '5']:
                print("👀 Reading sensor data...")
                res = await client.call_tool("get_recognition_result", {"operation": "get_result"})
                json_data = client.extract_content(res)
                print(f"📄 Raw Data:\n{json_data}")
                
                answer = await brain.analyze_data(json_data, user_query=None)
                print(f"\n🤖 DESCRIPTION: {answer}")

            # ---------------------------------------------------------
            # 6. PHOTO (to Internal Memory, microSD card is not used here)
            # ---------------------------------------------------------
            elif cmd in ['photo', 'snap', '6']:
                print("📸 Sending capture command...")
                res = await client.call_tool("multimedia_control", {"operation": "take_photo"})
                
                # Show raw output just in case
                raw_out = client.extract_content(res)
                print(f"✅ Done")
                print("ℹ️  Note: Image saved to HuskyLens internal memory.")

            else:
                print("❓ Unknown command.")

        except Exception as e:
            print(f"❌ Error in loop: {e}")


async def main():
    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY is missing in the script configuration.")
        return

    client = HuskyLensClient(SERVER_URL)
    brain = GeminiBrain(GEMINI_API_KEY)

    try:
        await client.connect()
        print("✅ Connected to HuskyLens MCP.")
        await main_loop(client, brain)
    finally:
        print("🔌 Closing connection...")
        await client.close()

if __name__ == '__main__':
    asyncio.run(main())