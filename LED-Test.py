from rpi_ws281x import *
from time import sleep

LED_COUNT      = 39    
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_BRIGHTNESS = 150     
LED_INVERT     = False   
LED_CHANNEL    = 0  
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


for i in range(LED_COUNT):
    print("Lighting LED " + str(i))
    if i > 0:
        strip.setPixelColor(i-1, Color(0,0,0))
        strip.setPixelColor(i, Color(100,100,100))
        strip.show()
        sleep(0.5)
    else:
        strip.setPixelColor(i, Color(100,100,100))
        strip.show()
        sleep(0.5)
