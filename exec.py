#!/bin/python
#!-*- coding: utf-8 -*-

import sys
import time
import datetime
import subprocess

templates = [
    [ # h
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
    ],
    [ # e
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
    ],
    [ # l
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
    ],
    [ # l
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
    ],
    [ # o
        [1, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
    ],
    [ # 同时支持多列,这里本来想画个六芒星,但是好像不太好画,就随便搞点
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ],
]
git_repository_path = '/Users/shenzhencheng/Documents/github/contribution_draw'
write_file = 'sample.html'

def push():
    pull_result = subprocess.getoutput("cd %s && git checkout master && git pull" % (git_repository_path))
    print("pull_result: ", pull_result)
    write_sth = subprocess.getoutput("cd %s && echo '<p>mock - sth - %s</p>' >> %s" % (git_repository_path, datetime.datetime.now().isoformat(), write_file))
    print("write_sth: ", write_sth)
    push_result = subprocess.getoutput("cd %s && git add . && git commit -m 'write sth' && git push --force origin master" % (git_repository_path))
    print("push_result: ", push_result)

def fetch_number(begin_timestamp_second):
    '''
    begin_timestamp: 开始时间戳(s)
    返回在template中对应的数字
    '''
    # 解析开始时间,如果这个时间不是周日,那么要等到周日才开始,因为github的第一行是周日
    begin_time_struct = time.localtime(begin_timestamp_second)
    begin_date = datetime.date.fromtimestamp(begin_timestamp_second)
    week_day = begin_time_struct.tm_wday
    # 开始时间要往后偏移 (6 - week_day) 天
    begin_date_offset = 6 - week_day
    true_begin_date = begin_date + datetime.timedelta(days=begin_date_offset)
    # 此时,这个时间对应了template中的第一个点,现在要计算的是,现在时间和真正的开始时间差了几天
    now_date = datetime.date.today()
    # now_date = datetime.date(year=2023, month=3, day=2)
    date_offset_index = (now_date - true_begin_date).days
    # 接下来根据这个date_offset,找到对应的数字
    last_max_index = -1
    for i in range(len(templates)):
        count_sum = 7 * len(templates[i][0])
        this_block_min_index = last_max_index + 1
        this_block_max_index = this_block_min_index + count_sum - 1
        if date_offset_index < this_block_min_index or date_offset_index > this_block_max_index:
            last_max_index = this_block_max_index
            continue
        else:
            retain_count = date_offset_index - last_max_index
            col = (int)((retain_count - 1) / 7)
            row = (int)((retain_count - 1) % 7)
            print("i: ", i, "row: ",row,"col: ",col)
            return templates[i][row][col]
    print("没找到对应的数字")
    return None
'''
我会用linux的crontab来每天一次定时执行这个脚本.执行脚本需要传入第一次调用时的日期(beginTime)
例如我是2022.09.29执行的话,我就传入2022.09.29.程序要计算当前日期是多少,然后在template中找到对应的数,如果这个数是1则push一把

大致流程就是这样,所以这里需要定义几个方法:
1. 根据当前的日期和开始日期,在template中找到并返回对应的值
2. git的一系列操作: 拉取,切换分支,写点东西,推送
'''
def main():
    args = sys.argv[1:]
    year = (int)(args[0])
    month = (int)(args[1])
    day = (int)(args[2])
    print("begin date: %s-%s-%s" % (year, month, day))
    d = datetime.datetime(year=year, month=month, day=day, hour=0, minute=0, second=0)
    ts = d.timestamp()
    number = fetch_number(ts)
    print("number: ", number)
    if number is not None and number > 0:
        print("准备进行push操作...")
        push()

if __name__ == "__main__":
    main()
