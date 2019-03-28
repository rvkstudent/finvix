import tkinter
from datetime import datetime, timedelta
import dateutil.relativedelta
#d2 = datetime.now() - dateutil.relativedelta.relativedelta(months=1)

master = tkinter.Tk()
canv_height = 300
canv_width = 800
x_period = 5
candles_in_period = 6

#<DATETIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>

ohlc =[
["20190319 100000", 206.40, 206.70, 205.93, 206.38, 7052240],
["20190319 110000", 206.36, 207.41, 206.30, 207.22, 8528020],
["20190319 120000", 207.22, 207.30, 206.78, 207.00, 4468400],
["20190319 130000", 207.02, 207.45, 206.91, 207.30, 3210360],
["20190319 140000", 207.26, 208.00, 207.23, 207.84, 7292400],
["20190319 150000", 207.86, 208.31, 207.71, 208.01, 3895920],
["20190319 160000", 208.05, 208.08, 206.95, 207.41, 5095890],
["20190319 170000", 207.36, 207.65, 207.04, 207.41, 3215010],
["20190319 180000", 207.42, 207.70, 206.87, 207.70, 4947180],
["20190319 150000", 207.86, 208.31, 207.71, 208.01, 3895920],
["20190319 160000", 208.05, 208.08, 206.95, 207.41, 5095890],
["20190319 170000", 207.36, 207.65, 207.04, 207.41, 3215010]
]

grip_padding_top = 20
grip_padding_bottom = 20
grip_padding_right = 50
grip_padding_left = 50

y_max = 215
y_min = 205

def get_extrem(ohlc):
    maximum = 0
    minimum = 10**6
    for elem in ohlc:
        if (elem[2] > maximum):
            maximum = elem[2]
        if (elem[3] < minimum):
            minimum = elem[3]
    return [maximum, minimum]

def get_ypoint(value, max, min, c_height):
    price_in_pixel =  (max - min) / c_height
    y = ( value - min ) / price_in_pixel
    return c_height - y + 20

price_coridor = get_extrem(ohlc)[0] - get_extrem(ohlc)[1]

canvas = tkinter.Canvas(master, bg='white', height=canv_height, width=canv_width)



area_pixels =  canv_height - grip_padding_bottom - grip_padding_top

#  atr расчитать

atr = 20

pixels_in_price_step = area_pixels / atr

def put_candle(x, open, high, low, close):
    python_green = "#476042"




    low_y = get_ypoint(low, y_max, y_min, canv_height - 40 )

    high_y = get_ypoint(high, y_max, y_min, canv_height - 40 )

    open_y = get_ypoint(open, y_max, y_min, canv_height - 40)

    close_y = get_ypoint(close, y_max, y_min, canv_height - 40)

     # линия свечи


    if (open > close):
        canvas.create_line(x, low_y, x, close_y, fill='#660000')
        canvas.create_line(x, open_y, x, high_y, fill='#660000')

        canvas.create_rectangle(x - 1, open_y, x + 1, close_y,
                                outline="#660000", fill="#FF3333", width=1)
    if (close > open):
        canvas.create_line(x, low_y, x, close_y, fill='#193300')
        canvas.create_line(x, open_y, x, high_y, fill='#193300')
        canvas.create_rectangle(x - 1, open_y, x + 1, close_y,
                                outline="#193300", fill="#00FF00", width=1)
#


    # тело свечи


print (pixels_in_price_step)

canvas.create_line(grip_padding_left, grip_padding_top, grip_padding_left, canv_height-grip_padding_top, dash=(4, 2), fill='#A8A8A8')
canvas.create_line(grip_padding_left, grip_padding_top, canv_width-grip_padding_right, grip_padding_top, dash=(4, 2), fill='#A8A8A8')
canvas.create_line(canv_width-grip_padding_right, grip_padding_top, canv_width-grip_padding_right, canv_height-grip_padding_bottom, dash=(4, 2), fill='#A8A8A8')
canvas.create_line(grip_padding_left, canv_height-grip_padding_bottom, canv_width-grip_padding_right, canv_height-grip_padding_bottom, dash=(4, 2), fill='#A8A8A8')

period = 5
candles_per_hour = 60 / period

for i in range (y_min, y_max, 1):
    y0 = i
    low_y = get_ypoint(y0, y_max, y_min, canv_height - 40)
    print (low_y)
    canvas.create_line(grip_padding_left, low_y, canv_width-grip_padding_right,low_y,
                       dash=(4, 2), fill='#A8A8A8')
    canvas.create_text(canv_width-grip_padding_right + 20, low_y - 5, text=i, fill="grey")

d2 = datetime.strptime("09:00","%H:%M")

for i in range (0, 15, 1):

    d2 = d2 + timedelta(minutes=60)
    print (d2)

    x0 = grip_padding_left + 4*candles_per_hour*i
    canvas.create_line(x0, grip_padding_top, x0, canv_height - grip_padding_top,
                       dash=(4, 2), fill='#A8A8A8')
    canvas.create_text(x0 + 20, canv_height - grip_padding_top + 10, text=d2.time().strftime("%H:%M"), fill="grey")

step = int((canv_width- grip_padding_right - grip_padding_left) / 9)
x0 = grip_padding_left+4

for elem in ohlc:


    put_candle(x0, elem [1], elem [2], elem [3], elem [4])

    x0 = x0 + 4




canvas.pack()
master.mainloop()



def cluster2(hour, minute, period):

    minute_time = hour*60 + minute - 600

    period_hour = minute_time // period * period // 60

    print(period_hour+10)

    period_minute = minute_time // period * period - period_hour*60

    print(period_minute)

cluster2(23, 59, 1)

