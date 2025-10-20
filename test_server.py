#!/usr/bin/env python3
"""
Simple Modbus TCP Server for testing the modbus_master.py client.
This server runs locally and provides a test environment.
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def run_test_server(host='127.0.0.1', port=5020):
    """
    Start a Modbus TCP test server.
    
    Args:
        host: IP address to bind to
        port: TCP port to listen on
    """
    # Initialize data store with some test values
    # Create 100 holding registers, starting with some preset values
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0]*100)
    )
    
    # Set some initial test values
    store.setValues(3, 0, [0, 1234, 5678, 9999, 42, 65535, 100, 200, 300, 400])
    
    context = ModbusServerContext(slaves=store, single=True)
    
    # Server identity
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Test Modbus Server'
    identity.ProductCode = 'TEST'
    identity.VendorUrl = 'http://test.local'
    identity.ProductName = 'Test Modbus TCP Server'
    identity.ModelName = 'Test Server v1.0'
    identity.MajorMinorRevision = '1.0.0'
    
    print(f"Starting Modbus TCP test server on {host}:{port}")
    print("Press Ctrl+C to stop")
    print("\nInitial register values (0-9):")
    print("  Address 0: 0")
    print("  Address 1: 1234")
    print("  Address 2: 5678")
    print("  Address 3: 9999")
    print("  Address 4: 42")
    print("  Address 5: 65535")
    print("  Address 6: 100")
    print("  Address 7: 200")
    print("  Address 8: 300")
    print("  Address 9: 400")
    
    # Start server
    StartTcpServer(
        context=context,
        identity=identity,
        address=(host, port)
    )

if __name__ == '__main__':
    run_test_server()
