# 🚀 Quick Setup Guide

## ✅ Current Status
- ✅ All directories created
- ✅ Dependencies installed
- ✅ Sample PDF created
- ❌ Need to set up Gemini API key

## 🔑 Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## ⚙️ Step 2: Set Up Environment

Create a file named `.env` in the project directory with this content:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the API key you copied from Google AI Studio.

## 🧪 Step 3: Test the System

Run this command to test everything:

```bash
python test_system.py
```

You should see all tests passing.

## 🚀 Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Step 5: Add Real PDFs (Optional)

1. Download PDFs from:
   - Pakistan Penal Code: https://www.pakistancode.gov.pk/
   - Constitution: https://www.na.gov.pk/en/downloads.php
2. Place them in the `pdfs/` directory
3. The app will automatically process them

## 🎯 Ready to Use!

Once you've set up the API key, you can:
- Ask questions like "What is section 302?"
- Search by section numbers
- Filter by document type
- View source citations

## 🆘 Need Help?

If you encounter any issues:
1. Check that your API key is correct
2. Ensure you have internet connection
3. Try running `python test_system.py` again
