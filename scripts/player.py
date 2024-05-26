import pygame


class Player:
    def __init__(self, game, screen,  pos, y_difference=0):
        self.surf = screen
        self.game = game
        self.pos = list(pos)
        self.screen = screen
        self.switch = 30
        #animation attributes
        self.action =  ''
        # Movement attributes
        self.flip = False
        self.speed = 3
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.img = self.game.assets['player']
        self.d = y_difference
        self.size = self.img.get_size()
        self.r = False
        self.air_time = 0
        
    #get the rect of the player for the purposes of collision detection
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.size)


    #update our position and handle collision based on user input and change the animation
    def update(self, tilemap, movement=(0, 0)):
        #set collisions in all directions to be false at the start of the frame
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        #update the frame movement based on the the user input
        frame_movement = (movement[0] * self.speed + self.velocity[0],movement[1] + self.velocity[1])
        self.last_mov = movement
        
        self.pos[0] += frame_movement[0] 
        entity_rect = self.rect()
        #handle the collisions on the x axis
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right 
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        if frame_movement[0] > 0:
            self.flip = False
        if frame_movement[0] < 0:
            self.flip = True
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        #handle the collisions on the y axis
        for rect in list(tilemap.physics_rects_around((self.pos[0],self.pos[1] + self.d))):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top 
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        for rect in list(tilemap.physics_rects_around((self.pos[0],self.pos[1] - self.d))):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top 
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y


        self.velocity[1] = min(5, self.velocity[1] + 0.2)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            self.air_time = 0
        else:
            self.air_time += 1


    def render(self, surf, offset = (0,0)):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

