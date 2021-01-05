import base64
with open("ticket.png", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)
print("#" * 100)
print(my_string.decode('utf-8'))