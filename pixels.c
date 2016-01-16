/* pixels:
 *   - wrappers around SDL functions dealing with windows and surfaces
 *   - routines for manipulating surface at pixel level
 */

#include <SDL2/SDL.h>
#include <stdint.h>

typedef SDL_Window  Window;
typedef SDL_Surface Surface;
typedef SDL_Rect    Rect;

int32_t init(void)
{
	return SDL_Init(SDL_INIT_VIDEO);
}

void shutdown(void)
{
	return SDL_Quit();
}

Window* open_window(const char *title, int32_t width, int32_t height)
{
	Window* window;
	Surface* surface;

	window = SDL_CreateWindow(title, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN);
	if (window)
	{
		surface = SDL_GetWindowSurface(window);
		SDL_FillRect(surface, NULL, SDL_MapRGB(surface->format, 0x00, 0x00, 0x00));
		SDL_UpdateWindowSurface(window);
	}

	return window;
}

void close_window(Window* window)
{
	return SDL_DestroyWindow(window);
}

int32_t update_window(Window* window)
{
	return SDL_UpdateWindowSurface(window);
}

void delay(int32_t ms)
{
	return SDL_Delay(ms);
}

Surface* get_surface(Window* window)
{
	return SDL_GetWindowSurface(window);
}

Surface* new_surface(int32_t width, int32_t height)
{
	return SDL_CreateRGBSurface(0, width, height, 32, 0, 0, 0, 0);
}

void free_surface(Surface* surface)
{
	SDL_FreeSurface(surface);
}

Surface* load_bmp(const char* file_name)
{
	return SDL_LoadBMP(file_name);
}

Rect* new_rect(int32_t x0, int32_t y0, int32_t width, int32_t height)
{
	Rect* rect;

	rect = malloc(sizeof(Rect));
	rect->x = x0;
	rect->y = y0;
	rect->w = width;
	rect->w = height;

	return rect;
}

void free_rect(Rect* rect)
{
	free(rect);
}

int32_t blit(Surface* src, Rect* srcrect, Surface* dst, Rect* dstrect)
{
	return SDL_BlitSurface(src, srcrect, dst, dstrect);
}

const char* get_error()
{
	return SDL_GetError();
}

void draw_rectangle(Surface* surface, int32_t x0, int32_t y0, int32_t width, int32_t height, int32_t color)
{
	int32_t x, y;
	int32_t *p, *pa;

	x0 = x0 < 0 ? 0 : x0;
	y0 = y0 < 0 ? 0 : y0;
	width = width < 0 ? 0 : width;
	height = height < 0 ? 0 : height;

	SDL_LockSurface(surface);

	pa = (int32_t *)surface->pixels;

	for (y = y0; (y < (y0 + height)) && (y < surface->h); ++y)
	{
		p = &pa[surface->w * y];

		for (x = x0; (x < (x0 + width)) && (x < surface->w); ++x)
		{
			if (x >= 0)
			{
				p[x] = color;
			}
		}
	}

	SDL_UnlockSurface(surface);
}

void set_pixels(Surface* surface, int32_t *x, int32_t *y, int32_t *color, int32_t n)
{
	int32_t i, *p, *pa = (int32_t *)surface->pixels;

	SDL_LockSurface(surface);

	for (i = 0; i < n; ++i)
	{
		if ((x[i] >= 0 && x[i] < surface->w) && (y[i] >= 0) && (y[i] < surface->h))
		{
			p = &pa[surface->w * y[i]];
			p[x[i]] = color[i];
		}
	}

	SDL_UnlockSurface(surface);
}

void set_pixel(Surface* surface, int32_t x, int32_t y, int32_t color)
{
	set_pixels(surface, &x, &y, &color, 1);
}

void get_pixels(Surface *surface, int32_t *x, int32_t *y, int32_t *color, int32_t n)
{
	int32_t i, *p, *pa = (int32_t *)surface->pixels;

	SDL_LockSurface(surface);

	for (i = 0; i < n; ++i)
	{

		if ((x[i] >= 0) && (x[i] < surface->w) && (y[i] >= 0) && (y[i] < surface->h))
		{
			p = &pa[surface->w * y[i]];
			color[i] = p[x[i]];
		}
		else
		{
			color[i] = 0;
		}
	}

	SDL_UnlockSurface(surface);
}

void get_pixel(Surface *surface, int32_t x, int32_t y, int32_t color)
{
	get_pixels(surface, &x, &y, &color, 1);
}

