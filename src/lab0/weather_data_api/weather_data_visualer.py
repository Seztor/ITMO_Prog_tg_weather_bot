def get_visual_data_current_weather(data: dict, temp_type: str):
    print(data)
    for i in data:
        if type(i) == type(list()):
            for j in i[0]:
                print(i[0][j], end=' ')
            print()
        elif type(i) == type(dict()):
            for j in i:
                print(i[j], end=' ')
            print()
        elif type(i) == type(str()):
            print(i)


# def convert_temp(temp_amount: int):
#     current_temp_type =
#     if
#         temp_str = ''
