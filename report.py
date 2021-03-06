import pandas as pd
from xlrd import open_workbook

def find_table(filenames, header, end_phrase, columns, type):

    trades = list()

    for filename in filenames:
        wb = open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        index = 0
        for row in range(sheet.nrows):
            index += 1
            if (header in str(sheet.cell(row, 0).value)):
                begin = index
            if (end_phrase in str(sheet.cell(row, 0).value)):
                end = index
                break

        column_index = {}
        index = 0

        for col in range(sheet.ncols):
            for column in columns:
                value = " ".join(sheet.cell(begin, col).value.splitlines())
                #print(column)
                if (columns[column] in value):
                    column_index[column] = index
            index += 1

        #print(column_index)

        if (type == "FUT"):
            sec_index = 0
            offset = 2
            end = end - 5

        if (type == "FUND"):
            sec_index = 1
            offset = 1

        for i in range(begin, end, 1):

            if ("ИТОГО" not in sheet.cell(i + offset, sec_index).value and sheet.cell(i + offset, sec_index).value != ''):
                sec_code = sheet.cell(i + offset, sec_index).value

                order_num = sheet.cell(i + offset, column_index['Номер заявки']).value
                trade_num = sheet.cell(i + offset, column_index['Номер сделки']).value
                trade_date = sheet.cell(i + offset, column_index['Дата заключения']).value
                trade_time = sheet.cell(i + offset, column_index['Время заключения']).value
                buy_qty = sheet.cell(i+ offset, column_index['Куплено']).value
                sold_qty = sheet.cell(i+ offset, column_index['Продано']).value
                price = sheet.cell(i+ offset, column_index['Цена сделки']).value
                if (type == "FUT"):
                    comis = float(sheet.cell(i+ offset, column_index['Комиссия']).value) + float(sheet.cell(i+ offset, column_index['Комиссия2']).value)
                if (type == "FUND"):
                    comis = float(sheet.cell(i + offset, column_index['Комиссия']).value)
                nkd = ''
                if 'НКД' in column_index:
                    nkd = sheet.cell(i+ offset, column_index['НКД']).value
                if (buy_qty == ''):
                    trade_type = "S"
                    qty = sold_qty
                else:
                    trade_type = "B"
                    qty = buy_qty

                trades.append(
                        {'SEC_CODE': sec_code, 'Направление сделки': trade_type, 'Номер заявки': order_num,
                         'Номер сделки': trade_num, 'Дата заключения': trade_date, 'Время заключения': trade_time,
                         'Количество': qty, 'Цена сделки': price, 'НКД': nkd, 'Комиссия': comis})

    #print(trades)

    long_position_volume = {}
    short_position_volume = {}

    sum_nkd = {}
    sum_qty = {}
    average_buy = {}
    average_sell = {}
    sum_profit = {}
    #trades = trades[0:3]
    for trade in trades:

        #print(trade)

        sec_code = trade['SEC_CODE']
        trade_type = trade['Направление сделки']
        trade_num = int(trade['Номер сделки'])
        nkd = trade['НКД']
        qty = float(trade['Количество'])

        price = float(trade['Цена сделки'])
        comis = float(trade['Комиссия'])
        if sec_code not in sum_qty:
            sum_qty[sec_code] = 0
            long_position_volume[sec_code] = 0
            short_position_volume[sec_code] = 0
            average_buy[sec_code] = 0
            average_sell[sec_code] = 0
            sum_profit[sec_code] = 0
            sum_nkd[sec_code] = 0



        if trade_type == "B":

            if long_position_volume[sec_code] >= 0 and short_position_volume[sec_code] == 0:

                sum_qty[sec_code] = sum_qty[sec_code] + qty

                if nkd == '':
                    long_position_volume[sec_code] = long_position_volume[sec_code] + qty * price
                    average_buy[sec_code] = long_position_volume[sec_code] / sum_qty[sec_code]
                else:
                    sum_nkd[sec_code] = sum_nkd[sec_code] + nkd
                    long_position_volume[sec_code] = long_position_volume[sec_code] + 10*price*qty #+ nkd
                    average_buy[sec_code] = long_position_volume[sec_code] / sum_qty[sec_code] / 10



            if short_position_volume[sec_code] > 0:

                if qty <= sum_qty[sec_code]:

                    if (nkd == ''):

                        sum_profit[sec_code] = sum_profit[sec_code] + (average_sell[sec_code] - price) * qty - comis * 2
                        short_position_volume[sec_code] = short_position_volume[sec_code] - qty * average_sell[sec_code]
                        # print("{} Профит {} = {}, Итого = {}".format(trade_num, sec_code, (average_sell[sec_code] - price) * qty, sum_profit[sec_code]))
                    else:
                        print("Шорт по облигации???")

                    # print("Профит {} = {}, Итого = {}".format(sec_code, (average_sell[sec_code] - price) * qty - comis * 2, sum_profit[sec_code]))


                    sum_qty[sec_code] = sum_qty[sec_code] - qty

                    if sum_qty[sec_code] > 0:
                        average_sell[sec_code] = short_position_volume[sec_code] / sum_qty[sec_code]
                    if sum_qty[sec_code] == 0:
                        average_sell[sec_code] = 0

                elif qty > sum_qty[sec_code]:

                    if (nkd == ''):
                        sum_profit[sec_code] = sum_profit[sec_code] + (average_sell[sec_code] - price) * sum_qty[sec_code] - comis * 2
                        # print("{} Профит {} = {}, Итого = {}".format(trade_num, sec_code, (average_sell[sec_code] - price) * sum_qty[sec_code],
                        #                                          sum_profit[sec_code]))
                    else:
                        pass
                    # print(
                    #     "Профит {} = {}, Итого = {}".format(sec_code, (average_sell[sec_code] - price) * sum_qty[sec_code] - comis * 2,
                    #                                       sum_profit[sec_code]))

                    short_position_volume[sec_code] = 0
                    sum_qty[sec_code] = qty - sum_qty[sec_code]


                    if nkd == '':
                        long_position_volume[sec_code] = long_position_volume[sec_code] + sum_qty[sec_code] * price - comis*2
                    else:
                        long_position_volume[sec_code] = long_position_volume[sec_code] + nkd - (
                                    1000 - 1000 * price / 100) * sum_qty[sec_code] + sum_qty[sec_code] * 1000 - comis*2

                    if sum_qty[sec_code] > 0:
                        average_buy[sec_code] = long_position_volume[sec_code] / sum_qty[sec_code]
                    if sum_qty[sec_code] == 0:
                        average_buy[sec_code] = 0


        if trade_type == "S":

            if short_position_volume[sec_code] >= 0 and long_position_volume[sec_code] == 0:

                if nkd == '':
                    short_position_volume[sec_code] = short_position_volume[sec_code] + qty * price
                else:
                    print ("Шорт по облигации?????")

                sum_qty[sec_code] = sum_qty[sec_code] + qty
                average_sell[sec_code] = short_position_volume[sec_code] / sum_qty[sec_code]

            if long_position_volume[sec_code] > 0:

                if qty <= sum_qty[sec_code]:

                    sum_qty[sec_code] = sum_qty[sec_code] - qty

                    if (nkd == ''):
                        sum_profit[sec_code] = sum_profit[sec_code] + (price - average_buy[sec_code])*qty - comis*2
                        long_position_volume[sec_code] = long_position_volume[sec_code] - qty * average_buy[sec_code]
                        # print("{} Профит {} = {}, Итого = {}".format(trade_num, sec_code, (price - average_buy[sec_code])*qty, sum_profit[sec_code]))
                    else:
                        sum_nkd[sec_code] = sum_nkd[sec_code] - nkd
                        sum_profit[sec_code] = sum_profit[sec_code] + (price - average_buy[sec_code]) * qty * 10 - comis*2 #+ nkd
                        long_position_volume[sec_code] = long_position_volume[sec_code] - (qty * average_buy[sec_code] * 10)

                    if sum_qty[sec_code] == 0:
                        long_position_volume[sec_code] = 0
                        sum_profit[sec_code] = -sum_nkd[sec_code] + sum_profit[sec_code]


                elif qty > sum_qty[sec_code]:



                    if (nkd == ''):
                        sum_profit[sec_code] = sum_profit[sec_code] + (price - average_buy[sec_code]) * sum_qty[
                            sec_code] - comis * 2
                        # print("{} Профит {} = {}, Итого = {}".format(trade_num, sec_code, (price - average_buy[sec_code]) * sum_qty[
                        #      sec_code], sum_profit[sec_code]))
                    else:
                        print("Шорт по облигации?????")

                    # print("Профит {} = {}, Итого = {}".format(sec_code, (
                    #             (nkd - (1000 - 1000 * price / 100) * sum_qty[sec_code] + sum_qty[sec_code] * 1000) /
                    #             sum_qty[sec_code] - average_buy[sec_code]) * sum_qty[sec_code] - comis * 2, sum_profit[sec_code]))

                    sum_qty[sec_code] = qty - sum_qty[sec_code]
                    short_position_volume[sec_code] = short_position_volume[sec_code] + sum_qty[sec_code] * price
                    long_position_volume[sec_code] = 0

                    if sum_qty[sec_code] > 0:
                        average_sell[sec_code] = short_position_volume[sec_code] / sum_qty[sec_code]
                    else:
                        average_sell[sec_code] = 0


    #print(sum_profit)
    for i in sum_profit:
        sum_profit[i] = int(sum_profit[i])
    print(sum_profit)

    

    total = 0

    for elem in sum_profit:
        total = total + sum_profit[elem]

    print ("Total {}".format(total))

    print("\nОткрытые позиции: \n")

    for i in sum_qty:

        if (sum_qty[i] > 0):
            print("{} количество {} ср. цена {}".format(i, sum_qty[i], average_buy[i] + average_sell[i]))



