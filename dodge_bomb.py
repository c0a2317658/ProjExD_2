import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数: こうかとんRect or 爆弾のRect
    戻り値: 判定結果タプル（横方向、縦方向のはみ出し判定結果）
    （はみ出ていればFalse）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出たら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出たら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示し、5秒間待機する
    引数：画面Surface
    戻り値：なし
    """
    fr_img = pg.Surface((WIDTH, HEIGHT))  # 透明Surface
    fr_img.fill((0, 0, 0))  # 黒で塗りつぶし
    fr_img.set_alpha(200)
    screen.blit(fr_img, (0, 0))
    font = pg.font.Font(None, 50)
    txt = font.render("GAME OVER", True, (255, 255, 255))
    txt_rect = txt.get_rect()
    txt_rect.center = (WIDTH//2, HEIGHT//2)

    screen.blit(txt,txt_rect)
    kk2_img = pg.image.load("fig/8.png")
    kk2_rct = kk2_img.get_rect() 
    kk3_rct = kk2_img.get_rect()
    kk2_rct.center = WIDTH//2 +150, HEIGHT//2
    kk3_rct.center = WIDTH//2 -150, HEIGHT//2
    screen.blit(kk2_img, kk2_rct)
    screen.blit(kk2_img, kk3_rct)
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾画像リストと加速リストを作成
    引数：なし
    戻り値：爆弾画像リスト、加速リスト
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 空のSurface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い円を描く
        bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    bb_rct = bb_img.get_rect()
    bb_imgs,bb_accs = init_bb_imgs()  # 爆弾画像リストと加速リスト
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾の縦初期位置
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾の横初期位置
    vx = +5
    vy = +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なったら
              # ゲームオーバー関数呼び出し
            gameover(screen)
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量加算
                sum_mv[1] += mv[1] #縦方向の移動量加算
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,avy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1

        bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()