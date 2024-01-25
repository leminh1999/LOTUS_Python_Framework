scheduleList=[{"id":1,"name":"AAA","time":"2019-01-01 00:00:00","status":5},
              {"id":2,"name":"AAA","time":"2019-01-01 00:00:00","status":1},
              {"id":3,"name":"BBB","time":"2019-01-01 00:00:00","status":1},
              {"id":4,"name":"BBB","time":"2019-01-01 00:00:00","status":1},
              {"id":5,"name":"BBB","time":"2019-01-01 00:00:00","status":1}]


#Remove all "AAA" in scheduleList
scheduleList = [x for x in scheduleList if x["name"] != "AAA"]
print(scheduleList)

