"""
Base uAgent class for AI Company agents
Provides common functionality for all agents including Cerebras integration
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from cerebras.cloud.sdk import Cerebras
from huggingface_hub import InferenceClient

load_dotenv()

class BaseUAgent:
    """Base class for all AI Company uAgents"""
    
    def __init__(self, name: str, role: str, port: int):
        self.name = name
        self.role = role
        self.port = port
        
        # Initialize Cerebras client (Primary)
        self.cerebras_api_key = os.getenv('CEREBRAS_API_KEY')
        if not self.cerebras_api_key:
            raise ValueError(f"CEREBRAS_API_KEY not found for {name}")
        
        self.cerebras_client = Cerebras(api_key=self.cerebras_api_key)
        
        # Initialize Meta Llama client (Fallback)
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.hf_model = os.getenv('HUGGINGFACE_MODEL', 'meta-llama/Llama-2-7b-chat-hf')
        
        if self.hf_api_key:
            self.hf_client = InferenceClient(
                model=self.hf_model,
                token=self.hf_api_key
            )
        else:
            self.hf_client = None
            print(f"⚠️ [{self.name}] HUGGINGFACE_API_KEY not found - Meta Llama fallback disabled")
        
        # Legacy ASI:One fallback (Third tier)
        self.asi_one_api_key = os.getenv('ASI_ONE_API_KEY')
        self.asi_one_base_url = 'https://api.asi1.ai/v1'
        
        # Initialize the agent
        self.agent = Agent(
            name=name,
            port=port,
            mailbox=True,
            publish_agent_details=True  # Register on Agentverse
        )
        
        print(f"🚀 [{self.name}] Initialized with Cerebras API")
        print(f"🔑 [{self.name}] Cerebras API Key configured: {bool(self.cerebras_api_key)}")
        print(f"🦙 [{self.name}] Meta Llama fallback available: {bool(self.hf_client)}")
        print(f"🔑 [{self.name}] ASI:One legacy fallback available: {bool(self.asi_one_api_key)}")
    
    async def call_cerebras(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call Cerebras API to generate response"""
        try:
            print(f"🚀 [{self.name}] Calling Cerebras API...")
            print(f"🔑 [{self.name}] Using model: llama-4-scout-17b-16e-instruct")
            
            chat_completion = self.cerebras_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-4-scout-17b-16e-instruct",
                max_tokens=max_tokens
            )
            
            content = chat_completion.choices[0].message.content
            print(f"✅ [{self.name}] Cerebras response received ({len(content)} chars)")
            return content
            
        except Exception as e:
            print(f"❌ [{self.name}] Error calling Cerebras: {str(e)}")
            print(f"🔄 [{self.name}] Falling back to Meta Llama...")
            return await self.call_meta_llama(prompt, max_tokens)
    
    async def call_meta_llama(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call Meta Llama API via Hugging Face to generate response"""
        if not self.hf_client:
            print(f"❌ [{self.name}] Meta Llama client not available")
            print(f"🔄 [{self.name}] Falling back to ASI:One...")
            return await self.call_asi_one_fallback(prompt, max_tokens)
            
        try:
            print(f"🦙 [{self.name}] Calling Meta Llama API...")
            print(f"🔑 [{self.name}] Using model: {self.hf_model}")
            
            # Format prompt for Llama chat
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            response = self.hf_client.text_generation(
                formatted_prompt,
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                return_full_text=False
            )
            
            content = response[0]['generated_text'] if isinstance(response, list) else response
            print(f"✅ [{self.name}] Meta Llama response received ({len(content)} chars)")
            return content
            
        except Exception as e:
            print(f"❌ [{self.name}] Error calling Meta Llama: {str(e)}")
            print(f"🔄 [{self.name}] Falling back to ASI:One...")
            return await self.call_asi_one_fallback(prompt, max_tokens)
    
    async def call_asi_one_fallback(self, prompt: str, max_tokens: int = 1000) -> str:
        """Fallback to ASI:One API if Cerebras and Meta Llama fail"""
        if not self.asi_one_api_key:
            raise Exception("All APIs failed - Cerebras, Meta Llama, and ASI:One unavailable")
            
        try:
            print(f"🔑 [{self.name}] Calling ASI:One legacy fallback API...")
            
            response = requests.post(
                f"{self.asi_one_base_url}/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.asi_one_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'asi1-mini',
                    'max_tokens': max_tokens,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"✅ [{self.name}] ASI:One legacy fallback response received ({len(content)} chars)")
                return content
            else:
                print(f"❌ [{self.name}] ASI:One legacy fallback API error: {response.status_code}")
                raise Exception(f"ASI:One legacy fallback API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ [{self.name}] Error calling ASI:One legacy fallback: {str(e)}")
            raise e
    
    def log_activity(self, activity: str, data: Dict[str, Any] = None):
        """Log agent activity"""
        print(f"[{self.name}] {activity}: {data or 'No data'}")
    
    def get_agent_address(self) -> str:
        """Get the agent's address for communication"""
        return str(self.agent.address)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            'name': self.name,
            'role': self.role,
            'port': self.port,
            'address': self.get_agent_address(),
            'status': 'active'
        }
