import os
from anthropic import Anthropic

def test_anthropic_api():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set")
        return

    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-2.1",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": "Say hello and tell me what you can do in one sentence."
            }]
        )
        print("API Response:", message.content)
        print("Success! The Anthropic API is working correctly.")
    except Exception as e:
        print(f"Error testing Anthropic API: {str(e)}")

if __name__ == "__main__":
    test_anthropic_api() 