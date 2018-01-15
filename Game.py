import tkinter
import image
import config
import random
import time

snake = list() # 蛇列表(包括蛇头和蛇身)

head = dict({'X' : config.HEAD_X, 'Y' : config.HEAD_Y, 'DIRECTION' : config.HEAD_DIRECTION, 'tag' : None}) # 蛇头字典，head['X']为蛇头X位置，head['Y']为蛇头Y位置，head['DIRECTION']为蛇头的方向，以下出现的蛇身体类同
# 将蛇头加入蛇列表
snake.append(head)
# 定义游戏状态
game_state = config.GAME_START
# 创建窗体
game_window = tkinter.Tk()
# 窗体标题设置
game_window.title("贪吃蛇")
# 窗体位置和大小设置
screenwidth = game_window.winfo_screenwidth()
screenheight = game_window.winfo_screenheight()
size = '%dx%d+%d+%d' % (config.GAME_WIDTH, config.GAME_HEIGHT, (screenwidth - config.GAME_WIDTH) / 2, (screenheight - config.GAME_HEIGHT) / 2)
game_window.geometry(size)
# 加载所有图片
back_image = dict({0: None,1: None}) # 创建字典保存两张背景构造图
head_image = dict({config.NORTH: None, config.SOUTH: None, config.WEST: None, config.EAST: None}) # 创建字典保存蛇头的四个方向图
body_image = dict({config.NORTH: None, config.SOUTH: None, config.WEST: None, config.EAST: None}) # 创建字典保存蛇身的四个方向图
back_image[0], back_image[1], fruit_image, \
    head_image[config.NORTH], head_image[config.SOUTH], head_image[config.WEST], head_image[config.EAST], \
        body_image[config.NORTH], body_image[config.SOUTH], body_image[config.WEST], body_image[config.EAST], \
            = image.load_image(tkinter)
start_image, stop_image = image.load_state_image(tkinter)
# 获取画布
window_canvas = tkinter.Canvas(game_window)
# 画布包装方式
window_canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
        

# 随机生成果实的方法
def random_fruit():
    exist_Rs_or_Cs = list()
    R_OR_C = random.randint(0, 1)
    if R_OR_C:
        for hb in snake:
            exist_Rs_or_Cs.append(hb['Y'] / 20)
        fruit_ROW = random.randint(0, config.GAME_ROW_NUM - 1)
        while fruit_ROW in exist_Rs_or_Cs:
            fruit_ROW = random.randint(0, config.GAME_ROW_NUM - 1)
        return \
            dict({'X': random.randint(0, config.GAME_COLUMN_NUM-1)*20, 'Y': fruit_ROW * 20})
    else:
        for hb in snake:
            exist_Rs_or_Cs.append(hb['X'] / 20)
        fruit_COLUMN = random.randint(0, config.GAME_COLUMN_NUM - 1)
        while fruit_COLUMN in exist_Rs_or_Cs:
            fruit_COLUMN = random.randint(0, config.GAME_COLUMN_NUM - 1)
        return \
            dict({'X': fruit_COLUMN * 20, 'Y': random.randint(0, config.GAME_ROW_NUM-1)*20})

# 检测是否吃到了果实的方法
def is_atefruit(fruit):
    if head['X'] == fruit['X'] and head['Y'] == fruit['Y']:
        return True
    else:
        return False

# 创建以蛇头为准对齐的方法
def head_align():
    if len(snake) == 1:
        return snake
    else:
        i = 1
        while i < len(snake):
            snake[i]['DIRECTION'] = \
                (config.NORTH if snake[i - 1]['Y'] < snake[i]['Y'] else config.SOUTH) \
                    if snake[i - 1]['X'] == snake[i]['X'] else \
                    (config.WEST if snake[i - 1]['X'] > snake[i]['Y'] else config.EAST)
            i += 1


# 蛇吃到果实，蛇的长度增加一的方法，顺便再生产果实
def action_atefruit():
    window_canvas.delete("fruit_image")
    X = snake[-1]['X'] if snake[-1]['DIRECTION'] == config.NORTH or snake[-1]['DIRECTION'] == config.SOUTH else \
        (snake[-1]['X'] + 20 if snake[-1]['DIRECTION'] == config.WEST else snake[-1]['X'] - 20)
    Y = snake[-1]['Y'] if snake[-1]['DIRECTION'] == config.WEST or snake[-1]['DIRECTION'] == config.EAST else \
        (snake[-1]['Y'] + 20 if snake[-1]['DIRECTION'] == config.NORTH else snake[-1]['Y'] - 20)
    body = dict({'X': X, 'Y': Y, 'DIRECTION': None, 'tag': "None"})
    snake.append(body)
    head_align()
    snake[-1]['tag'] = "body_image_%d%04d"%(snake[-1]['DIRECTION'],len(snake))
    window_canvas.create_image(snake[-1]['X'], snake[-1]['Y'], anchor = tkinter.NW, image = body_image[snake[-1]['DIRECTION']], tag = snake[-1]['tag'])
    fruit = random_fruit()
    window_canvas.create_image(fruit['X'], fruit['Y'], anchor=tkinter.NW, image=fruit_image, tag="fruit_image")
    return fruit


