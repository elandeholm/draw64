import time
from random import randint
import pixels

class C64Graphics():
	WIDTH    = 320
	HEIGHT   = 200
	OSWIDTH  = 384
	OSHEIGHT = 272
	XSTART   =  (OSWIDTH  - WIDTH)  // 2
	YSTART    = (OSHEIGHT - HEIGHT) // 2
	PALETTE = (
		0x101010, 0xffffff, 0xe04040, 0x60ffff,
		0xe060e0, 0x40e040, 0x4040e0, 0xffff40,
		0xe0a040, 0x9c7448, 0xffa0a0, 0x545454,
		0x888888, 0xa0ffa0, 0xa0a0ff, 0xc0c0c0 )

	def __init__(self, title='', message=''):
		self.window = pixels.Window(width=self.OSWIDTH, height=self.OSHEIGHT, title=title)
		self.surface = self.window.surface()

		self.surface.draw_rectangle(0, 0, self.OSWIDTH, self.OSHEIGHT, self.PALETTE[3])
		self.surface.draw_rectangle(self.XSTART, self.YSTART, self.WIDTH, self.HEIGHT, self.PALETTE[8])
		self.set_color(3)

	def set_color(self, c):
		self.color = self.PALETTE[c]

	def draw_rectangle(self, x0, y0, width, height, overscan=False):
		self.surface.draw_rectangle(
			x=(x0 if overscan else x0 + self.XSTART),
			y=(y0 if overscan else y0 + self.YSTART),
			width=width,
			height=height,
			color=self.color)

	def draw_hline(self, x0, y0, length, overscan=False):
		self.draw_rectangle(x0=x0, y0=y0, width=length, height=1, overscan=overscan)

	def draw_vline(self, x0, y0, length, overscan=False):
		self.draw_rectangle(x0=x0, y0=y0, width=1, height=length, overscan=overscan)

	def refresh(self):
		self.window.refresh()

	def sleep(self, ms):
		pixels.delay(ms)

if __name__ == '__main__':
	c64graphics = C64Graphics('Commodore 64 graphics')


	raster_bars = (
		(   # std grey gradient
			0x00, 0x00, 0x0b, 0x00, 0x0b, 0x0b, 0x0c, 0x0b, 0x0c, 0x0c, 0x0f, 0x0c, 0x0f, 0x0f, 0x01, 0x0f,
			0x01, 0x01, 0x0f, 0x01, 0x0f, 0x0f, 0x0c, 0x0f, 0x0c, 0x0c, 0x0b, 0x0c, 0x0b, 0x0b, 0x00, 0x0b
		),
		(   # green gradient
			0x00, 0x00, 0x0b, 0x00, 0x0b, 0x0b, 0x05, 0x0b, 0x05, 0x05, 0x0d, 0x05, 0x0d, 0x0d, 0x01, 0x0d,
			0x01, 0x01, 0x0d, 0x01, 0x0d, 0x0d, 0x05, 0x0d, 0x05, 0x05, 0x0b, 0x05, 0x0b, 0x0b, 0x00, 0x0b
		),
		(   # blue gradient
			0x00, 0x00, 0x0b, 0x00, 0x0b, 0x0b, 0x06, 0x0b, 0x06, 0x06, 0x0e, 0x06, 0x0e, 0x0e, 0x01, 0x0e,
			0x01, 0x01, 0x0e, 0x01, 0x0e, 0x0e, 0x06, 0x0e, 0x06, 0x06, 0x0b, 0x06, 0x0b, 0x0b, 0x00, 0x0b
		),
		(   # red gradient
			0x00, 0x00, 0x0b, 0x00, 0x0b, 0x0b, 0x02, 0x0b, 0x02, 0x02, 0x0a, 0x02, 0x0a, 0x0a, 0x01, 0x0a,
			0x01, 0x01, 0x0a, 0x01, 0x0a, 0x0a, 0x02, 0x0a, 0x02, 0x02, 0x0b, 0x02, 0x0b, 0x0b, 0x00, 0x0b
		) )

	vv = [ [ x, y ] for x in range(8) for y in range(6) if y <= x]

	l = len(vv)

	for n in range(666):
		j = randint(0, l-1)
		n_l = n % l
		tmp = vv[n_l]
		vv[n_l] = vv[j]
		vv[j] = tmp

	for x, y in vv:
		for i, c in enumerate(raster_bars[randint(0, 3)]):
			c64graphics.set_color(c)
			c64graphics.draw_hline(x0=0, y0=(48 * y + i), length=384, overscan=True)
		for i, c in enumerate(raster_bars[randint(0, 3)]):
			c64graphics.set_color(c)
			c64graphics.draw_vline(x0=(4 + 48 * x + i), y0=0, length=272, overscan=True)
		c64graphics.refresh()
		c64graphics.sleep(5)

	c64graphics.refresh()


	c64graphics.sleep(5000)

	pixels.shutdown()

