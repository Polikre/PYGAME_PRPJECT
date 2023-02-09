import pygame as p
import sys
import os


clock = p.time.Clock()
FPS = 10
WIDTH = 1000
HEIGHT = 1000
SIZE_W = 10
SIZE_H = 10
tile_width = tile_height = 100


p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
running = True
p.mouse.set_visible(0)
player = None
all_sprites = p.sprite.Group()
tiles_group = p.sprite.Group()
player_group = p.sprite.Group()
boxes_group = p.sprite.Group()


def load_image(name, colorkey=None, W_TMP=10, H_TMP=10):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = p.image.load(fullname)
    image = p.transform.scale(image, (SIZE_W * W_TMP, SIZE_H * H_TMP))
    if name == "drago_sheet8*2.png":
        print(image.get_size())
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    p.quit()
    sys.exit()


def start_screen():
    intro_text = [""]
    fon = p.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = p.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, p.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                terminate()
            elif event.type == p.KEYDOWN or \
                    event.type == p.MOUSEBUTTONDOWN:
                return
        p.display.flip()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Player(p.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sheet=load_image("hero.png", -1, 100, 45), columns=10, rows=8):
        super().__init__(player_group)
        self.x12 = pos_x
        self.y12 = pos_y
        self.died = False
        self.current = "stand"
        self.numToWord = {1: "stand", 2: "alert", 3: "shot", 4: "walk", 5: "run", 6: "jump", 7: "hit", 8: "die"}
        self.WordToNum = {i: j for j, i in self.numToWord.items()}
        self.frames = {"walk": [], "die": [], "stand": [], "shot": [], "alert": [], "run": [], "jump": [], "hit": []}
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.current][self.cur_frame]
        self.image = p.transform.scale(self.image, (tile_width, tile_height))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = p.Rect(self.x12 * tile_width, self.y12 * tile_height, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[self.numToWord[j + 1]].append(sheet.subsurface(p.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.current][self.cur_frame]
        self.image = p.transform.scale(self.image, (tile_width, tile_height))

    def update_condition(self, cur):
        self.current = cur
        self.cur_frame = 0

    def moved_animation(self, screen, clock):




        '''framesPerSquare = 10
        frameCount = (abs(dR) + abs(dC)) * framesPerSquare
        for frame in range(frameCount + 1):
            r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_
        SIZE, move.endRow * SQ_
        SIZE, SQ_
        SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)  # draw captured piece onto rectangle if move.pieceCaptured != '-.
        screen.blit(IMAGES[move - pieceCaptured], endSquare)  # draw moving piece
        screen.blit(IMAGES[move - pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_
        SIZE, SQ_
        SIZE, SQ_SIZE)) p.display.flip()
        clock.tick(60)'''


tile_images = {
    'wall': load_image('box.jpg'),
    'empty': load_image('grass.jpg')
}


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, screen, clock):
        frame_hours = 20
        frame_count = (self.dx + self.dy) // frame_hours
        print(frame_count)
        for frame in range(1, frame_hours + 1):
            print(frame)
            r = self.dx * frame // frame_count
            c = self.dy * frame // frame_count
            for sprite in all_sprites:
                sprite.rect.x += r
                sprite.rect.y += c
                if p.sprite.spritecollideany(player, boxes_group):
                    sprite.rect.x -= r
                    sprite.rect.y -= c
            screen.fill((255, 255, 255))
            player_group.update()
            all_sprites.draw(screen)
            player_group.draw(screen)
            p.display.flip()
            clock.tick(60)

    def update_(self, event):
        if event.key == p.K_LEFT:
            self.dx = tile_width
            self.dy = 0
        if event.key == p.K_RIGHT:
            self.dx = -tile_width
            self.dy = 0
        elif event.key == p.K_UP:
            self.dy = tile_height
            self.dx = 0
        elif event.key == p.K_DOWN:
            self.dy = -tile_height
            self.dx = 0

    def concern(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy


class Tile(p.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Boxes(p.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(boxes_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    zn = (0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Boxes('wall', x, y)
            elif level[y][x] == '@':
                zn = (x, y)
                Tile('empty', zn[0], zn[1])
                new_player = Player(zn[0], zn[1])
    return new_player, x, y


text = "map.txt"
try:
    map_level = load_level(text)
    SIZE_W = len(map_level[0])
    SIZE_H = len(map_level)
    start_screen()
    player, level_x, level_y = generate_level(load_level(text))
    camera = Camera()
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                camera.update_(event)
                camera.apply(screen, clock)
        screen.fill((255, 255, 255))
        player_group.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        p.display.flip()
    p.quit()
except FileNotFoundError:
    print("Такого файла не существует")