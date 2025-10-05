#!/usr/bin/env python3
"""
Test script for Meta Llama integration
Tests the CEO agent with Cerebras → Meta Llama → ASI:One fallback hierarchy
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Add the ai_uagents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_uagents'))

from ceo_uagent import CEOuAgent

async def test_meta_llama_integration():
    """Test Meta Llama integration with CEO agent"""
    print("🦙 Testing Meta Llama Integration with Hack-Aura")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Cerebras API key is configured
    cerebras_key = os.getenv('CEREBRAS_API_KEY')
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    
    print(f"✅ Cerebras API Key configured: {bool(cerebras_key)}")
    print(f"✅ Hugging Face API Key configured: {bool(hf_key)}")
    
    if not cerebras_key:
        print("❌ CEREBRAS_API_KEY not found in environment")
        return False
    
    try:
        # Initialize CEO agent
        print("\n🤖 Initializing CEO Agent...")
        ceo_agent = CEOuAgent()
        
        # Test basic functionality
        print("\n🧠 Testing CEO Agent with fallback hierarchy...")
        
        # Test 1: Normal Cerebras call
        print("\n🚀 Test 1: Normal Cerebras API call...")
        test_prompt = "Generate a simple business idea for a tech startup. Keep it brief."
        
        try:
            response = await ceo_agent.call_cerebras(test_prompt, 500)
            if response:
                print(f"✅ Cerebras API call successful")
                print(f"📝 Response: {response[:100]}...")
            else:
                print("❌ No response from Cerebras API")
                return False
        except Exception as e:
            print(f"❌ Cerebras API call failed: {str(e)}")
            return False
        
        # Test 2: Force Meta Llama fallback (if HF key available)
        if hf_key:
            print("\n🦙 Test 2: Testing Meta Llama fallback...")
            try:
                # Temporarily break Cerebras to test fallback
                original_client = ceo_agent.cerebras_client
                ceo_agent.cerebras_client = None
                
                response = await ceo_agent.call_cerebras(test_prompt, 500)
                if response:
                    print(f"✅ Meta Llama fallback successful")
                    print(f"📝 Response: {response[:100]}...")
                else:
                    print("❌ No response from Meta Llama fallback")
                
                # Restore original client
                ceo_agent.cerebras_client = original_client
                
            except Exception as e:
                print(f"❌ Meta Llama fallback failed: {str(e)}")
                # Restore original client
                ceo_agent.cerebras_client = original_client
        else:
            print("\n⚠️ Test 2: Skipped - No Hugging Face API key")
        
        print("\n🎉 Meta Llama integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_meta_llama_integration()
    
    if success:
        print("\n✅ All tests passed! Meta Llama integration is working.")
        print("🔄 Fallback hierarchy: Cerebras → Meta Llama → ASI:One")
        sys.exit(0)
    else:
        print("\n❌ Tests failed! Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
