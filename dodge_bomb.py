import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900

# 加速度のリスト
accs = [a for a in range(1, 11)]

move_key_dic = {
                pg.K_UP: (0, -5),
                pg.K_DOWN: (0, +5),
                pg.K_LEFT: (-5, 0),
                pg.K_RIGHT: (+5, 0),
}

def kk_direction():
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_trans_img = pg.transform.flip(kk_img, True, False)
    return {
        (0, 0): kk_img,
        (0, -5): pg.transform.rotozoom(kk_trans_img, 90, 1.0),
        (-5, 0): kk_img,
        (+5, 0): kk_trans_img,
        (+5, +5): pg.transform.rotozoom(kk_trans_img, -45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_trans_img, -90, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_trans_img, 45, 1.0)
    }

def check_bound(obj_domain: pg.Rect):
    """"
    引数：こうかとんRectか、ばくだんRect
    戻値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if (obj_domain.left < 0) or (WIDTH < obj_domain.right): # 横方向判定
        yoko = False
    if (obj_domain.top < 0) or (HEIGHT < obj_domain.bottom): # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    
    """"こうかとん"""

    kk_dir_dic = kk_direction()
    kk_img = kk_dir_dic[(0, 0)] # 初期画像
    
    
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
    accerator = 1.001 # 加速度
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
            
        if kk_domain.colliderect(bomb_domain):
            # screen.blit(pg.transform.rotozoom(kk_img, 0, 10.0), [800, 450])
            # pg.display.update()
            # count = tmr
            # while True:
            #     if count - tmr > 3:
            #         break
            #     tmr += 1
            #     clock.tick(100)
            print("ゲームオーバー")
            return
    
        screen.blit(bg_img, [0, 0])


        """"こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_move = [0, 0]
        
        # こうかとんをキーボード操作
        for key, move_tpl in move_key_dic.items():
            if key_lst[key]:
                sum_move[0] += move_tpl[0] # 横方向の合計移動量
                sum_move[1] += move_tpl[1] # 縦方向の合計移動量
        kk_img = kk_dir_dic[tuple(sum_move)]
                
        kk_domain.move_ip(sum_move[0], sum_move[1]) # 移動
        
        # はみだしを判定
        if check_bound(kk_domain) != (True, True):
            kk_domain.move_ip(-sum_move[0], -sum_move[1])
            
        # 移動後の座標に表示
        screen.blit(kk_img, kk_domain)
        
        """"ばくだん"""
        bomb_domain.move_ip(vx*accerator, vy*accerator) # 加速させている
        # bomb_domain.move_ip(vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]) # 爆弾の移動.時間ともに加速
        
        # はみだしを判定する.はみ出したら方向転換
        yoko, tate = check_bound(bomb_domain)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bomb_circle, bomb_domain) # rectを使って試しにblit
        
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()