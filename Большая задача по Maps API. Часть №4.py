import pygame
import requests
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
coords = [139.56, 35.56]
scale = [0.005, 0.005]
size = (600, 450)
l_list = ['map', 'sat', 'sat,skl']
l_index = 0


def load_map():
    global l_index
    if l_index > len(l_list) - 1:
        l_index %= len(l_list)
    elif l_index < 0:
        l_index = len(l_list) - 1
    geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "ll": str(coords[0]) + "," + str(coords[1]),
        "spn": str(scale[0]) + "," + str(scale[1]),
        "z": "13",
        "l": l_list[l_index]}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    img = response.content
    file = open('new_img_for_yandex_map', 'wb')
    file.write(img)
    file.close()


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        surface = pygame.Surface((50, 50))
        surface.fill((150, 150, 150))
        self.image = surface
        self.rect = self.image.get_rect()

    def on_click(self):
        global l_index
        l_index += 1


try:
    load_map()
    img = pygame.image.load('new_img_for_yandex_map')
    screen = pygame.display.set_mode(size)
    running = True
    font = pygame.font.Font(None, 25)
    text = font.render('Слой', 1, (0, 0, 0))
    button = Button()
    button.rect.x, button.rect.y = 550, 0
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if scale[0] < 10:
                        scale[0] *= 2
                        scale[1] *= 2
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_PAGEDOWN:
                    if scale[0] > 0.0001:
                        scale[0] /= 2
                        scale[1] /= 2
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_DOWN:
                    if coords[1] > -90:
                        coords[1] -= scale[1] * 1.3
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_UP:
                    if coords[1] < 90:
                        coords[1] += scale[1] * 1.3
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                if event.key == pygame.K_RIGHT:
                    if coords[0] < 180:
                        coords[0] += scale[0] * 1.3
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_LEFT:
                    if coords[0] > -180:
                        coords[0] -= scale[0] * 1.3
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button.rect.x < event.pos[0] < button.rect.x + button.rect.w and
                        button.rect.y < event.pos[1] < button.rect.y + button.rect.h):
                    button.on_click()
                    load_map()
                    img = pygame.image.load('new_img_for_yandex_map')
        screen.blit(img, (0, 0))
        screen.blit(button.image, (550, 0))
        screen.blit(text, (550, 0))

        pygame.display.flip()
except Exception as err:
    print(f"{err}")
    pygame.quit()
