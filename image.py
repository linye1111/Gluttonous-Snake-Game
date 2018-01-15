# 加载图片的模块内方法
def load_image(tkinter):
    return \
        tkinter.PhotoImage(file="../image/background0.gif"), \
        tkinter.PhotoImage(file="../image/background1.gif"), \
        tkinter.PhotoImage(file="../image/fruit.gif"), \
        tkinter.PhotoImage(file="../image/head_N.gif"), \
        tkinter.PhotoImage(file="../image/head_S.gif"), \
        tkinter.PhotoImage(file="../image/head_W.gif"), \
        tkinter.PhotoImage(file="../image/head_E.gif"), \
        tkinter.PhotoImage(file="../image/body_N.gif"), \
        tkinter.PhotoImage(file="../image/body_S.gif"), \
        tkinter.PhotoImage(file="../image/body_W.gif"), \
        tkinter.PhotoImage(file="../image/body_E.gif") \

def load_state_image(tkinter):
    return \
        tkinter.PhotoImage(file="../image/start.gif"), \
        tkinter.PhotoImage(file="../image/over.gif")
