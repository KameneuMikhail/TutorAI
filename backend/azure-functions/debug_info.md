# Azure Function Debug Mode

## Current Status
✅ Function is running in debug mode with verbose logging
- Function endpoint: `http://localhost:7071/api/get_subjects`
- Debug port: `9091` (for Python debugger attachment)

## How to Debug

### Option 1: VS Code Debugger (Recommended)
1. Open VS Code in the `azure-functions` folder
2. Set breakpoints in `get_subjects/__init__.py`
3. Press `F5` or go to Run > Start Debugging
4. Select "Attach to Python Functions"
5. The debugger will attach automatically

### Option 2: Manual Debugger Attachment
1. Install debugpy: `pip install debugpy`
2. Add to your function code:
   ```python
   import debugpy
   debugpy.listen(("localhost", 9091))
   debugpy.wait_for_client()
   ```
3. Attach your debugger to `localhost:9091`

### Option 3: Test with Logging
The function is running with verbose logging. Check the terminal output for:
- Request processing logs
- Language detection logs
- Response logs

## Test the Function
```bash
# Default (Russian)
curl http://localhost:7071/api/get_subjects

# English
curl "http://localhost:7071/api/get_subjects?lang=en"

# Russian
curl "http://localhost:7071/api/get_subjects?lang=ru"
```

## View Logs
Check the terminal where `func start --verbose` is running to see:
- Function invocations
- Language detection
- Response data
- Any errors
