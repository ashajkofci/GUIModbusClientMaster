#!/usr/bin/env python3
"""
Cross-platform Modbus TCP Master GUI
A graphical tool to read and write Modbus TCP holding registers.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException


class ModbusGUI:
    """GUI application for Modbus TCP Master."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Modbus TCP Master")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        self.client = None
        self.connected = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Connection Frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding="10")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        conn_frame.columnconfigure(1, weight=1)
        conn_frame.columnconfigure(3, weight=1)
        
        # IP Address
        ttk.Label(conn_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ip_var = tk.StringVar(value="127.0.0.1")
        ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=20)
        ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ip_entry.bind('<Return>', lambda e: self.toggle_connection())
        
        # Port
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_var = tk.StringVar(value="502")
        port_entry = ttk.Entry(conn_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        port_entry.bind('<Return>', lambda e: self.toggle_connection())
        
        # Unit ID
        ttk.Label(conn_frame, text="Unit ID:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.unit_var = tk.StringVar(value="1")
        unit_entry = ttk.Entry(conn_frame, textvariable=self.unit_var, width=10)
        unit_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 10))
        unit_entry.bind('<Return>', lambda e: self.toggle_connection())
        
        # Connect/Disconnect Button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=6, padx=(0, 5))
        
        # Status Label
        self.status_var = tk.StringVar(value="Disconnected")
        status_label = ttk.Label(conn_frame, textvariable=self.status_var, foreground="red")
        status_label.grid(row=0, column=7, sticky=tk.W)
        
        # Read Registers Frame
        read_frame = ttk.LabelFrame(main_frame, text="Read Registers", padding="10")
        read_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        read_frame.columnconfigure(1, weight=1)
        read_frame.columnconfigure(3, weight=1)
        
        # Start Address
        ttk.Label(read_frame, text="Start Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.read_start_var = tk.StringVar(value="0")
        read_start_entry = ttk.Entry(read_frame, textvariable=self.read_start_var, width=15)
        read_start_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        read_start_entry.bind('<Return>', lambda e: self.read_registers() if self.connected else None)
        
        # Count
        ttk.Label(read_frame, text="Count:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.read_count_var = tk.StringVar(value="10")
        read_count_entry = ttk.Entry(read_frame, textvariable=self.read_count_var, width=15)
        read_count_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        read_count_entry.bind('<Return>', lambda e: self.read_registers() if self.connected else None)
        
        # Read Button
        self.read_btn = ttk.Button(read_frame, text="Read Registers", command=self.read_registers, state=tk.DISABLED)
        self.read_btn.grid(row=0, column=4, padx=(0, 0))
        
        # Write Register Frame
        write_frame = ttk.LabelFrame(main_frame, text="Write Register", padding="10")
        write_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        write_frame.columnconfigure(1, weight=1)
        write_frame.columnconfigure(3, weight=1)
        
        # Address
        ttk.Label(write_frame, text="Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.write_addr_var = tk.StringVar(value="0")
        write_addr_entry = ttk.Entry(write_frame, textvariable=self.write_addr_var, width=15)
        write_addr_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        write_addr_entry.bind('<Return>', lambda e: self.write_register() if self.connected else None)
        
        # Value
        ttk.Label(write_frame, text="Value(s) (0-65535):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.write_value_var = tk.StringVar(value="0")
        write_value_entry = ttk.Entry(write_frame, textvariable=self.write_value_var, width=15)
        write_value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        write_value_entry.bind('<Return>', lambda e: self.write_register() if self.connected else None)
        
        # Write Button
        self.write_btn = ttk.Button(write_frame, text="Write Register", command=self.write_register, state=tk.DISABLED)
        self.write_btn.grid(row=0, column=4, padx=(0, 0))
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Output Text Area with scrollbar
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, state=tk.DISABLED, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear Button
        clear_btn = ttk.Button(output_frame, text="Clear Output", command=self.clear_output)
        clear_btn.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
    def log_message(self, message, level="info"):
        """Add a message to the output text area."""
        self.output_text.config(state=tk.NORMAL)
        
        # Add timestamp and format message
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if level == "success":
            prefix = "✓"
        elif level == "error":
            prefix = "✗"
        elif level == "info":
            prefix = "ℹ"
        else:
            prefix = ""
        
        formatted_message = f"[{timestamp}] {prefix} {message}\n"
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def toggle_connection(self):
        """Connect or disconnect from Modbus server."""
        if self.connected:
            self.disconnect()
        else:
            self.connect()
            
    def connect(self):
        """Connect to Modbus server."""
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get().strip())
            
            if not ip:
                messagebox.showerror("Error", "Please enter an IP address")
                return
            
            self.log_message(f"Connecting to {ip}:{port}...")
            
            self.client = ModbusTcpClient(host=ip, port=port, timeout=3)
            
            if self.client.connect():
                self.connected = True
                self.status_var.set("Connected")
                self.root.nametowidget(str(self.connect_btn)).configure(style="")
                
                # Update UI
                for widget in self.root.nametowidget(str(self.connect_btn)).master.winfo_children():
                    if isinstance(widget, ttk.Label) and widget.cget("textvariable") == str(self.status_var):
                        widget.configure(foreground="green")
                
                self.connect_btn.config(text="Disconnect")
                self.read_btn.config(state=tk.NORMAL)
                self.write_btn.config(state=tk.NORMAL)
                
                self.log_message(f"Connected to {ip}:{port}", "success")
            else:
                self.log_message(f"Failed to connect to {ip}:{port}", "error")
                messagebox.showerror("Connection Error", f"Could not connect to {ip}:{port}")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
        except Exception as e:
            self.log_message(f"Connection error: {e}", "error")
            messagebox.showerror("Error", f"Connection error: {e}")
            
    def disconnect(self):
        """Disconnect from Modbus server."""
        if self.client:
            self.client.close()
            self.client = None
            
        self.connected = False
        self.status_var.set("Disconnected")
        
        # Update UI
        for widget in self.root.nametowidget(str(self.connect_btn)).master.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("textvariable") == str(self.status_var):
                widget.configure(foreground="red")
        
        self.connect_btn.config(text="Connect")
        self.read_btn.config(state=tk.DISABLED)
        self.write_btn.config(state=tk.DISABLED)
        
        self.log_message("Disconnected", "info")
        
    def read_registers(self):
        """Read holding registers from Modbus server."""
        if not self.connected or not self.client:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        try:
            start_address = int(self.read_start_var.get().strip())
            count = int(self.read_count_var.get().strip())
            unit_id = int(self.unit_var.get().strip())
            
            if count <= 0 or count > 125:
                messagebox.showerror("Error", "Count must be between 1 and 125")
                return
            
            if start_address < 0 or start_address > 65535:
                messagebox.showerror("Error", "Address must be between 0 and 65535")
                return
            
            self.log_message(f"Reading {count} register(s) starting at address {start_address}...")
            
            # Run in thread to avoid blocking UI
            def read_thread():
                try:
                    response = self.client.read_holding_registers(
                        address=start_address,
                        count=count,
                        slave=unit_id
                    )
                    
                    if response.isError():
                        self.root.after(0, lambda: self.log_message(f"Error reading registers: {response}", "error"))
                        self.root.after(0, lambda: messagebox.showerror("Read Error", str(response)))
                    else:
                        registers = response.registers
                        
                        # Format output
                        output = "\n" + "="*60 + "\n"
                        output += f"{'Address':<12} {'Value (dec)':<15} {'Value (hex)'}\n"
                        output += "="*60 + "\n"
                        
                        for i, value in enumerate(registers):
                            addr = start_address + i
                            output += f"{addr:<12} {value:<15} 0x{value:04X}\n"
                        
                        output += "="*60
                        
                        self.root.after(0, lambda: self.log_message(output, "success"))
                        
                except ModbusException as e:
                    self.root.after(0, lambda: self.log_message(f"Modbus error: {e}", "error"))
                    self.root.after(0, lambda: messagebox.showerror("Modbus Error", str(e)))
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Error: {e}", "error"))
                    self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            
            thread = threading.Thread(target=read_thread, daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input values. Please enter valid numbers.")
            
    def write_register(self):
        """Write a value to a holding register."""
        if not self.connected or not self.client:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        try:
            address = int(self.write_addr_var.get().strip())
            raw_value = self.write_value_var.get().strip()
            unit_id = int(self.unit_var.get().strip())
            
            if address < 0 or address > 65535:
                messagebox.showerror("Error", "Address must be between 0 and 65535")
                return
            
            if not raw_value:
                messagebox.showerror("Error", "Please enter a value to write")
                return

            # Support comma or whitespace separated lists; allow 0x-prefixed numbers.
            tokens = [token for token in raw_value.replace(",", " ").split() if token]
            if not tokens:
                messagebox.showerror("Error", "Please enter a valid value")
                return

            try:
                values = [int(token, 0) for token in tokens]
            except ValueError:
                messagebox.showerror("Error", "Values must be integers (decimal or 0x-prefixed hex)")
                return

            for val in values:
                if val < 0 or val > 65535:
                    messagebox.showerror("Error", "Values must be between 0 and 65535 (uint16)")
                    return

            values = tuple(values)
            multiple_values = len(values) > 1

            if multiple_values:
                pretty = ", ".join(f"{v} (0x{v:04X})" for v in values)
                self.log_message(
                    f"Writing {len(values)} value(s) [{pretty}] starting at register {address}..."
                )
            else:
                value = values[0]
                self.log_message(f"Writing value {value} (0x{value:04X}) to register {address}...")
            
            # Run in thread to avoid blocking UI
            def write_thread():
                try:
                    response = self.client.write_registers(
                        address=address,
                        values=list(values),
                        slave=unit_id
                    )
                    
                    if response.isError():
                        self.root.after(0, lambda: self.log_message(f"Error writing register: {response}", "error"))
                        self.root.after(0, lambda: messagebox.showerror("Write Error", str(response)))
                    else:
                        if multiple_values:
                            self.root.after(
                                0,
                                lambda: self.log_message(
                                    f"Successfully wrote {len(values)} value(s) starting at register {address}",
                                    "success"
                                )
                            )
                        else:
                            value = values[0]
                            self.root.after(
                                0,
                                lambda: self.log_message(
                                    f"Successfully wrote {value} to register {address}",
                                    "success"
                                )
                            )
                        
                        # Verify write (allow device time to update)
                        time.sleep(0.2)
                        self.root.after(0, lambda: self.log_message("Verifying write...", "info"))
                        verify_response = self.client.read_holding_registers(
                            address=address,
                            count=len(values),
                            slave=unit_id
                        )
                        
                        if verify_response.isError():
                            self.root.after(0, lambda: self.log_message(f"Verify read failed: {verify_response}", "error"))
                            return

                        read_back = verify_response.registers[: len(values)]
                        if len(read_back) < len(values):
                            self.root.after(0, lambda: self.log_message("Verification returned insufficient data", "error"))
                            return

                        if list(read_back) == list(values):
                            if multiple_values:
                                formatted = ", ".join(
                                    f"{address + idx}={val} (0x{val:04X})"
                                    for idx, val in enumerate(read_back)
                                )
                                self.root.after(0, lambda: self.log_message(f"Verification successful: {formatted}", "success"))
                            else:
                                self.root.after(0, lambda: self.log_message(f"Verification successful: register {address} = {read_back[0]}", "success"))
                        else:
                            if multiple_values:
                                expected = ", ".join(str(v) for v in values)
                                observed = ", ".join(str(v) for v in read_back)
                                self.root.after(0, lambda: self.log_message(f"Warning: read back values [{observed}] differ from written values [{expected}]", "error"))
                            else:
                                value = values[0]
                                self.root.after(0, lambda: self.log_message(f"Warning: read back value {read_back[0]} differs from written value {value}", "error"))
                        
                except ModbusException as e:
                    self.root.after(0, lambda: self.log_message(f"Modbus error: {e}", "error"))
                    self.root.after(0, lambda: messagebox.showerror("Modbus Error", str(e)))
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Error: {e}", "error"))
                    self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            
            thread = threading.Thread(target=write_thread, daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input values. Please enter valid numbers.")
            
    def on_closing(self):
        """Handle window close event."""
        if self.connected:
            self.disconnect()
        self.root.destroy()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = ModbusGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
