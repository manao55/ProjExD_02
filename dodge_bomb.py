import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，爆弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向，縦方向の判定結果タプル（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    # こうかとんSurface（kk_img）からこうかとんRect（kk_rct）を抽出する
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))  # 練習１
    bd_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # 爆弾Surface（bd_img）から爆弾Rect（bd_rct）を抽出する
    bd_rct = bd_img.get_rect()
    # 爆弾Rectの中心座標を乱数で指定する
    bd_rct.center = x, y 
    vx, vy = +5, +5  # 練習２
    kk_zis = {  # 辞書作成
        (5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (5,-5):pg.transform.rotozoom(kk_img, 315, 1.0),
        (0,-5):pg.transform.rotozoom(kk_img, 270, 1.0),
        (-5,-5):pg.transform.rotozoom(kk_img, 315, 1.0),
        (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5,5):pg.transform.rotozoom(kk_img, 45, 1.0),
        (0,5):pg.transform.rotozoom(kk_img, 90, 1.0),
        (5,5):pg.transform.rotozoom(kk_img, 45, 1.0)
    }

    clock = pg.time.Clock()
    tmr = 0
    ###
    bd_size = 20  # 爆弾の初期サイズ
    bd_expand = True  # 爆弾の拡大フラグ
    ###
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bd_rct):  # 練習５
            print("ゲームオーバー")
            return   # ゲームオーバー 
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        if(sum_mv[0] >= 5):
            kk_img = pg.transform.flip(kk_img, False, True)
        if sum_mv != [0, 0]:
            kk_img = kk_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                kk_img = pg.transform.flip(kk_img, True, False)

        
        """
        試行錯誤の足跡
        """
        # angle = 0
        # if sum_mv[0] < 0:  # 左方向への移動
        #     angle = 90
        # elif sum_mv[0] > 0:  # 右方向への移動
        #     angle = 270
        # elif sum_mv[1] < 0:  # 上方向への移動
        #     angle = 0
        # elif sum_mv[1] > 0:  # 下方向への移動
        #     angle = 180
 
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)  # 練習２
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向に画面外だったら
            vx *= -1
        if not tate:  # 縦方向に範囲外だったら
            vy *= -1
        if bd_expand:
            bd_size += 1  # サイズを1増やす
            if bd_size >= 500:  # 最大サイズに達したら
                bd_expand = False
        # else:
        #     bd_size -= 1  # サイズを1減らす
        #     if bd_size <= 20:  # 最小サイズに達したら
        #         bd_expand = True
        bd_img = pg.Surface((bd_size, bd_size))  # 爆弾のサイズを変更
        bd_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
        pg.draw.circle(bd_img, (255, 0, 0), (bd_size // 2, bd_size // 2), bd_size // 2)
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
