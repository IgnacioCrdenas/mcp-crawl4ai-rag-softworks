#!/usr/bin/env python3
"""
Test script for Amazon Nova Micro model integration.
This script tests the nova-micro model functionality in isolation.
"""
import os
import sys
import json
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from providers.aws_bedrock import invoke_bedrock_model

def test_nova_micro():
    """Test Nova Micro model invocation."""
    print("Testing Amazon Nova Micro model...")
    
    # Test prompt
    prompt = "Explain the benefits of using cost-effective AI models in one sentence."
    
    # Test parameters
    model_id = "amazon.nova-micro-v1:0"
    max_tokens = 100
    temperature = 0.7
    
    print(f"Model ID: {model_id}")
    print(f"Prompt: {prompt}")
    print(f"Max tokens: {max_tokens}")
    print(f"Temperature: {temperature}")
    print("-" * 50)
    
    try:
        result = invoke_bedrock_model(
            model_id=model_id,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if result:
            print("✅ Success! Nova Micro response:")
            print(result)
            print(f"\nResponse length: {len(result)} characters")
        else:
            print("❌ Error: No response received from Nova Micro")
            
    except Exception as e:
        print(f"❌ Error invoking Nova Micro: {e}")
        return False
    
    return True

def test_other_nova_models():
    """Test other Nova models if available."""
    models_to_test = [
        "amazon.nova-lite-v1:0",
        "amazon.nova-pro-v1:0"
    ]
    
    prompt = "What are multimodal AI capabilities?"
    
    for model_id in models_to_test:
        print(f"\nTesting {model_id}...")
        try:
            result = invoke_bedrock_model(
                model_id=model_id,
                prompt=prompt,
                max_tokens=50,
                temperature=0.5
            )
            
            if result:
                print(f"✅ {model_id} works!")
                print(f"Response: {result[:100]}...")
            else:
                print(f"❌ {model_id} returned no response")
                
        except Exception as e:
            print(f"❌ {model_id} error: {e}")

def check_aws_credentials():
    """Check if AWS credentials are configured."""
    required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing AWS credentials:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these environment variables before running the test.")
        return False
    
    print("✅ AWS credentials configured")
    return True

if __name__ == "__main__":
    print("Amazon Nova Models Test Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_aws_credentials():
        sys.exit(1)
    
    # Test Nova Micro (primary focus)
    success = test_nova_micro()
    
    # Test other Nova models (optional)
    print("\n" + "=" * 50)
    print("Testing other Nova models (optional)...")
    test_other_nova_models()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Nova Micro integration test completed successfully!")
        print("\nTo use Nova Micro in your application, set:")
        print('BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"')
    else:
        print("❌ Nova Micro integration test failed!")
        sys.exit(1)
