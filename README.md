# Modbus TCP Master

A cross-platform tool for testing Modbus TCP communication. Available in both **GUI** and **CLI** versions. This tool allows you to read a range of holding registers and write uint16 values to individual registers.

## Features

- ✅ **Graphical User Interface (GUI)** - Easy-to-use cross-platform interface
- ✅ Read a range of holding registers
- ✅ Write uint16 values (0-65535) to registers
- ✅ Cross-platform compatibility (Windows, Linux, macOS)
- ✅ Support for custom TCP ports and unit IDs
- ✅ Automatic write verification
- ✅ Clear formatted output with decimal and hexadecimal values
- ✅ Real-time connection status
- ✅ Command-line interface (CLI) also available

## Requirements

- Python 3.7 or higher
- pymodbus library
- tkinter (for GUI - usually included with Python)

## Installation

1. Clone this repository or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pymodbus
```

**Note for Linux users:** You may need to install tkinter separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter
```

## Usage

### GUI Application (Recommended)

The GUI provides an intuitive interface for interacting with Modbus TCP devices.

**Start the GUI:**

```bash
python modbus_gui.py
```

or on some systems:

```bash
python3 modbus_gui.py
```

**GUI Features:**

1. **Connection Settings**
   - Enter IP address of the Modbus server
   - Configure TCP port (default: 502)
   - Set Modbus unit/slave ID (default: 1)
   - Connect/Disconnect button with status indicator

2. **Read Registers**
   - Enter start address
   - Specify number of registers to read
   - Click "Read Registers" to fetch values
   - Results display in both decimal and hexadecimal format

3. **Write Register**
   - Enter register address
   - Enter uint16 value (0-65535)
   - Click "Write Register" to write value
   - Automatic verification of written value

4. **Output Window**
   - Real-time logging of all operations
   - Timestamp for each action
   - Color-coded status indicators (✓ success, ✗ error, ℹ info)
   - Clear button to reset output

**GUI Screenshots:**

![GUI Connected](screenshots_gui_connected.png)
*GUI interface after connecting to a Modbus server*

![GUI Reading Registers](screenshots_gui_reading.png)
*Reading multiple registers with formatted output*

![GUI Writing Register](screenshots_gui_writing.png)
*Writing a value to a register with automatic verification*

### Command-Line Interface (CLI)

### Command-Line Interface (CLI)

For automation or scripting, use the command-line interface.

#### Basic Syntax

```bash
python modbus_master.py --host <IP_ADDRESS> [options] <operation>
```

### Reading Registers

Read a range of holding registers:

```bash
python modbus_master.py --host 192.168.1.100 --read <START_ADDRESS> <COUNT>
```

**Example:** Read 10 registers starting at address 0:

```bash
python modbus_master.py --host 192.168.1.100 --read 0 10
```

**Output:**
```
✓ Connected to 192.168.1.100:502

Reading 10 register(s) starting at address 0...

============================================================
Address    Value (dec)     Value (hex)    
============================================================
0          0               0x0000
1          1234            0x04D2
2          5678            0x162E
3          0               0x0000
...
============================================================
✓ Disconnected
```

### Writing Registers

Write a uint16 value to a single register:

```bash
python modbus_master.py --host 192.168.1.100 --write <ADDRESS> <VALUE>
```

**Example:** Write value 1234 to register at address 5:

```bash
python modbus_master.py --host 192.168.1.100 --write 5 1234
```

**Output:**
```
✓ Connected to 192.168.1.100:502

Writing value 1234 (0x04D2) to register at address 5...
✓ Successfully wrote 1234 to register 5

Verifying write...
✓ Verification successful: register 5 = 1234
✓ Disconnected
```

### Advanced Options

#### Custom TCP Port

Use a non-standard Modbus TCP port:

```bash
python modbus_master.py --host 192.168.1.100 --port 5020 --read 0 5
```

#### Custom Unit ID (Slave ID)

Specify a different Modbus unit/slave ID:

```bash
python modbus_master.py --host 192.168.1.100 --unit 2 --read 100 10
```

#### Connection Timeout

Set a custom connection timeout (in seconds):

```bash
python modbus_master.py --host 192.168.1.100 --timeout 5 --read 0 10
```

#### Combined Options

```bash
python modbus_master.py --host 192.168.1.100 --port 5020 --unit 2 --timeout 5 --read 0 10
```

## Command-Line Arguments

### Required Arguments

- `--host` : IP address or hostname of the Modbus TCP server

### Optional Arguments

- `--port` : TCP port (default: 502)
- `--unit` : Modbus unit/slave ID (default: 1)
- `--timeout` : Connection timeout in seconds (default: 3)

### Operations (choose one)

- `--read START COUNT` : Read COUNT registers starting at address START
- `--write ADDRESS VALUE` : Write VALUE (uint16: 0-65535) to register at ADDRESS

## Value Range

When writing registers, values must be in the uint16 range:
- **Minimum:** 0
- **Maximum:** 65535 (0xFFFF)

Values outside this range will be rejected with an error message.

## Cross-Platform Compatibility

This tool is designed to work on:
- **Windows** (10/11 and Server versions)
- **Linux** (Ubuntu, Debian, CentOS, etc.)
- **macOS** (10.14+)

The tool uses pure Python and the pymodbus library, ensuring consistent behavior across all platforms.

## Testing with a Modbus Simulator

If you don't have a physical Modbus device, you can test with a Modbus simulator:

1. Install a Modbus TCP simulator/server (e.g., ModRSsim2, pymodbus simulator)
2. Configure it to listen on the desired port (default 502)
3. Run the modbus_master.py commands against the simulator

## Examples

### Example 1: Quick Register Check

Read first 5 registers:

```bash
python modbus_master.py --host 192.168.1.100 --read 0 5
```

### Example 2: Set Register Value

Write maximum uint16 value:

```bash
python modbus_master.py --host 192.168.1.100 --write 0 65535
```

### Example 3: Read Multiple Register Ranges

Read registers 0-9:
```bash
python modbus_master.py --host 192.168.1.100 --read 0 10
```

Read registers 100-104:
```bash
python modbus_master.py --host 192.168.1.100 --read 100 5
```

### Example 4: Different Slave Device

Access a different device on the same server:

```bash
python modbus_master.py --host 192.168.1.100 --unit 3 --read 0 10
```

## Troubleshooting

### Connection Refused
- Verify the server IP address and port
- Check if the Modbus TCP server is running
- Verify firewall settings allow TCP connections on the Modbus port

### Timeout Errors
- Increase timeout: `--timeout 10`
- Check network connectivity
- Verify the server is responding

### Permission Errors
On Linux, ports below 1024 may require sudo:
```bash
sudo python modbus_master.py --host 192.168.1.100 --port 502 --read 0 10
```

## License

This tool is provided as-is for testing and development purposes.

## Contributing

Feel free to submit issues and enhancement requests!
