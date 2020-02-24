import pygame
import requests

pygame.init()
coords = [139.56, 35.56]
scale = [0.005, 0.005]
size = (600, 450)


def load_map():
    geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "ll": str(coords[0]) + "," + str(coords[1]),
        "spn": str(scale[0]) + "," + str(scale[1]),
        "l": "map"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    img = response.content
    file = open('new_img_for_yandex_map', 'wb')
    file.write(img)
    file.close()


try:
    load_map()
    img = pygame.image.load('new_img_for_yandex_map')
    screen = pygame.display.set_mode(size)
    running = True

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
                    if coords[1] - scale[1] * 1.5 > -85:
                        coords[1] -= scale[1] * 1.5
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_UP:
                    if coords[1] + scale[1] * 1.5 < 85:
                        coords[1] += scale[1] * 1.5
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                if event.key == pygame.K_RIGHT:
                    if coords[0] + scale[0] * 1.5 < 180:
                        coords[0] += scale[0] * 1.5
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
                elif event.key == pygame.K_LEFT:
                    if coords[0] - scale[0] * 1.5 > -180:
                        coords[0] -= scale[0] * 1.5
                        load_map()
                        img = pygame.image.load('new_img_for_yandex_map')
        screen.blit(img, (0, 0))
        pygame.display.flip()
except Exception:
    print("error")
    pygame.quit()
