# Screen Stream Center - Real-time Screen Streaming

A high-performance Python application that streams the center portion of your main PC's screen to a secondary laptop in real-time using DirectX acceleration and Ethernet connectivity.

## 🚀 Features

- **Perfect Center Capture**: Automatically detects screen resolution and captures exact 500x500 center region
- **High Performance**: Uses DxCam with DirectX acceleration for 60 FPS game capture
- **Low Latency**: Ethernet direct connection for minimal delay
- **Auto-Centered Display**: Client window automatically centers on laptop screen
- **Cross-Platform**: Works on Windows systems
- **Real-time Markers**: Visual center indicators for precise alignment

## 📋 Requirements

### Main PC (Server)
```bash
pip install dxcam opencv-python numpy pillow pyautogui
```

### Laptop (Client)
```bash
pip install opencv-python numpy pillow
```

## 🛠️ Setup Instructions

### Network Configuration

1. **Connect PCs via Ethernet cable**
2. **Set static IP addresses**:
   - Main PC: `192.168.1.1`
   - Laptop: `192.168.1.2`
   - Subnet Mask: `255.255.255.0`

3. **Verify connection**:
   ```cmd
   # On laptop, ping main PC:
   ping 192.168.1.1
   ```

### Usage

1. **Start Server (Main PC)**:
   ```bash
   python server.py
   ```
   - Automatically detects screen resolution
   - Starts streaming center 500x500 region
   - Listens for client connections

2. **Start Client (Laptop)**:
   ```bash
   python client.py
   ```
   - Connects to main PC
   - Opens centered 500x500 display window
   - Press `Q` to quit

## 🎮 Gaming Optimization

### For Valorant/Competitive Games
- Uses **DxCam** for DirectX hardware acceleration
- 60 FPS capture capability
- Low CPU usage on main PC
- Minimal input lag

### Legal Notice
⚠️ **Use responsibly**:
- Single-player games: ✅ Generally safe
- Competitive multiplayer: ⚠️ Check game EULA/TOS
- Anti-cheat games: ❌ High risk of bans

## 📁 File Structure

```
screen-stream-center/
├── server.py          # Main PC streaming server
├── client.py          # Laptop viewing client
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔧 Technical Details

### Screen Capture Methods
- **Primary**: DxCam (DirectX) - 60 FPS gaming capture
- **Fallback**: PyAutoGUI - Software-based capture
- **Region**: Perfect center 500x500 pixels

### Network Protocol
- TCP socket communication
- JPEG frame compression
- Pickle serialization for data transfer

### Performance
- **Resolution**: 500x500 pixels
- **Frame Rate**: Up to 60 FPS with DxCam
- **Latency**: <50ms over Ethernet
- **Bandwidth**: ~5-10 Mbps

## 🐛 Troubleshooting

### Connection Issues
1. Check Ethernet cable connection
2. Verify IP addresses match in both scripts
3. Disable firewalls temporarily for testing
4. Ensure both PCs are on same subnet

### Performance Issues
1. Use DxCam for gaming content
2. Close unnecessary applications
3. Ensure direct Ethernet connection (not through router)
4. Adjust JPEG quality in server code

### Capture Issues
1. Run as Administrator if game capture fails
2. Check DxCam compatibility with your GPU
3. Verify screen resolution detection

## 📊 Customization

### Change Capture Size
Modify in both `server.py` and `client.py`:
```python
# Change from 500 to desired size
CAPTURE_SIZE = 600
start_x = center_x - CAPTURE_SIZE//2
start_y = center_y - CAPTURE_SIZE//2
```

### Adjust Streaming Quality
```python
# In server.py - adjust JPEG quality (0-100)
_, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is for educational and personal use only. Users are responsible for complying with game EULAs and terms of service.

## ⚠️ Disclaimer

This software is provided as-is. The developers are not responsible for any account bans, legal issues, or damages resulting from misuse. Always respect game developers' terms of service.

---

**⭐ If this project helped you, please give it a star!**
