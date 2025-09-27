"""
Simple GUI for PCTracker application.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pystray
from PIL import Image
import os

from tracker import UsageTracker
from config import config
from autostart import AutoStart


class PCTrackerGUI:
    """Simple GUI for PCTracker."""
    
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("PCTracker - Computer Usage Monitor")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Set window icon
        try:
            icon_path = "assets/logo.ico"
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set window icon: {e}")
        
        # Initialize components
        self.tracker = UsageTracker()
        self.tracker.add_callback(self.on_data_update)
        self.autostart = AutoStart()
        
        # Enable auto-start automatically
        if not self.autostart.is_enabled():
            self.autostart.setup_autostart()
        
        # UI variables
        self.is_tracking = tk.BooleanVar(value=True)
        self.current_time = tk.StringVar(value="00:00:00")
        self.today_time = tk.StringVar(value="00:00:00")
        self.update_job = None
        self.is_closing = False
        self.chart_canvas = None  # Store chart canvas reference
        self.tray_icon = None  # Store tray icon reference
        
        # Create UI
        self.create_widgets()
        self.setup_layout()
        
        # Start tracking automatically
        self.tracker.start_tracking()
        
        # Start update loop
        self.update_display()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        
        # Header section
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="PCTracker",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Computer Usage Time Monitor",
            font=ctk.CTkFont(size=12)
        )
        
        
        # Time display section
        self.time_frame = ctk.CTkFrame(self.main_frame)
        
        # Current session frame
        self.current_frame = ctk.CTkFrame(self.time_frame)
        self.current_label = ctk.CTkLabel(
            self.current_frame,
            text="Current Session:",
            font=ctk.CTkFont(size=12)
        )
        self.current_time_label = ctk.CTkLabel(
            self.current_frame,
            textvariable=self.current_time,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Today's usage frame
        self.today_frame = ctk.CTkFrame(self.time_frame)
        self.today_label = ctk.CTkLabel(
            self.today_frame,
            text="Today's Usage:",
            font=ctk.CTkFont(size=12)
        )
        self.today_time_label = ctk.CTkLabel(
            self.today_frame,
            textvariable=self.today_time,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Chart section
        self.chart_frame = ctk.CTkFrame(self.main_frame)
        self.chart_label = ctk.CTkLabel(
            self.chart_frame,
            text="Weekly Usage Chart",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
    
    def setup_layout(self):
        """Setup widget layout."""
        # Main frame
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame.pack(fill="x", pady=(0, 10))
        self.title_label.pack(pady=(10, 5))
        self.subtitle_label.pack(pady=(0, 10))
        
        
        # Time display
        self.time_frame.pack(fill="x", pady=(0, 15))
        self.time_frame.pack_propagate(False)
        self.time_frame.configure(height=60)
        
        # Arrange time display frames
        self.current_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.current_label.pack(side="left", padx=5)
        self.current_time_label.pack(side="left", padx=5)
        
        self.today_frame.pack(side="right", fill="x", expand=True, padx=10, pady=10)
        self.today_label.pack(side="left", padx=5)
        self.today_time_label.pack(side="left", padx=5)
        
        # Chart
        self.chart_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.chart_label.pack(pady=10)
        self.create_chart()
        
    
    def create_chart(self):
        """Create weekly usage chart."""
        try:
            # Get weekly data
            weekly_data = self.tracker.get_weekly_usage()
            
            # Create simple bar chart
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            # Prepare data
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            hours = []
            
            for i in range(7):
                date = (datetime.now().date() - timedelta(days=datetime.now().weekday() - i)).isoformat()
                day_data = weekly_data['days'].get(date, {})
                hours.append(day_data.get('total_time', 0) / 3600)  # Convert to hours
            
            # Create bar chart
            bars = ax.bar(days, hours, color='#1f538d')
            ax.set_ylabel('Hours', color='white')
            ax.set_title('Weekly Usage', color='white')
            ax.tick_params(colors='white')
            
            # Style the chart
            for bar in bars:
                bar.set_facecolor('#1f538d')
            
            # Embed chart in tkinter
            self.chart_canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creating chart: {e}")
    
    def refresh_chart(self):
        """Refresh the chart display."""
        try:
            if self.chart_canvas:
                self.chart_canvas.draw()
        except Exception as e:
            print(f"Error refreshing chart: {e}")
    
    
    def on_data_update(self, data):
        """Handle data updates from tracker."""
        if data['type'] == 'session_update':
            # Update current session time
            duration = data['data']['duration']
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            self.current_time.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def update_display(self):
        """Update display with current data."""
        if not self.is_closing:
            # Update today's usage
            today_usage = self.tracker.get_today_usage()
            total_seconds = today_usage.get('total_time', 0)
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            self.today_time.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # Schedule next update
            self.update_job = self.root.after(1000, self.update_display)
    
    
    
    def minimize_to_tray(self):
        """Minimize window to system tray."""
        self.root.withdraw()
        # Create tray icon in a separate thread to avoid blocking
        import threading
        tray_thread = threading.Thread(target=self.create_tray_icon, daemon=True)
        tray_thread.start()
    
    def create_tray_icon(self):
        """Create system tray icon."""
        try:
            # Load icon from assets
            icon_path = "assets/logo.ico"
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                # Resize to appropriate size for tray icon
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
            else:
                # Fallback to simple blue icon
                image = Image.new('RGB', (64, 64), color='blue')
            
            menu = pystray.Menu(
                pystray.MenuItem("Show Window", self.show_window),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("PCTracker", image, "PCTracker", menu)
            self.tray_icon.run()
        except Exception as e:
            print(f"Error creating tray icon: {e}")
            self.show_window()
    
    def show_window(self):
        """Show main window."""
        # Stop tray icon if running
        if self.tray_icon:
            try:
                self.tray_icon.stop()
                self.tray_icon = None
            except:
                pass
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        # Refresh chart to fix white screen issue
        self.root.after(100, self.refresh_chart)
    
    def quit_app(self):
        """Quit application."""
        self.is_closing = True
        self.tracker.stop_tracking()
        
        # Stop tray icon if running
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except:
                pass
        
        self.root.quit()
        self.root.destroy()
    
    def on_closing(self):
        """Handle window closing."""
        if config.get("gui", "minimize_to_tray"):
            self.minimize_to_tray()
        else:
            self.quit_app()
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()


def main():
    """Main function for GUI."""
    app = PCTrackerGUI()
    app.run()


if __name__ == "__main__":
    main()
