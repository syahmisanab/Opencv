import time
import smbus2
import signal

LCD_ADDR = 0x27  
bus = smbus2.SMBus(1)

LCD_CHR = 1  # Data mode
LCD_CMD = 0  # Command mode
LCD_BACKLIGHT = 0x08  # Backlight ON
ENABLE = 0b00000100  # Enable bit

def lcd_byte(bits, mode):
    high_bits = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
    bus.write_byte(LCD_ADDR, high_bits)
    bus.write_byte(LCD_ADDR, high_bits | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, high_bits & ~ENABLE)
    bus.write_byte(LCD_ADDR, low_bits)
    bus.write_byte(LCD_ADDR, low_bits | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, low_bits & ~ENABLE)
    
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # Display ON, Cursor OFF
    lcd_byte(0x28, LCD_CMD)  # 2-line mode, 5x8 font
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(0.2)
    
def lcd_display(text):
    lcd_byte(0x80, LCD_CMD)  # Move to first line
    for char in text:
        lcd_byte(ord(char), LCD_CHR)
def lcd_clear():
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(0.2)
    
def signal_handler(sig, frame):
    print("\nClearing LCD and exiting...")
    lcd_clear()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_lcd_demo():
    """Run a simple LCD demo: display 'Autobotic' and keep running."""
    lcd_init()
    lcd_display("Autobotic")

    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        pass

# run code
run_lcd_demo()
