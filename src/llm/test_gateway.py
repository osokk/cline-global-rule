"""
Test script for Anthropic Gateway

This script tests the gateway with your API key and validates it works correctly.
If the API key is invalid, it will prompt you to update it.
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path so we can import the gateway
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.llm.anthropic_gateway import AnthropicGateway


def test_gateway_with_key(api_key: str):
    """Test the gateway with a specific API key."""
    print("=" * 60)
    print("Testing Anthropic Gateway")
    print("=" * 60)
    
    # Create gateway with the provided key
    gateway = AnthropicGateway(
        api_key=api_key,
        max_inflight_weight=3,
        min_start_gap_seconds=0.8,
        max_retries=3,  # Fewer retries for testing
    )
    
    print("\n1. Testing light call (simple task)...")
    try:
        response = gateway.create_message(
            size="light",
            model="claude-sonnet-4-20250514",
            messages=[
                {"role": "user", "content": "Say 'Gateway working!' and nothing else."}
            ],
            max_tokens=50,
        )
        print(f"✅ Light call successful!")
        print(f"   Response: {response.content[0].text}")
        print(f"   Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
    except Exception as e:
        error_msg = str(e).lower()
        if "authentication" in error_msg or "api key" in error_msg or "401" in error_msg:
            print(f"❌ Authentication failed: {e}")
            print("\n" + "=" * 60)
            print("API KEY IS INVALID OR EXPIRED")
            print("=" * 60)
            print("\nPlease update your API key:")
            print("1. Go to: https://console.anthropic.com/settings/keys")
            print("2. Create a new API key or verify the existing one")
            print("3. Update the key in this script or set ANTHROPIC_API_KEY env var")
            print("\nCurrent key (first 20 chars): " + api_key[:20] + "...")
            return False
        else:
            print(f"❌ Light call failed: {e}")
            return False
    
    print("\n2. Testing heavy call (longer task)...")
    try:
        response = gateway.create_message(
            size="heavy",
            model="claude-sonnet-4-20250514",
            messages=[
                {"role": "user", "content": "List 3 benefits of using a rate-limited API gateway. Be concise."}
            ],
            max_tokens=200,
        )
        print(f"✅ Heavy call successful!")
        print(f"   Response length: {len(response.content[0].text)} chars")
        print(f"   Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
    except Exception as e:
        print(f"❌ Heavy call failed: {e}")
        return False
    
    print("\n3. Testing concurrent calls (3 light calls)...")
    try:
        import concurrent.futures
        
        def make_call(i):
            return gateway.create_message(
                size="light",
                model="claude-sonnet-4-20250514",
                messages=[
                    {"role": "user", "content": f"Say 'Call {i} complete' and nothing else."}
                ],
                max_tokens=50,
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_call, i) for i in range(1, 4)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        print(f"✅ Concurrent calls successful! Completed {len(results)} calls")
        for i, result in enumerate(results, 1):
            print(f"   Call {i}: {result.content[0].text}")
    except Exception as e:
        print(f"❌ Concurrent calls failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nGateway is working correctly. You can now use it in your projects:")
    print("\n  from cline_global_rules.src.llm.anthropic_gateway import gateway")
    print("  response = gateway.create_message(size='light', ...)")
    print("\n" + "=" * 60)
    return True


def main():
    """Main test function."""
    # Try to get API key from environment first (same as Roo uses)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("\nPlease set your API key:")
        print("  Windows: set ANTHROPIC_API_KEY=your_key_here")
        print("  Linux/Mac: export ANTHROPIC_API_KEY=your_key_here")
        print("\nOr pass it directly in the code (not recommended for git)")
        sys.exit(1)
    
    print("Using API key from ANTHROPIC_API_KEY environment variable")
    
    # Test the gateway
    success = test_gateway_with_key(api_key)
    
    if not success:
        print("\n⚠️  TESTS FAILED - Please fix the issues above and try again")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
