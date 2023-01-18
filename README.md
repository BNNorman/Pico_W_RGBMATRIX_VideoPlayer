# Pico_W_RGBMATRIX_VideoPlayer
Cicuitpython code to receive video images to playback on RGB Matrix plus Python code to send the video frames.

This code uses a Pico W and Waveshare Pico-RGB-Matrix-P3-64x32 panel (From the Pi Hut) to display video frames on the matrix. By slowing down the rate of sending it could be a slideshow.

The panel is great, you plug the Pico W into the socket on the back of it. There's a smoky acrylic screen which helps a little and a spare Pico compatible socket to add extra hardware to it.

During testing I used a Python program running on my PC to send the video frames using UDP. Both devices were on my home network but the Pico W could be setup as an access point (IP addr like 182.168.4.1) so that point to point comms could take place without going through a WiFi router.

I used a snippet from Shrek for testing.

Enjoy

# Files

VideoSender.py - Standard Python 3 code does what it says on the tin. Edit the code to chose your own video or slideshow. (MP4)
VideoReceiver.py - CircuitPython 8.0.0 beta 6 code which captures the UDP packets and displays the image on the RGB Matrix 
secrets.py - holds your Wifi ssid and password
