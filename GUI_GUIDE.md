# Modbus TCP Master GUI - Quick Start Guide

## Overview

The Modbus TCP Master GUI provides an easy-to-use graphical interface for reading and writing Modbus TCP holding registers. It's cross-platform and works on Windows, Linux, and macOS.

## Starting the GUI

```bash
python modbus_gui.py
```

Or on some systems:

```bash
python3 modbus_gui.py
```

## User Interface Layout

### 1. Connection Settings (Top Section)

**Fields:**
- **IP Address**: Enter the IP address of your Modbus TCP server (e.g., 192.168.1.100)
- **Port**: TCP port number (default: 502)
- **Unit ID**: Modbus unit/slave ID (default: 1)
- **Connect/Disconnect Button**: Toggles connection state
- **Status Indicator**: Shows "Connected" (green) or "Disconnected" (red)

**Usage:**
1. Enter the IP address of your Modbus device
2. Adjust port and unit ID if needed (most devices use port 502 and unit ID 1)
3. Click "Connect"
4. Wait for green "Connected" status

### 2. Read Registers Section

**Fields:**
- **Start Address**: The first register address to read from (e.g., 0)
- **Count**: Number of consecutive registers to read (e.g., 10)
- **Read Registers Button**: Executes the read operation

**Usage:**
1. Ensure you're connected to the server
2. Enter the starting register address
3. Enter how many registers you want to read (1-125)
4. Click "Read Registers"
5. Results appear in the output window showing:
   - Register address
   - Value in decimal format
   - Value in hexadecimal format

**Example:**
- Start Address: 0
- Count: 10
- Result: Reads registers 0-9

### 3. Write Register Section

**Fields:**
- **Address**: Single register address to write to (e.g., 5)
- **Value (0-65535)**: The uint16 value to write
- **Write Register Button**: Executes the write operation

**Usage:**
1. Ensure you're connected to the server
2. Enter the register address
3. Enter a value between 0 and 65535
4. Click "Write Register"
5. The operation is performed and verified automatically
6. Results appear in the output window

**Important Notes:**
- Values must be in the range 0-65535 (uint16)
- The GUI automatically verifies the write by reading back the value
- Writes to one register at a time

### 4. Output Window (Bottom Section)

**Features:**
- Real-time logging of all operations
- Timestamp for each action ([HH:MM:SS])
- Status indicators:
  - ✓ Success (green checkmark)
  - ✗ Error (red X)
  - ℹ Information (info icon)
- Scrollable text area
- **Clear Output Button**: Clears all messages

**Log Messages Include:**
- Connection/disconnection events
- Read operations with formatted results
- Write operations with verification status
- Error messages with descriptions

## Example Workflow

### Reading Registers

1. Start the GUI: `python modbus_gui.py`
2. Enter connection details:
   - IP Address: 192.168.1.100
   - Port: 502
   - Unit ID: 1
3. Click "Connect"
4. Configure read operation:
   - Start Address: 0
   - Count: 10
5. Click "Read Registers"
6. View results in output window

### Writing a Register

1. Ensure you're connected (follow steps 1-3 above)
2. Configure write operation:
   - Address: 5
   - Value: 1234
3. Click "Write Register"
4. Check output window for:
   - Write confirmation
   - Verification result

### Disconnecting

1. Click "Disconnect" button when finished
2. Status changes to "Disconnected" (red)
3. Read and Write buttons become disabled

## Tips

- **Connection Issues**: Check IP address, port, and network connectivity
- **Timeout Errors**: Server might be slow or unreachable
- **Value Errors**: Ensure values are within 0-65535 range
- **Address Errors**: Valid register addresses are typically 0-65535
- **Multiple Reads**: You can read up to 125 registers at once
- **Output History**: Use "Clear Output" to reset the log when needed

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Submit current field (same as clicking button)
- **Escape**: No direct shortcut, use mouse to close window

## Error Messages

Common error messages and their meanings:

- "Not connected to server": Click Connect first
- "Invalid port number": Port must be a number (typically 502)
- "Value must be between 0 and 65535": Enter a valid uint16 value
- "Count must be between 1 and 125": Adjust register count
- "Connection error": Check network and server availability

## Cross-Platform Notes

### Windows
- Double-click modbus_gui.py or run from Command Prompt
- tkinter is included with Python installation
- May need to allow firewall access for Modbus TCP

### Linux
- Run from terminal: `python3 modbus_gui.py`
- Install tkinter if needed: `sudo apt-get install python3-tk`
- May need sudo for ports below 1024

### macOS
- Run from terminal: `python3 modbus_gui.py`
- tkinter is included with Python installation
- May need to grant network permissions

## Troubleshooting

### GUI Won't Start

**Problem**: Window doesn't appear
**Solution**: 
- Check if tkinter is installed: `python3 -c "import tkinter"`
- Install if missing (see README.md)

### Can't Connect

**Problem**: Connection fails
**Solutions**:
- Verify IP address is correct
- Check if Modbus server is running
- Verify port number (usually 502)
- Check firewall settings
- Try pinging the server: `ping <ip_address>`

### Write Verification Fails

**Problem**: Write succeeds but verification shows different value
**Possible Causes**:
- Server modified the value
- Another client changed the value
- Register is read-only
- Network delay or packet loss

## Support

For issues or questions:
1. Check the README.md file
2. Verify your Modbus server is working with test_server.py
3. Try the CLI version (modbus_master.py) to isolate GUI issues
4. Check the output window for detailed error messages