# 蛇前进一步的方法
def step():
    global old_head_direction
    X = head['X']
    Y = head['Y']
    DIRECTION = head['DIRECTION']
    if DIRECTION == config.NORTH:
        head['Y'] -= config.STEP_NUM
    elif DIRECTION == config.SOUTH:
        head['Y'] += config.STEP_NUM
    elif DIRECTION == config.WEST:
        head['X'] -= config.STEP_NUM
    else:
        head['X'] += config.STEP_NUM
    window_canvas.delete("head_image_%d" % (old_head_direction))
    old_head_direction = DIRECTION
    head['tag'] = "head_image_%d" % (DIRECTION)
    window_canvas.create_image(head['X'], head['Y'], anchor=tkinter.NW, image=head_image[DIRECTION],
                            tag = head['tag'])
    if len(snake) > 1:
        window_canvas.delete(snake[-1]['tag'])      
        snake[-1]['X'] = X
        snake[-1]['Y'] = Y
        snake[1:1] = [snake.pop(-1)]
        head_align()
        window_canvas.create_image(snake[1]['X'], snake[1]['Y'], anchor=tkinter.NW, image=body_image[snake[1]['DIRECTION']], tag = snake[1]['tag'] )
    return old_head_direction
# 检测是否蛇头越界的方法
def isout_of_bounds():
    if head['X'] < 0 or head['Y'] < 0 \
            or head['X'] > config.GAME_WIDTH - 20 \
            or head['Y'] > config.GAME_HEIGHT - 20:
        return True
    else:
        return False
# 检测蛇头是否与蛇身发生碰撞
def isbomb():
    i = 1
    while i < len(snake):
        if snake[i]['X'] == head['X'] and snake[i]['Y'] == head['Y']:
            return True
        i += 1
    else:
        return False


# 监听键盘控制方向
def key_control_direction(event):
    if event.char == 'w':
        if head['DIRECTION'] != config.SOUTH and head['DIRECTION'] != config.NORTH:
            head['DIRECTION'] = config.NORTH
    elif event.char == 's':
        if head['DIRECTION'] != config.SOUTH and head['DIRECTION'] != config.NORTH:
            head['DIRECTION'] = config.SOUTH
    elif event.char == 'a':
        if head['DIRECTION'] != config.EAST and head['DIRECTION'] != config.WEST:
            head['DIRECTION'] = config.WEST
    elif event.char == 'd':
        if head['DIRECTION'] != config.EAST and head['DIRECTION'] != config.WEST:
            head['DIRECTION'] = config.EAST



# 左上角画出蛇的长度的标识的方法
def draw_action():
    window_canvas.delete("LENGHT")
    window_canvas.create_text(10,10,text="长度：%d"%(len(snake)),anchor=tkinter.NW,fill="red",font="time 24 bold",tag="LENGHT")

# 鼠标点击事件
def call_back_click(event):
    global game_state
    # 如果游戏状态为启动状态，则修改状态为运行
    # 如果游戏状态为结束状态，则修改状态为启动状态
    if game_state == config.GAME_START:
        game_state = config.GAME_RUNNING
        global snake
        global head
        snake = list() # 蛇列表(包括蛇头和蛇身)

        head = dict({'X' : config.HEAD_X, 'Y' : config.HEAD_Y, 'DIRECTION' : config.HEAD_DIRECTION, 'tag' : None}) # 蛇头字典，head['X']为蛇头X位置，head['Y']为蛇头Y位置，head['DIRECTION']为蛇头的方向，以下出现的蛇身体类同
        # 将蛇头加入蛇列表
        snake.append(head)

        # 删除启动图片
        window_canvas.delete("START")
        
    elif game_state == config.GAME_STOP:
        window_canvas.delete("OVER")

        game_state = config.GAME_START
        game_start()


# 游戏结束
def game_over():
    global game_state
    game_state = config.GAME_STOP
    for x in snake:
        window_canvas.delete(x['tag'])
    snake.clear()
    window_canvas.delete('LENGHT')
    window_canvas.delete('START')
    window_canvas.create_image(100,50,anchor=tkinter.NW,image=stop_image,tag="OVER")
    for r in range(config.GAME_ROW_NUM):
        for c in range(config.GAME_COLUMN_NUM):
            window_canvas.delete("back_image_%d" % (r * 100 + c))



# 游戏开始
def game_start():
    global window_canvas
    global fruit
    # 背景画背景
    # 根据蛇列表显示游戏背景画面的方法
    for r in range(config.GAME_ROW_NUM):
        for c in range(config.GAME_COLUMN_NUM):
            window_canvas.create_image(c * 20, r * 20, anchor=tkinter.NW, image=back_image[(r + c) % 2],
                                       tag="back_image_%d" % (r * 100 + c))
    head['tag'] = "head_image_%d" % (head['DIRECTION'])
    window_canvas.create_image(head['X'], head['Y'], anchor=tkinter.NW, image=head_image[head['DIRECTION']], tag = head['tag'])

    # 长度
    window_canvas.create_text(10, 10, text="长度：%d" % (len(snake)), anchor=tkinter.NW, fill="red",
                                  font="time 24 bold", tag="LENGHT")    
    fruit = random_fruit()
    window_canvas.create_image(fruit['X'], fruit['Y'], anchor=tkinter.NW, image=fruit_image, tag="fruit_image")
    window_canvas.create_image(100, 50, anchor=tkinter.NW, image=start_image, tag="START")    
def game():
    global fruit
    global old_head_direction
    if game_state == config.GAME_START:
        
        # 鼠标监听
        window_canvas.bind("<Button-1>", call_back_click)
        window_canvas.bind("<Key>", key_control_direction)
        window_canvas.focus_set()
        old_head_direction = head['DIRECTION']
        control_count = 0
        
        game_start()

    while True:
        if game_state == config.GAME_RUNNING:
            window_canvas.delete('START')
            control_count += 1
            if control_count >= 50 - len(snake):
                control_count = 0
                old_head_direction = step()

                # 检测碰撞
                if isbomb() or isout_of_bounds():
                    game_over()
                if is_atefruit(fruit):
                    fruit = action_atefruit()
                    draw_action()
            # 更新显示
        game_window.update()
        # 休眠10ms
        time.sleep(0.002)



if __name__ == "__main__":
    game()
    game_window.mainloop()
