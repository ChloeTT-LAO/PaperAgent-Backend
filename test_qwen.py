#!/usr/bin/env python3
"""
Quick test script for Qwen API
测试 Qwen API 是否正常工作
"""

import os
import sys

def test_qwen_api():
    """Test if Qwen API is working"""
    
    print("🧪 Testing Qwen API Connection...\n")
    
    # Check API Key
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ DASHSCOPE_API_KEY not set!")
        print("\n设置方法:")
        print("  export DASHSCOPE_API_KEY='sk-your-key-here'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    # Try to import OpenAI
    try:
        from openai import OpenAI
        print("✅ OpenAI SDK imported")
    except ImportError:
        print("❌ OpenAI SDK not installed")
        print("\n安装方法:")
        print("  pip install openai")
        return False
    
    # Test API call
    try:
        print("\n📡 Sending test request to Qwen API...")
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello' in one word"}
            ],
            temperature=0.7,
            max_tokens=10
        )
        
        answer = response.choices[0].message.content
        print(f"✅ API Response: {answer}")
        print(f"✅ Tokens used: {response.usage.total_tokens}")
        
        print("\n🎉 Qwen API is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ API call failed: {e}")
        print("\n可能的原因:")
        print("  1. API Key 无效")
        print("  2. 网络连接问题")
        print("  3. 免费额度已用完")
        print("\n检查方法:")
        print("  访问: https://bailian.console.aliyun.com/")
        return False

if __name__ == "__main__":
    success = test_qwen_api()
    sys.exit(0 if success else 1)
