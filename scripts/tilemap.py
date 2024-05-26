import pygame
import json
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

AutoTileMap = {
    
    tuple(sorted([(1,0),(0,1)])):0,
    tuple(sorted([(1,0),(0,1),(1,1)])):0,
    tuple(sorted([(1,0),(0,1),(1,1),(-1,-1)])):0,
    tuple(sorted([(1,0),(0,1),(1,1),(-1,1)])):0,
    tuple(sorted([(1,0),(1,1),(1,-1),(0,1)])):0,
    tuple(sorted([(1,0),(1,1),(1,-1),(0,1),(-1,1)])):0,
    tuple(sorted([(1,0),(0,1),(1,1),(-1,-1),(1,-1)])):0,
    tuple(sorted([(1,0),(0,1),(-1,0)])):1,
    tuple(sorted([(1,0),(0,1),(-1,0),(-1,1)])):1,
    tuple(sorted([(1,0),(0,1),(-1,0),(-1,1),(1,1)])):1, 
    tuple(sorted([(-1,-1),(0,1),(-1,0),(-1,1),(1,1),(1,0)])):1, 
    tuple(sorted([(1,0),(0,1),(-1,0),(-1,1),(1,1),(-1,1)])):1,    
    tuple(sorted([(1,0),(0,1),(-1,0),(-1,1),(1,1),(-1,1),(-1,-1)])):1,    
    tuple(sorted([(1,0),(-1,0),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)])):1,
    tuple(sorted([(1,0),(-1,0),(0,1),(-1,-1),(1,-1),(1,1),(-1,1)])):1,
    tuple(sorted([(1,0),(-1,0),(0,1),(1,-1),(1,1),(-1,1)])):1,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(1,-1),(1,1),(-1,1)])):1,
    tuple(sorted([(-1,0),(0,1)])):2,
    tuple(sorted([(-1,0),(0,1),(-1,1)])):2,
    tuple(sorted([(-1,0),(0,1),(-1,1),(-1,-1)])):2,
    tuple(sorted([(-1,0),(0,1),(-1,1),(-1,-1),(1,1)])):2,
    tuple(sorted([(-1,0),(0,1),(-1,1),(1,1)])):2,
    tuple(sorted([(-1,0),(0,-1),(0,1)])):3,
    tuple(sorted([(-1,0),(0,-1),(0,1),(-1,-1)])):3,
    tuple(sorted([(-1,0),(0,-1),(0,1),(-1,-1),(-1,1)])):3,
    tuple(sorted([(-1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,1)])):3,
    tuple(sorted([(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)])):3,
    tuple(sorted([(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)])):3,
    tuple(sorted([(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1)])):3,
    tuple(sorted([(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(-1,1)])):3,
    tuple(sorted([(-1,0),(0,-1)])):4,
    tuple(sorted([(-1,0),(0,-1),(-1,-1)])):4,
    tuple(sorted([(-1,0),(0,-1),(-1,-1),(-1,1)])):4,
    tuple(sorted([(-1,0),(0,-1),(-1,-1),(1,-1)])):4,
    tuple(sorted([(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)])):4,
    tuple(sorted([(1,0),(0,-1)])):6,
    tuple(sorted([(1,0),(0,-1),(1,-1)])):6,
    tuple(sorted([(1,0),(0,-1),(1,-1),(1,1)])):6,
    tuple(sorted([(1,0),(0,-1),(1,-1),(-1,-1)])):6,
    tuple(sorted([(1,0),(0,-1),(1,-1),(-1,-1),(1,1)])):6,
    tuple(sorted([(1,0),(0,1),(0,-1)])):7,
    tuple(sorted([(1,0),(0,1),(0,-1),(1,-1)])):7,
    tuple(sorted([(1,0),(0,1),(0,-1),(1,-1),(1,1)])):7,
    tuple(sorted([(1,0),(0,1),(0,-1),(1,-1),(1,1),(-1,-1)])):7,
    tuple(sorted([(1,0),(0,1),(0,-1),(1,-1),(1,1),(-1,1)])):7,
    tuple(sorted([(1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)])):7,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)])):8,
    tuple(sorted([(-1,0),(0,-1),(1,0)])):9, 
    tuple(sorted([(-1,0),(0,-1),(1,0),(-1,-1)])):9, 
    tuple(sorted([(-1,0),(0,-1),(1,0),(-1,-1),(1,-1)])):9, 
    tuple(sorted([(-1,0),(0,-1),(1,0),(-1,-1),(1,-1),(1,1)])):9, 
    tuple(sorted([(1,0),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)])):9,
    tuple(sorted([(1,0),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1),(1,1)])):9,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1)])):10,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(1,-1),(1,1),(-1,1)])):11,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(-1,1)])):12,
    tuple(sorted([(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1)])):13,
}
constant = 3
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'],tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'],tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        return matches
    
    def solid_check(self, loc):
        tile_loc = str(int(loc[0]//self.tile_size)) + ';' + str(int(loc[1]//self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surf, offset = (0,0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]-offset[0], tile['pos'][1]-offset[1]))

        for x in range(offset[0]//self.tile_size, (offset[0] + surf.get_width())//self.tile_size + 1):
            for y in range(offset[1]//self.tile_size, (offset[1] + surf.get_height())//self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][self.tilemap[loc]['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def load(self,path):
        f = open(path, 'r')
        data = json.load(f)
        self.loaddata(data)

        f.close()
    
    def loaddata(self,data):
        self.tilemap = data['tilemap']
        self.tile_size = data['tile_size'] 
        self.offgrid_tiles = data['offgrid']

    def export(self, path):
        f = open(path +'.json', 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles},fp=f)
        f.close()

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in sorted([(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,-1),(1,1),(-1,1)]):
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in PHYSICS_TILES) and (neighbors in AutoTileMap):
                tile['variant'] = AutoTileMap[neighbors]
