prices = [10,11,10,11,10,11,10,11,10,11]
last_price_pos = dict()
price_level_offcet = dict()

for i in range(len(prices)):
    cur_pos = i
    curr_price = prices[i]
    if(curr_price in last_price_pos):
        print("Previous = {}".format(last_price_pos[curr_price]))
        print("Current = {}".format(cur_pos))
        print(max(prices[last_price_pos[curr_price]:cur_pos]))
        if(curr_price in price_level_offcet):
            price_level_offcet[curr_price].append(1)
        else:
            price_level_offcet[curr_price] = []
    else:
        last_price_pos[curr_price] = cur_pos

print (price_level_offcet)
