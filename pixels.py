import ctypes

libpixels = ctypes.cdll.LoadLibrary('./libpixels.so')

class PixelsError(BaseException):
	pass

def cwrap(x):
	if x is None:
		return ctypes.c_void_p(0)
	if isinstance(x, str):
		return ctypes.c_char_p(bytes(x, 'ASCII'))
	if type(x).__name__ == 'int':
		return ctypes.c_int32(x)
	raise ValueError

def init():
	libpixels.init()
	
def shutdown():
	libpixels.shutdown()

def get_error():
	return libpixels.get_error().value

def delay(ms):
	return libpixels.delay(cwrap(ms))

class Window():
	def __init__(self, width, height, title=''):
		self.window = libpixels.open_window(cwrap(title), cwrap(width), cwrap(height))

	def surface(self): # XXX error handling..
		return Surface(surface=libpixels.get_surface(self.window))

	def refresh(self): # XXX error handling
		return libpixels.update_window(self.window)

	def close(self):
		if self.window is not None:
			r = libpixels.close_window(self.window)
			self.window = None
			if r != 0:
				raise PixelsError('libpixels.close_window()', get_error())

class Surface():
	def __init__(self, surface=None, window=None, width=None, height=None, load=None):
		if surface is not None:
			self.surface = surface
		elif window is not None:
			self.surface = libpixels.get_surface(window)
			if not self.surface:
				raise PixelsError('libpixels.get_surface()', get_error())
		elif load is not None:
			self.surface = libpixels.load_bmp(cwrap(load))
			if not self.surface:
				raise PixelsError('libpixels.load_bmp()', get_error())
		elif width is not None and height is not None:
			self.surface = libpixels.new_surface(cwrap(width), cwrap(height))
			if not self.surface:
				raise PixelsError('libpixels.new_surface()', get_error())
		else:
			self.surface = None

	def blit(self, dst, src_rect=None, dst_rect=None):
		if libpixels.blit(self.surface, cwrap(src_rect), dst.surface, cwrap(dst_rect)):
			raise PixelsError('libpixels.blit()', get_error())

	def draw_rectangle(self, x, y, width, height, color):
		libpixels.draw_rectangle(self.surface, cwrap(x), cwrap(y), cwrap(width), cwrap(height), cwrap(color))

	def set_pixel(self, x, y, color):
		libpixels.set_pixel(self.surface, cwrap(x), cwrap(y), cwrap(color))

#	def get_pixel(self) ...

	def free(self):
		if self.surface is not None:
			if libpixels.free_surface(self.surface):
				raise PixelsError('libpixels.free_surface()', get_error)
			self.surface = None

class Rect():
	def __init__(self, width, height, x=0, y=0):
		self.rect = libpixels.new_rect(x, y, width, height)
		if not self.rect:
			raise PixelsError('libpixels.new_rect(); out of memory')

	def free(self):
		if self.rect is not None:
			libpixels.free_rect(self.rect)
		self.rect = None