end_phrase = "Итого - Комиссия Брокера"
header = "Заключенные в отчетном периоде сделки"

columns = {"Номер заявки" : "Номер заявки","Номер сделки" : "Номер сделки", "Дата заключения": "Дата заключения",
           "Время заключения": "Время заключения", "Куплено" : "Куплено", "Продано": "Продано", "Цена сделки": "Цена сделки",
           "Комиссия": "Комиссия", "НКД": "НКД"}

find_table(["C:\Reports\Broker_Report_42658_2016.xlsx","C:\Reports\Broker_Report_42658_EBS_2017.xlsx",
            "C:\Reports\Broker_Report_42658_EBS_2018.xlsx" ,"C:\Reports\Broker_Report_42658_EBS_2019.xlsx" ], header, end_phrase, columns, "FUND")


end_phrase = "TOTAL"
header = "Срочные сделки с производными финансовыми инструментами"

columns = {"Номер заявки" : "№ заявки","Номер сделки" : "Номер сделки", "Дата заключения": "Дата" , "Время заключения": "Время",
           "Куплено" : "Куплено", "Продано": "Продано", "Цена сделки": "Цена/премия,  руб.", "Комиссия": "Комиссия", "НКД": "НКД"}

find_table(["C:\Reports\Broker_Report_42658_2016.xlsx","C:\Reports\Broker_Report_42658_EBS_2017.xlsx",
            "C:\Reports\Broker_Report_42658_EBS_2018.xlsx" ,"C:\Reports\Broker_Report_42658_EBS_2019.xlsx" ], header, end_phrase, columns, "FUT")



# end_phrase = "TOTAL"
# header = "Срочные сделки с производными финансовыми инструментами"
#
# columns = {"Номер заявки" : "№ заявки","Номер сделки" : "Номер сделки", "Дата заключения": "Дата" , "Время заключения": "Время",
#            "Куплено" : "Куплено", "Продано": "Продано", "Цена сделки": "Цена/премия,  руб.", "Комиссия": "Комиссия", "НКД": "НКД"}
#
# find_table("C:\Reports\Broker_Report_42658_EBS_2019_3.xlsx", header, end_phrase, columns, "FUT")

