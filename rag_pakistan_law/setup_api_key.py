"""
Script to help set up the Gemini API key
"""
import os

def main():
    print("🔑 Gemini API Key Setup")
    print("=" * 30)
    
    print("\n1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated API key")
    
    api_key = input("\nEnter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    # Create .env file
    env_content = f"GEMINI_API_KEY={api_key}\n"
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ API key saved to .env file")
        print("\n🧪 Testing the setup...")
        
        # Test the setup
        os.environ["GEMINI_API_KEY"] = api_key
        
        try:
            from gemini_integration import GeminiIntegration
            gemini = GeminiIntegration(api_key)
            
            if gemini.test_connection():
                print("✅ API key is working!")
                print("\n🚀 You can now run: streamlit run app.py")
            else:
                print("❌ API key test failed. Please check your key.")
                
        except Exception as e:
            print(f"❌ Error testing API key: {e}")
            
    except Exception as e:
        print(f"❌ Error saving API key: {e}")

if __name__ == "__main__":
    main()
