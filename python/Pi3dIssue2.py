import threading

from graphics.pi3d import pi3d

ENABLE_BUG = True

# Setup display and initialise pi3d
scnx = 800
scny = 600

display = pi3d.display()

display.create2D(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(1.0,0.2,0.6,1)

texs = pi3d.textures()

bbtitle = texs.loadTexture("graphics/pi3d/textures/pi3dbbd.png",True)

# Fetch key presses
mykeys = pi3d.key()

def run():
  while True:
    display.clear()
    if not ENABLE_BUG:
      pi3d.rectangle(bbtitle,5,scny,256+5,32)
    display.swapBuffers()

if ENABLE_BUG:
  thread = threading.Thread(target=run)
  thread.start()
  thread.join()

else:
  run()
