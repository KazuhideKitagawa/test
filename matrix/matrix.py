#!/usr/bin/env python

import time
import MakeLumaFont
from luma.led_matrix.device import max7219
from luma.core.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


myFontObj=MakeLumaFont.MakeLumaFont()
myFont=myFontObj.main()

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
msg='UTF-8の漢字も表示できます'

for i in range(0,10):
    show_message(device, msg, fill="white", font=proportional(myFont))
    time.sleep(1)

print(msg)

