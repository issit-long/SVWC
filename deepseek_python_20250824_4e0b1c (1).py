import socket
import json
import time
from typing import List, Dict, Union

class SamsungMDCController:
    def __init__(self, tv_ips: List[str]):
        self.tv_ips = tv_ips
        self.port = 1515  # Default MDC port
        self.timeout = 2  # seconds
        
    def send_command(self, ip: str, command: str) -> str:
        """Send a command to a Samsung display via MDC protocol"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((ip, self.port))
                sock.sendall(command.encode('ascii'))
                
                # Wait for response
                response = sock.recv(1024).decode('ascii').strip()
                return response
        except Exception as e:
            raise Exception(f"Failed to send command to {ip}: {e}")
    
    def power_on(self, display: Union[str, int] = 'all') -> Dict:
        """Turn on specified display(s)"""
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, "ka 00 01\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], "ka 00 01\r")
            return {f"display_{display}": response}
    
    def power_off(self, display: Union[str, int] = 'all') -> Dict:
        """Turn off specified display(s)"""
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, "ka 00 00\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], "ka 00 00\r")
            return {f"display_{display}": response}
    
    def set_volume(self, display: Union[str, int], volume: int) -> Dict:
        """Set volume level (0-100) for specified display(s)"""
        # Convert 0-100 scale to hex (00-64)
        vol_hex = format(min(max(volume, 0), 100), '02x')
        
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, f"kf 00 {vol_hex}\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], f"kf 00 {vol_hex}\r")
            return {f"display_{display}": response}
    
    def mute(self, display: Union[str, int] = 'all') -> Dict:
        """Mute specified display(s)"""
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, "ke 00 01\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], "ke 00 01\r")
            return {f"display_{display}": response}
    
    def unmute(self, display: Union[str, int] = 'all') -> Dict:
        """Unmute specified display(s)"""
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, "ke 00 00\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], "ke 00 00\r")
            return {f"display_{display}": response}
    
    def set_input(self, display: Union[str, int], input_source: str) -> Dict:
        """Set input source for specified display(s)"""
        # Map input sources to MDC codes
        input_map = {
            "hdmi1": "0x21",
            "hdmi2": "0x22",
            "dp": "0x23",
            "vga": "0x15",
            "magicinfo": "0x31"
        }
        
        source_code = input_map.get(input_source.lower(), "0x21")
        
        if display == 'all':
            results = {}
            for i, ip in enumerate(self.tv_ips, 1):
                results[f"display_{i}"] = self.send_command(ip, f"xb 00 {source_code}\r")
            return results
        else:
            idx = int(display) - 1
            response = self.send_command(self.tv_ips[idx], f"xb 00 {source_code}\r")
            return {f"display_{display}": response}
    
    def set_layout(self, layout: str) -> Dict:
        """Set video wall layout"""
        # This would typically use MagicInfo or similar API
        # For now, we'll just return a mock response
        return {"status": "success", "layout": layout, "message": "Layout change simulated"}
    
    def get_status(self, display: int) -> Dict:
        """Get status of a specific display"""
        # In a real implementation, this would query the display for status
        # For now, we'll return mock data
        return {
            "power": "on",
            "volume": 50,
            "muted": False,
            "input": "hdmi1",
            "temperature": 42,
            "hours": 1234
        }
    
    def get_all_status(self) -> Dict:
        """Get status of all displays"""
        status = {}
        for i in range(1, len(self.tv_ips) + 1):
            status[f"display_{i}"] = self.get_status(i)
        return status