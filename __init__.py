from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import json
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
import nonebot
from nonebot.permission import SUPERUSER

nonebot.init(superusers={"114514"})

# 使用前需要修改以下内容：
# nonebot.init(superusers={"114514"})
# if(not (event.group_id==1919810))
# url = url = "http://ctfd.ctf/users/{}".format(i)
# 实际上这个插件是临时为了招新赛搓的，只能说可以用

session = on_keyword("启动监听", priority=20, block=True,permission=SUPERUSER)
@session.handle()
async def _(event:GroupMessageEvent):
    if(not (event.group_id==1919810)):
       print("非指定群聊")
       return
    while True:
        datas = []
        num = 0
        for i in range(50):
            url = "http://ctfd.ctf/users/{}".format(i)
            response = requests.get(url)
            name = re.search(r"<h1>(.*?)</h1>", response.text).group(1)
            if name == "404":
                continue
            else:
                num += 1
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')
            for row in rows:
                data = []
                cells = row.find_all('td')
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data[0] == "Challenge" or row_data[0] == "挑战":
                    continue
                time_cell = row.find('td', class_='solve-time')
                time_data = time_cell.find('span')['data-time'] if time_cell else ''
                date_time = datetime.strptime(time_data, "%Y-%m-%dT%H:%M:%S.%fZ")
                date_time += timedelta(hours=8)
                row_data.append(date_time.strftime("%d日%H时%M分"))
                data.append(name)
                row_data = [x for x in row_data if x]
                del row_data[2]
                data.append(row_data)
                if data == []:
                    continue
                datas.append(data)    
        try:
            with open('scoreboard.txt', 'r') as file:
                latest = json.load(file)
        except:
            latest = []
        print(latest)
        print(datas) 
        if datas == latest:
            print("无变化") 
            continue
        else:
            extra_elements = []
            for element in datas:
                if element not in latest:
                    extra_elements.append(element)
            print('''已完成对全部 {} 个用户的遍历，新获取到以下内容：'''.format(num)+str(extra_elements))
            with open('scoreboard.txt', 'w') as file:
                file.write(json.dumps(datas))
            for diff in extra_elements:
                await session.send('''恭喜 {} 在 {} 攻破 {} 方向 {} 题目！'''.format(diff[0],diff[1][2],diff[1][1],diff[1][0]))