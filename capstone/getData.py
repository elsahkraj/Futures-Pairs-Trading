from localPath import base_dir
from xls_api import getDataFromXls
from csv_api import saveCSVFileToPath
import os
import datetime
from dateutil.parser import parse

# import data
data = getDataFromXls(os.path.join(base_dir, '艾佳-目标产品名单.xlsx'), startRow=0)

header = data[0]
content = data[1:]

# define target trading time in "openTime"
openTime = []
baseDay = parse(datetime.datetime.now().strftime('%Y-%m-%d'))
timeOne = baseDay + datetime.timedelta(hours=9, minutes=00)
timeTwo = baseDay + datetime.timedelta(hours=10, minutes=30)
timeThree = baseDay + datetime.timedelta(hours=13, minutes=30)
timeFour = baseDay + datetime.timedelta(hours=21, minutes=00)
openTime.append(timeOne)
openTime.append(timeTwo)
openTime.append(timeThree)
openTime.append(timeFour)

# logical statements
in_or_not = lambda x, interval: True if x >= interval[0] and x <= interval[1] else False
at_or_not = lambda x, timepoint: True if x == timepoint else False


new_content = []

# processing by line
for i in range(len(content)):

    currentRow = content[i]

    # processing current row

    # domestic and foreign trading time
    local_time = currentRow[4:8]
    foreign_time = currentRow[12:18]

    # conversion between data formats
    for j in range(len(local_time)-1, -1, -1):
        if len(local_time[j]) == 0:
            del local_time[j]
            continue

        t = local_time[j].split('-')

        # if time format is 9:00, then convert to 09:00
        start = t[0] if len(t[0]) == 4 else '0' + t[0]
        end = t[1] if len(t[0]) == 4 else '0' + t[0]

        # convert origin format to datetime format
        startTime = baseDay + datetime.timedelta(hours=int(start[:2]),
                                                minutes=int(start[2:]))
        endTime = baseDay + datetime.timedelta(hours=int(end[:2]),
                                                minutes=int(end[2:]))

        # if endTime is smaller, then add one day
        if endTime < startTime:
            endTime = endTime + datetime.timedelta(days=1)
        # redefine local time as an interval, convert 0900-1015 to [09:00, 10:15]
        local_time[j] = [startTime, endTime]

    for j in range(len(foreign_time)-1, -1, -1):
        if len(foreign_time[j]) == 0:
            del foreign_time[j]
            continue
        t = foreign_time[j].split('-')

        start = t[0] if len(t[0]) == 4 else '0' + t[0]
        end = t[1] if len(t[0]) == 4 else '0' + t[0]

        startTime = baseDay + datetime.timedelta(hours=int(start[:2]),
                                                minutes=int(start[2:]))
        endTime = baseDay + datetime.timedelta(hours=int(end[:2]),
                                                minutes=int(end[2:]))
        if endTime < startTime:
            endTime = endTime + datetime.timedelta(days=1)

        foreign_time[j] = [startTime, endTime]



    # for t in range(len(openTime)):
    #     for k in range(len(local_time)):
    #         if at_or_not(openTime[t], local_time[k][0]):
    #             count = 0
    #             for p in range(len(foreign_time)):
    #                 if in_or_not(openTime[t], foreign_time[p]):
    #                     count = count + 1
    #             if (count > 0):
    #                 currentRow.append(openTime[t].strftime('%H:%M'))
    #             else:
    #                 currentRow.append('None')

    for t in range(len(local_time)):
        for k in range(len(openTime)):
            if at_or_not(openTime[k], local_time[t][0]):
                count = 0
                for p in range(len(foreign_time)):
                    if in_or_not(openTime[k], foreign_time[p]):
                        count = count + 1
                if (count>0):
                    currentRow.append(openTime[k].strftime('%H:%M'))
                else:
                    currentRow.append('None')


    new_content.append(currentRow)
# define new headers
header = header + ['time_1', 'time_2', 'time_3', 'time_4']

# write back to file

saveCSVFileToPath(os.path.join(base_dir, 'newFile1.csv'),
                  header, new_content)
