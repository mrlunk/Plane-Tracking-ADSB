# UNDER DEVELOPMENT, might not work yet ;)

import pygame

# define constants for the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# define constants for the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# define constants for the map bounds
MAP_LEFT = 4.6639
MAP_RIGHT = 5.1223
MAP_TOP = 52.3946
MAP_BOTTOM = 52.3276

# define a function to convert latitude and longitude to screen coordinates
def lat_lon_to_screen(lat, lon):
    x = (lon - MAP_LEFT) / (MAP_RIGHT - MAP_LEFT) * WINDOW_WIDTH
    y = (MAP_TOP - lat) / (MAP_TOP - MAP_BOTTOM) * WINDOW_HEIGHT
    return (int(x), int(y))

# create a Pygame window
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# load the font
font = pygame.font.SysFont(None, 24)

# read in the data
data = []
with open("data.txt") as f:
    for line in f:
        parts = line.strip().split("|")
        dt = parts[0].split(": ")[1]
        ti = parts[1].split(": ")[1]
        hex = parts[2].split(": ")[1].strip()
        flt = parts[3].split(": ")[1].strip()
        spd = float(parts[4].split(": ")[1])
        dist = float(parts[5].split(": ")[1].strip().split(" ")[0])
        alt = int(parts[6].split(": ")[1].strip().split(" ")[0])
        lat = float(parts[7].split(": ")[1])
        lon = float(parts[8].split(": ")[1])
        data.append((dt, ti, hex, flt, spd, dist, alt, lat, lon))

# draw the map
screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 1)
for lat in range(int(MAP_BOTTOM * 100), int(MAP_TOP * 100) + 1):
    for lon in range(int(MAP_LEFT * 100), int(MAP_RIGHT * 100) + 1):
        if lat % 5 == 0 and lon % 5 == 0:
            x, y = lat_lon_to_screen(lat / 100.0, lon / 100.0)
            pygame.draw.circle(screen, BLACK, (x, y), 2, 0)

# draw the planes
for dt, ti, hex, flt, spd, dist, alt, lat, lon in data:
    x, y = lat_lon_to_screen(lat, lon)
    pygame.draw.circle(screen, RED, (x, y), 5, 0)
    text = font.render(flt, True, BLACK)
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y + 15
    screen.blit(text, text_rect)

# update the display
pygame.display.update()

# wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
           
