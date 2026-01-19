# Debug Setup for Azure Functions

## Prerequisites
✅ debugpy is installed (already done)
✅ VS Code Azure Functions extension installed
✅ Python extension for VS Code installed

## How to Debug

### Method 1: VS Code Debugger (Recommended)

1. **Open the project in VS Code**
   - Open the `backend/azure-functions` folder in VS Code

2. **Set Breakpoints**
   - Open `get_subjects/__init__.py`
   - Click in the left margin to set breakpoints (red dots)

3. **Start Debugging**
   - Press `F5` or go to Run > Start Debugging
   - Select "Attach to Python Functions"
   - The function will start automatically and the debugger will attach

4. **Test the Function**
   - Make a request: `curl http://localhost:7071/api/get_subjects`
   - The debugger will pause at your breakpoints

### Method 2: Manual Start + Attach

1. **Start Function Manually**
   ```bash
   cd backend/azure-functions
   func start
   ```

2. **Attach Debugger in VS Code**
   - Press `F5`
   - Select "Attach to Python Functions"
   - The debugger will attach to the running process

### Troubleshooting

**If debugger doesn't attach:**
1. Make sure port 9091 is not blocked
2. Check that debugpy is installed: `pip list | grep debugpy`
3. Restart VS Code
4. Check the Debug Console in VS Code for errors

**If breakpoints don't work:**
1. Make sure `justMyCode: false` is set in launch.json (already configured)
2. Verify path mappings are correct
3. Try setting breakpoints on lines with actual code (not empty lines)

**Port conflicts:**
- Function runs on: 7071
- Debugger attaches on: 9091
- Make sure both ports are available

## Current Configuration

- **Debug Port**: 9091
- **Function Port**: 7071
- **Python Runtime**: Python 3.9+
- **Debugpy Version**: 1.8.19

## Test Debugging

1. Set a breakpoint in `get_subjects/__init__.py` on line 49 (language detection)
2. Start debugging (F5)
3. Make a request: `curl http://localhost:7071/api/get_subjects`
4. Debugger should pause at the breakpoint
5. Use VS Code debug controls to step through code
