import cv2
import socket
import pickle
import struct
import tkinter as tk

def get_screen_resolution():
    """Get the laptop's screen resolution automatically"""
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def center_window(window_name, window_width, window_height):
    """Center the window on the laptop screen"""
    screen_width, screen_height = get_screen_resolution()
    
    # Calculate perfect center position
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Create and position window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)
    cv2.moveWindow(window_name, x, y)
    
    print(f"💻 Laptop screen: {screen_width}x{screen_height}")
    print(f"🪟 Stream window centered at: ({x}, {y})")

# Main client code
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.1'  # Your main PC's IP
port = 9999

try:
    client_socket.connect((host_ip, port))
    print("✅ Connected to server!")
    
    # Center the window before streaming starts
    center_window("Screen Stream - Press Q to quit", 500, 500)
    
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        
        if not data: break
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        
        frame_data = data[:msg_size]
        data = data[msg_size:]
        
        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        cv2.imshow("Screen Stream - Press Q to quit", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client_socket.close()
    cv2.destroyAllWindows()
    print("🔌 Client closed")