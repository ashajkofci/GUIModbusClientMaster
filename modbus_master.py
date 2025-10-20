#!/usr/bin/env python3
"""
Cross-platform Modbus TCP Master
A simple tool to read and write Modbus TCP holding registers.
"""

import argparse
import sys
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException


class ModbusMaster:
    """Modbus TCP Master client for reading and writing registers."""
    
    def __init__(self, host, port=502, timeout=3):
        """
        Initialize Modbus TCP client.
        
        Args:
            host: IP address or hostname of the Modbus server
            port: TCP port (default 502)
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = None
    
    def connect(self):
        """Establish connection to Modbus server."""
        try:
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )
            if self.client.connect():
                print(f"✓ Connected to {self.host}:{self.port}")
                return True
            else:
                print(f"✗ Failed to connect to {self.host}:{self.port}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close connection to Modbus server."""
        if self.client:
            self.client.close()
            print("✓ Disconnected")
    
    def read_registers(self, start_address, count, unit_id=1):
        """
        Read a range of holding registers.
        
        Args:
            start_address: Starting register address
            count: Number of registers to read
            unit_id: Modbus unit/slave ID (default 1)
            
        Returns:
            List of register values or None on error
        """
        if not self.client or not self.client.connected:
            print("✗ Not connected to server")
            return None
        
        try:
            response = self.client.read_holding_registers(
                address=start_address,
                count=count,
                slave=unit_id
            )
            
            if response.isError():
                print(f"✗ Error reading registers: {response}")
                return None
            
            return response.registers
        except ModbusException as e:
            print(f"✗ Modbus error: {e}")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def write_register(self, address, value, unit_id=1):
        """
        Write a uint16 value to a single holding register.
        
        Args:
            address: Register address
            value: uint16 value to write (0-65535)
            unit_id: Modbus unit/slave ID (default 1)
            
        Returns:
            True on success, False on error
        """
        if not self.client or not self.client.connected:
            print("✗ Not connected to server")
            return False
        
        # Validate uint16 range
        if not (0 <= value <= 65535):
            print(f"✗ Value {value} out of uint16 range (0-65535)")
            return False
        
        try:
            response = self.client.write_register(
                address=address,
                value=value,
                slave=unit_id
            )
            
            if response.isError():
                print(f"✗ Error writing register: {response}")
                return False
            
            return True
        except ModbusException as e:
            print(f"✗ Modbus error: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False


def main():
    """Main entry point for the Modbus TCP master application."""
    parser = argparse.ArgumentParser(
        description='Modbus TCP Master - Read and write holding registers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read 10 registers starting at address 0
  %(prog)s --host 192.168.1.100 --read 0 10
  
  # Write value 1234 to register at address 5
  %(prog)s --host 192.168.1.100 --write 5 1234
  
  # Read registers with custom port and unit ID
  %(prog)s --host 192.168.1.100 --port 5020 --unit 2 --read 100 5
        """
    )
    
    # Connection parameters
    parser.add_argument('--host', required=True,
                        help='Modbus server IP address or hostname')
    parser.add_argument('--port', type=int, default=502,
                        help='TCP port (default: 502)')
    parser.add_argument('--unit', type=int, default=1,
                        help='Modbus unit/slave ID (default: 1)')
    parser.add_argument('--timeout', type=int, default=3,
                        help='Connection timeout in seconds (default: 3)')
    
    # Operations
    operation_group = parser.add_mutually_exclusive_group(required=True)
    operation_group.add_argument('--read', nargs=2, metavar=('START', 'COUNT'),
                                 type=int,
                                 help='Read COUNT registers starting at START address')
    operation_group.add_argument('--write', nargs=2, metavar=('ADDRESS', 'VALUE'),
                                 type=int,
                                 help='Write VALUE (uint16) to register at ADDRESS')
    
    args = parser.parse_args()
    
    # Create and connect to Modbus master
    master = ModbusMaster(args.host, args.port, args.timeout)
    
    if not master.connect():
        return 1
    
    try:
        if args.read:
            start_address, count = args.read
            print(f"\nReading {count} register(s) starting at address {start_address}...")
            registers = master.read_registers(start_address, count, args.unit)
            
            if registers is not None:
                print("\n" + "="*60)
                print(f"{'Address':<10} {'Value (dec)':<15} {'Value (hex)':<15}")
                print("="*60)
                for i, value in enumerate(registers):
                    addr = start_address + i
                    print(f"{addr:<10} {value:<15} 0x{value:04X}")
                print("="*60)
                return 0
            else:
                return 1
        
        elif args.write:
            address, value = args.write
            print(f"\nWriting value {value} (0x{value:04X}) to register at address {address}...")
            
            if master.write_register(address, value, args.unit):
                print(f"✓ Successfully wrote {value} to register {address}")
                
                # Verify write by reading back
                print("\nVerifying write...")
                registers = master.read_registers(address, 1, args.unit)
                if registers is not None and len(registers) > 0:
                    read_value = registers[0]
                    if read_value == value:
                        print(f"✓ Verification successful: register {address} = {read_value}")
                    else:
                        print(f"⚠ Warning: read back value {read_value} differs from written value {value}")
                return 0
            else:
                return 1
    
    finally:
        master.disconnect()


if __name__ == '__main__':
    sys.exit(main())
