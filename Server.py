import dxcam
import cv2
import numpy as np
import socket
import pickle
import struct
import tkinter as tk

def get_screen_center():
    """Detect screen resolution and calculate perfect center for 500x500 capture"""
    # Method 1: Using tkinter for accurate screen detection
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    print(f"📺 Detected Screen Resolution: {screen_width}x{screen_height}")
    
    # Calculate perfect center coordinates
    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2
    
    # Calculate top-left corner for 500x500 capture
    start_x = screen_center_x - 250
    start_y = screen_center_y - 250
    
    print(f"🎯 Screen Center: ({screen_center_x}, {screen_center_y})")
    print(f"📷 Capture Area: ({start_x}, {start_y}) to ({start_x+500}, {start_y+500})")
    
    return start_x, start_y, screen_width, screen_height

# Main server code
def main():
    # Detect screen and calculate center
    start_x, start_y, screen_width, screen_height = get_screen_center()
    
    # Initialize DxCam - MUCH better for gaming!
    print("🚀 Initializing DxCam for high-performance capture...")
    camera = dxcam.create()
    
    if camera is None:
        print("❌ Failed to initialize DxCam")
        return
    
    # Start capturing region
    region = (start_x, start_y, start_x + 500, start_y + 500)
    camera.start(region=region, target_fps=60)  # 60 FPS capture!
    print("✅ DxCam started capturing 500x500 center region at 60 FPS")
    
    # Socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.1'  # Your main PC's static IP
    port = 9999
    server_socket.bind((host_ip, port))
    server_socket.listen(5)
    print(f"🌐 Server listening on {host_ip}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"🔗 Connection from: {addr}")
        
        if client_socket:
            try:
                while True:
                    # Capture frame using DxCam (much faster than pyautogui!)
                    frame = camera.get_latest_frame()
                    
                    if frame is not None:
                        # Convert BGR to RGB (DxCam returns BGR, OpenCV expects BGR actually)
                        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Not needed with DxCam
                        
                        # Add visual markers to verify perfect center
                        cv2.circle(frame, (249, 249), 4, (0, 0, 255), -1)  # Red center dot
                        cv2.line(frame, (249, 240), (249, 258), (0, 255, 0), 2)  # Vertical
                        cv2.line(frame, (240, 249), (258, 249), (0, 255, 0), 2)  # Horizontal
                        cv2.rectangle(frame, (0, 0), (499, 499), (255, 255, 255), 2)
                        
                        # Add info text
                        cv2.putText(frame, f"Center: (249,249)", (10, 20), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                        cv2.putText(frame, f"Screen: {screen_width}x{screen_height}", (10, 40), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                        cv2.putText(frame, "DxCam - 60 FPS", (10, 60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                        
                        # Compress and send frame
                        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                        data = pickle.dumps(buffer)
                        message = struct.pack("Q", len(data)) + data
                        
                        client_socket.sendall(message)
                    else:
                        # No frame available yet, small delay
                        import time
                        time.sleep(0.001)
                        
            except Exception as e:
                print(f"❌ Error: {e}")
                client_socket.close()
                print("🔌 Client disconnected")
            finally:
                camera.stop()

if __name__ == "__main__":
    main()