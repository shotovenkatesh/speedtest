import tkinter
import requests
from tkinter import *

correct_words = 0
incorrect_words = 0
begin = True
times_up = False
game_over = False


def start_typing():
    global window
    window = tkinter.Tk()
    window.title("Speed Test")
    window.config(width=500, height=500, background="#222831", pady=100)

    def button_pressed():
        global game_over
        game_over = True

        if game_over:
            global correct_words
            global incorrect_words
            global begin
            global times_up
            window.destroy()
            correct_words = 1
            incorrect_words = 0
            begin = True
            times_up = False
            start_typing()

    response = requests.get("https://random-word-api.herokuapp.com//word?number=500")
    words_list = response.json()

    timer_label = Label(window, text="0")
    timer_label.config(font=("Courier", 40),foreground = "#F0A500",background = "#222831")
    timer_label.pack()

    text = Text(window, {"bg": "#222831", "bd": 150, "fg": "#00ADB5", "height": 2, "font": ("Courier New", 30),
                         "insertbackground": "#FF2E63", "wrap": "word","highlightthickness": 0})

    text.insert(INSERT, words_list)
    text.focus()
    text.mark_set("insert", "%d.%d" % (1.0, 0.0))
    text.pack()

    text.tag_add("start", "1.0", "5.0")
    #LIGHT BG AND FG
    text.tag_config("start", background="#393E46", foreground="#FFFFFF")

    def start_timer(count):
        global times_up
        global correct_words
        global incorrect_words
        if count >= 0:
            window.after(1000, start_timer, count - 1)
            timer_label.config(text=count)
        else:
            times_up = True
            timer_label.config(text="Times Up",padx = 20,pady = 20)
            text.config(state="disabled")
            text.destroy()
        if times_up:
            gross_wpm = correct_words / 5
            net_wpm = gross_wpm - incorrect_words
            accuracy = (net_wpm / gross_wpm) * 100

            if accuracy < 0  or net_wpm < 0:
                formatted_net_wpm = 0
                formatted_accuracy = 0
            else:
                formatted_net_wpm = '{0:.0f}'.format(net_wpm)
                formatted_accuracy = f"{'{0:.1f}'.format(accuracy)}%"

            speed_label = Label(text=f"wpm : {formatted_net_wpm} words", font=("Courier", 30), foreground = "#F0A500",background = "#222831",padx = 20,pady = 20)
            speed_label.pack()

            accuracy_label = Label(text=f"Accuracy : {formatted_accuracy} ", font=("Courier", 30), foreground = "#F0A500",background = "#222831",padx = 20,pady = 20)
            accuracy_label.pack()

            play_again = Button(text="Start Again", font=("Courier", 30),bg = "#F0A500",activebackground =  "#F0A500",padx = 20,pady = 20)
            play_again.config(foreground = "#F0A500",highlightthickness = 0, bd = 0,command=button_pressed)
            play_again.pack()

    def type_check(key):
        global begin
        global correct_words
        global incorrect_words
        if begin:
            start_timer(60)
        if text.get("insert") == key.char:
            correct_words += 1
            text.tag_config("start", foreground="#FFFFFF")
            # text.config(fg="blue")
            insert = text.index("insert")
            text.delete(insert)
        else:
            # text.config(fg="red")
            incorrect_words += 1
        begin = False

    text.bind("<Key>", type_check)


start_typing()

mainloop()
