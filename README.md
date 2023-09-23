# 用于CTFd的QQ播报机器人

使用前需要修改以下内容：
`nonebot.init(superusers={"114514"})`
`if(not (event.group_id==1919810))`
`url = "http://ctfd.ctf/users/{}".format(i)`
实际上这个插件是临时为了招新赛搓的，只能说可以用

使用时只需要superuser用户发送`启动监听`(注意是否设置了前缀)
如果需要的话可以在while最后加一个`time.sleep()`