import pygame
from pygame.locals import *
import random

pygame.init()

# Tạo màu nền
gray = (100, 100, 100)
green = (76, 208, 56)
yellow = (255, 232, 0)
red = (200, 0, 0)
white = (255, 255, 255)

# Tạo cửa sổ game
width = 500
height = 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game Car")

# Khởi tạo biến
gameover = False
speed = 2
score = 0

# Khởi tạo đường
road_width = 300
street_width = 10
street_height = 50

# Lane đường
lane_left = 150
lane_center = 250
lane_right = 350
lanes = [lane_left, lane_center, lane_right]

lane_move_y = 0

# Road và edge
road = (100, 0, road_width, height)
left_edge = (95, 0, street_width, height)
right_edge = (395, 0, street_width, height)

# Vị trí xe start
player_x = 250
player_y = 400

# Đối tượng xe ngẫu nhiên
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Tỉ lệ ảnh xe
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Xe player
class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('image/car.png')
         
        super().__init__(image,x,y)
        

# Sprite group
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Tạo xe player
player = PlayerVehicle(player_x, player_y)
player_group.add(player)
#load xe ngẫu nhiên
image_name=['pickup_truck.png', 'semi_trailer.png','taxi.png','van.png']
Vehicle_image=[]
for name in image_name:
    image=pygame.image.load('image/'+name)
    Vehicle_image.append(image)
#Load hình va chạm
crash=pygame.image.load('image/crash.png')
crash_rect=crash.get_rect()
# Vòng lặp
# Cài đặt FPS
clock = pygame.time.Clock()
fps = 120
running = True

while running:
    # Chỉnh khung hình/s
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        #điều khiển xe
        if event.type ==KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0]>lane_left:
                player.rect.x-=100
            if event.key == K_RIGHT and player.rect.center[0]<lane_right:
                player.rect.x+=100
            #chek lỗi
        for verhicle in vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover=True
    #chek lỗi khi xe đứng yên
    if pygame.sprite.spritecollide(player,vehicle_group,True):
        gameover = True
        #nổ xe
        crash_rect.center=[player.rect.center[0],player.rect.top]
    # Vẽ cỏ
    screen.fill(green)
    
    # Vẽ đường
    pygame.draw.rect(screen, gray, road)
    
    # Vẽ hành lang đường
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)
    
    # Vẽ làn đường
    lane_move_y += speed * 2
    if lane_move_y >= street_height * 2:
        lane_move_y = 0
    
    for y in range(street_height * -2, height, street_height * 2):
        pygame.draw.rect(screen, white, (lane_left + 45, y + lane_move_y, street_width, street_height))
        pygame.draw.rect(screen, white, (lane_center + 45, y + lane_move_y, street_width, street_height))
    
    # Vẽ xe player
    player_group.draw(screen)
    
    # Thêm xe ngẫu nhiên
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.y < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(Vehicle_image)
            vehicle = Vehicle(image, lane, -100)
            vehicle_group.add(vehicle)
    
    # Di chuyển và vẽ các xengẫu nhiên
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # Kiểm tra va chạm với xe player
        if pygame.sprite.spritecollide(player, vehicle_group, False):
            # Xử lý khi xe player va chạm với xe ngẫu nhiên
            # Ở đây, bạn có thể thêm các xử lý như kết thúc trò chơi hoặc trừ đi điểm số, tùy theo logic của trò chơi của bạn.
            pass
        
        # Xóa các xe đã vượt qua màn hình
        if vehicle.rect.y > height:
            vehicle.kill()
            score += 1
            # Tăng tốc độ game sau mỗi lượt
            if score > 0 and score % 5 == 0:
                speed += 1
    
    # Vẽ nhóm xe ngẫu nhiên
    vehicle_group.draw(screen)
    #hiển thị điểm 
    font=pygame.font.Font(pygame.font.get_default_font(),16)
    text=font.render('Điểm: '+str(score),True,white)
    text_rect=text.get_rect()
    text_rect.center=(50,40)
    screen.blit(text,text_rect)
    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        font=pygame.font.Font(pygame.font.get_default_font(),16)
        text=font.render('Game OVER! Tiep Tuc( Y / N ) ',True,white)
        text_rect=text.get_rect()
        text_rect.center=(width/2,100)
        screen.blit(text,text_rect)
        
    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type ==KEYDOWN:
                if event.key == K_y:
                     #reset 
                     gameover = False
                     score = 0
                     speed = 2
                     #làm rỗng length
                     vehicle_group.empty()
                     player.rect.center=[player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()