import datetime

x = []
with open("dates.txt", "r") as file:
    for line in file:
        a = line
        a = a.strip()[27:37]
        if len(a) == 0:
            continue
        x.append(a)
new_file = open("valid_dates.txt", "w")
for date in x:
    o_d = date
    date = date.split("/")
    d = int(date[0])
    m = int(date[1])
    y = int(date[2])
    dt = datetime.date(y, m, d)
    if dt.weekday() == 6:
        new_file.write(o_d + "\n")
