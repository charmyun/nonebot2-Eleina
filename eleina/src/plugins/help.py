from nonebot import on_command
from nonebot.adapters.cqhttp import Event, Bot

help=on_command("help")
@help.handle()
async def help_h(bot:Bot,event:Event):
    await help.finish(''
        +'---'+'群聊指令'+'---\n'
        +'1.设置禁言：/ban @bqq\n'
        +'2.设置(移出)精华消息：回复[目标消息]@bot /sp(dp)\n'
        +'3.生成随机数：/roll a,b\n'
        +'4.生成xml大图：@bot /generate_image\n'
        +'5.json代码转名片（暂不稳定）:@bot /generate_json\n'
        +'6./help\n'
        +'---'+'私聊指令'+'---\n'
        +'python代码运行：/code\n'
        +'/help'
    '')