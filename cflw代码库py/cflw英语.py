ga月 = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
ga星期 = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def f月份(i):
    "一月 = 1"
    return ga月[i-1]
def f星期(i):
    "星期一 = 0"
    return ga星期[i]