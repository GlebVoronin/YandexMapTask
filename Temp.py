import pygame
import requests

pygame.init()
coords = (139.56, 35.56)
scale = (0.005, 0.005)
size = (600, 450)

geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "ll": str(coords[0]) + ',' + str(coords[1]),
    "spn": str(scale[0]) + ',' + str(scale[1]),
    "z": "13",
    "l": "map"}
try:
    response = requests.get(geocoder_api_server, params=geocoder_params)
    img = response.content
    file = open('new_img_for_yandex_map', 'wb')
    file.write(img)
    file.close()
    img = pygame.image.load('new_img_for_yandex_map')
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(img, (0, 0))
        pygame.display.flip()
except Exception:
    print("error")
    pygame.quit()
