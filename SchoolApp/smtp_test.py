import smtplib

email = "ktjljulie@gmail.com"
password = "gxfikmsjuwdfqjmd"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, password)

print("LOGIN SUCCESSFUL")

server.quit()