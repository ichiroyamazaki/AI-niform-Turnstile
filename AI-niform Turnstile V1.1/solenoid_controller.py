import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time

class SolenoidController:
    def __init__(self, root):
        self.root = root
        self.root.title("Solenoid Controller")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Serial connection variables
        self.serial_connection = None
        self.is_connected = False
        
        # Solenoid state
        self.solenoid_state = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Try to auto-connect to Arduino
        self.auto_connect()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Solenoid Controller", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection", padding="10")
        conn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Port selection
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(conn_frame, text="Refresh", command=self.refresh_ports)
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Connect button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Solenoid Control", padding="20")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # ON button
        self.on_btn = ttk.Button(control_frame, text="SOLENOID ON", 
                                command=self.turn_on, state="disabled",
                                style="On.TButton")
        self.on_btn.grid(row=0, column=0, padx=(0, 10), ipadx=20, ipady=10)
        
        # OFF button
        self.off_btn = ttk.Button(control_frame, text="SOLENOID OFF", 
                                 command=self.turn_off, state="disabled",
                                 style="Off.TButton")
        self.off_btn.grid(row=0, column=1, padx=(10, 0), ipadx=20, ipady=10)
        
        # State indicator
        state_frame = ttk.Frame(control_frame)
        state_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Label(state_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        self.state_indicator = ttk.Label(state_frame, text="OFF", 
                                        font=("Arial", 12, "bold"), foreground="red")
        self.state_indicator.pack(side=tk.LEFT)
        
        # Configure column weights
        conn_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure button styles
        style = ttk.Style()
        style.configure("On.TButton", foreground="white", background="green")
        style.configure("Off.TButton", foreground="white", background="red")
    
    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list and not self.port_var.get():
            self.port_var.set(port_list[0])
    
    def auto_connect(self):
        """Try to automatically connect to Arduino"""
        self.refresh_ports()
        if self.port_combo['values']:
            self.port_var.set(self.port_combo['values'][0])
            self.toggle_connection()
    
    def toggle_connection(self):
        """Connect or disconnect from Arduino"""
        if not self.is_connected:
            self.connect()
        else:
            self.disconnect()
    
    def connect(self):
        """Connect to Arduino via serial"""
        try:
            port = self.port_var.get()
            if not port:
                self.status_label.config(text="Please select a port", foreground="red")
                return
            
            # Try to close any existing connection first
            if self.serial_connection:
                self.serial_connection.close()
                time.sleep(0.5)
            
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            
            self.is_connected = True
            self.status_label.config(text=f"Connected to {port}", foreground="green")
            self.connect_btn.config(text="Disconnect")
            self.on_btn.config(state="normal")
            self.off_btn.config(state="normal")
            
        except serial.SerialException as e:
            error_msg = str(e)
            if "Permission denied" in error_msg or "Access is denied" in error_msg:
                self.status_label.config(text="Permission denied! Try these solutions:", foreground="red")
                self.show_permission_help()
            elif "could not open port" in error_msg.lower():
                self.status_label.config(text="Port busy! Close Arduino IDE/other programs", foreground="red")
            else:
                self.status_label.config(text=f"Serial error: {error_msg}", foreground="red")
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {str(e)}", foreground="red")
    
    def show_permission_help(self):
        """Show help dialog for permission issues"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Permission Error Solutions")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        
        # Center the window
        help_window.transient(self.root)
        help_window.grab_set()
        
        frame = ttk.Frame(help_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="COM Port Permission Error Solutions", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        solutions = [
            "1. Close Arduino IDE if it's open (it locks the COM port)",
            "2. Close any other programs using the COM port",
            "3. Try running Python as Administrator:",
            "   - Right-click Command Prompt → Run as Administrator",
            "   - Navigate to your folder and run: python solenoid_controller.py",
            "4. Unplug and reconnect the Arduino USB cable",
            "5. Try a different USB port on your computer",
            "6. Check Device Manager for COM port conflicts",
            "7. Restart your computer if the issue persists"
        ]
        
        for solution in solutions:
            ttk.Label(frame, text=solution, wraplength=450, justify=tk.LEFT).pack(anchor=tk.W, pady=2)
        
        ttk.Button(frame, text="Close", command=help_window.destroy).pack(pady=(20, 0))
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        
        self.is_connected = False
        self.status_label.config(text="Disconnected", foreground="red")
        self.connect_btn.config(text="Connect")
        self.on_btn.config(state="disabled")
        self.off_btn.config(state="disabled")
        self.state_indicator.config(text="OFF", foreground="red")
        self.solenoid_state = False
    
    def send_command(self, command):
        """Send command to Arduino"""
        if self.is_connected and self.serial_connection:
            try:
                self.serial_connection.write(command.encode())
                self.serial_connection.flush()
            except Exception as e:
                self.status_label.config(text=f"Send failed: {str(e)}", foreground="red")
    
    def turn_on(self):
        """Turn solenoid ON"""
        if self.is_connected:
            self.send_command("ON")
            self.solenoid_state = True
            self.state_indicator.config(text="ON", foreground="green")
    
    def turn_off(self):
        """Turn solenoid OFF"""
        if self.is_connected:
            self.send_command("OFF")
            self.solenoid_state = False
            self.state_indicator.config(text="OFF", foreground="red")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_connected:
            self.turn_off()  # Turn off solenoid before closing
            self.disconnect()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SolenoidController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
