#!/usr/bin/python
import Adafruit_CharLCD as LCD
import time


class Menu(object):

    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    YELLOW = (1, 1, 0)
    CYAN = (0, 1, 1)
    MAGENTA = (1, 0, 1)
    WHITE = (1, 1, 1)
    NOT_ACTIVE = '\x00'
    ACTIVE = '\x01'

    def __init__(self, lcd_instance, selectable=False):
        self.__lcd = lcd_instance
        self.__items = []
        self.selectable = selectable
        self.top = True
        self.first = True
        self.last = False
        self.position = 0
        self.color = Menu.GREEN

    def register_menuitem(self, item, func):
        self.__items.append((item, func))

    def red(self):
        self.color = Menu.RED
        self.__lcd.set_color(Menu.RED)

    def green(self):
        self.color = Menu.GREEN
        self.__lcd.set_color(Menu.GREEN)

    def blue(self):
        self.color = Menu.BLUE
        self.__lcd.set_color(Menu.BLUE)

    def yellow(self):
        self.color = Menu.YELLOW
        self.__lcd.set_color(Menu.YELLOW)

    def cyan(self):
        self.color = Menu.CYAN
        self.__lcd.set_color(Menu.CYAN)

    def magenta(self):
        self.color = Menu.MAGENTA
        self.__lcd.set_color(Menu.MAGENTA)

    def white(self):
        self.color = Menu.WHITE
        self.__lcd.set_color(Menu.WHITE)

    def bell(self):
        self.__lcd.set_backlight(False)
        time.sleep(0.05)
        self.__lcd.set_backlight(True)
        self.__lcd.set_color(*self.color)

    def write_top(self, text):
        self.__lcd.set_cursor(0, 0)
        self.__lcd.message(text)

    def write_bottom(self, text):
        self.__lcd.set_cursor(0, 1)
        self.__lcd.message(text)

    def down(self):
        if len(self.__items) == 1:
            self.bell()
            self.last = True
            return
        if self.position >= len(self.__items)-1:
            self.last = True
            self.bell()
            return
        self.position += 1
        self.first = False
        # TODO: Branch for selectable / non-selectable options
        self.write_top(self.__items[self.position-1][0].repr(

        )+Menu.NOT_ACTIVE)
        self.write_bottom(self.__items[self.position][0].repr(

        )+Menu.ACTIVE)

    def up(self):
        if len(self.__items) == 1:
            self.bell()
            self.first = True
            return
        if self.position == 0:
            self.first = True
            self.bell()
            return
        self.position -= 1
        self.last = False
        # TODO: Branch for selectable / non-selectable options
        self.write_top(self.__items[self.position][0].repr()+Menu.ACTIVE)
        self.write_bottom(self.__items[self.position+1][0].repr()+Menu.NOT_ACTIVE)

    def loop(self):
        self.write_top(self.__items[self.position][0].repr()+Menu.ACTIVE)
        if len(self.__items) > 1:
            self.write_bottom(self.__items[self.position+1][0].repr(

            )+Menu.NOT_ACTIVE)
        while True:
            if self.__lcd.is_pressed(LCD.DOWN):
                self.down()
            elif self.__lcd.is_pressed(LCD.UP):
                self.up()
            # TODO: Add select, back, OK
            elif self.__lcd.is_pressed(LCD.SELECT):
                self.__items[self.position][1]()


class MenuItem(object):
    def __init__(self, text, checked=False, fillchar=' '):
        self.text = text
        self.checked = checked
        self.fillchar = fillchar

    def __repr(self):
        if len(self.text) >= 15:
            return self.text[:15]
        fill_len = 15 - len(self.text)
        return self.text + (self.fillchar * fill_len)

    def __repr_selectable(self):
        if len(self.text) >= 14:
            return self.text[:14]
        fill_len = 14 - len(self.text)
        return self.text + (self.fillchar * fill_len)

    def repr(self):
        return self.__repr()

    def repr_selectable(self):
        if self.checked:
            return '\x01'+self.__repr_selectable()
        return '\x00'+self.__repr_selectable()


if __name__ == '__main__':

    global lcd
    lcd = LCD.Adafruit_CharLCDPlate()

    # Ticks - nonchecked and checked
    lcd.create_char(0, [31, 17, 17, 17, 17, 17, 17, 31])
    lcd.create_char(1, [31, 17, 21, 21, 21, 21, 17, 31])
    lcd.create_char(2, [0, 0, 0, 0, 4, 0, 0, 0])
    lcd.create_char(3, [0, 0, 0, 4, 14, 4, 0, 0])

    lcd.set_color(*Menu.GREEN)
    lcd.clear()
    lcd.message('Initialising\x02\x03')
    menu = Menu(lcd)
    menu.bell()
    time.sleep(3)
    items = [
        MenuItem('PwnAll', fillchar='.'),
        MenuItem('PwnSSID', fillchar='.'),
        MenuItem('PwnExceptSSID', fillchar='.'),
        MenuItem('PwnMAC', fillchar='.'),
        MenuItem('PwnExceptMAC', fillchar='.'),
        MenuItem('ScanSSIDs', fillchar='.'),
        MenuItem('ScanMACs', fillchar='.'),
        MenuItem('TailLogs', fillchar='.')
    ]
    menu.bell()
    for item in items:
        menu.register_menuitem(item, lambda: '__placeholder_function__')
    menu.loop()
