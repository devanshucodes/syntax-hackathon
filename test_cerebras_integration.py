#!/usr/bin/env python3
"""
Test script for Cerebras integration
Tests the CEO agent with Cerebras API
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Add the ai_uagents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_uagents'))

from ceo_uagent import CEOuAgent

async def test_cerebras_integration():
    """Test Cerebras integration with CEO agent"""
    print("🚀 Testing Cerebras Integration with Hack-Aura")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Cerebras API key is configured
    cerebras_key = os.getenv('CEREBRAS_API_KEY')
    if not cerebras_key:
        print("❌ CEREBRAS_API_KEY not found in environment")
        return False
    
    print(f"✅ Cerebras API Key configured: {cerebras_key[:20]}...")
    
    try:
        # Initialize CEO agent
        print("\n🤖 Initializing CEO Agent...")
        ceo_agent = CEOuAgent()
        
        # Test basic functionality
        print("\n🧠 Testing CEO Agent with Cerebras...")
        
        # Test basic Cerebras API call
        print("\n💡 Testing Cerebras API call...")
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
        
        print("\n🎉 Cerebras integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_cerebras_integration()
    
    if success:
        print("\n✅ All tests passed! Cerebras integration is working.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed! Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
