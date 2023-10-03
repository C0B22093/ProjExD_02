import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900

move_key_dic = {
                pg.K_UP: (0, -5),
                pg.K_DOWN: (0, +5),
                pg.K_LEFT: (-5, 0),
                pg.K_RIGHT: (+5, 0),
}


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    
    """"こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_domain = kk_img.get_rect()
    kk_domain.center = (900, 400)
    
    """"ばくだん"""
    bomb_circle = pg.Surface((20, 20))
    pg.draw.circle(bomb_circle, (255, 0 ,0), (10,10), 10)
    bomb_circle.set_colorkey((0, 0, 0)) # 円の背景である黒い部分を透明にする
    
    bomb_domain = bomb_circle.get_rect() # surfaceからrect抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bomb_domain.center = (x, y) # rectにランダムな座標を設定する。
    vx, vy = +5, +5 # 爆弾の速度
    
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
    
        screen.blit(bg_img, [0, 0])
        # screen.blit(kk_img, [900, 400])
        
        # screen.blit(bomb_circle, [100, 100])
        """"こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_move = [0, 0]
        for key, move_tpl in move_key_dic.items():
            if key_lst[key]:
                sum_move[0] += move_tpl[0] # 横方向の合計移動量
                sum_move[1] += move_tpl[1] # 縦方向の合計移動量
        kk_domain.move_ip(sum_move[0], sum_move[1]) # 移動させる
        screen.blit(kk_img, kk_domain) # 移動後の座標に表示させる
        
        """"ばくだん"""
        bomb_domain.move_ip(vx, vy) # 爆弾の移動
        screen.blit(bomb_circle, bomb_domain) # rectを使って試しにblit
        
        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()