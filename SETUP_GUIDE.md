# Quick Setup Guide for Windows

## Step 1: Run Setup Script

Open PowerShell or Command Prompt in the project directory and run:

```cmd
setup.bat
```

This will automatically:
- Activate the virtual environment
- Upgrade pip
- Install PyTorch with CUDA support
- Install all other dependencies

## Step 2: Create Environment File

```cmd
copy .env.example .env
```

You can edit `.env` to customize settings (optional).

## Step 3: Test the Installation

### Option A: Quick Test
```cmd
python main.py --prompt "Hello, world!" --quantized
```

### Option B: Interactive Chat
```cmd
python main.py --interactive --quantized
```

### Option C: Start API Server
```cmd
python api_server.py
```

Then in another terminal:
```cmd
python examples\api_example.py
```

## Troubleshooting

### Issue: "source: command not found"
**Solution:** On Windows, use `venv\Scripts\activate` instead of `source venv/bin/activate`

### Issue: "No module named 'torch'"
**Solution:** 
1. Make sure virtual environment is activated
2. Run `setup.bat` again
3. Or manually install: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

### Issue: "CUDA out of memory"
**Solution:** Always use the `--quantized` flag to enable 8-bit quantization

### Issue: Model download is slow
**Solution:** The model is ~12GB. First download will take time. Subsequent runs will use the cached model.

## Next Steps

1. **Try the chat interface:**
   ```cmd
   python main.py --interactive --quantized
   ```

2. **Start the API server:**
   ```cmd
   python api_server.py
   ```
   Then visit http://localhost:8000 in your browser

3. **Fine-tune on your data:**
   - Add your text files to `data/` folder
   - Run: `python train.py --data data/your_file.txt`

4. **Read the documentation:**
   - `README.md` - Full documentation
   - `API_DOCS.md` - API reference
   - `examples/api_example.py` - Code examples

## Common Commands

```cmd
# Activate environment
venv\Scripts\activate

# Run chat
python main.py --interactive --quantized

# Run API server
python api_server.py

# Fine-tune model
python train.py --data data/your_data.txt

# Test API
python examples\api_example.py
```

Enjoy your custom LLM platform! 🚀
