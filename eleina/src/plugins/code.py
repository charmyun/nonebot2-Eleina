import sys
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot,Message,PrivateMessageEvent

coding=on_command('code',rule=to_me(),priority=1)
#发送过来的&会自动被cp码转成&amp,所以需要先字符替换
@coding.got('''code''',prompt="请输入神秘暗号：")
async def handle_code(bot:Bot,event:PrivateMessageEvent,state:T_State):
    code=state['''code''']
    code=code.replace('&amp;', '&').replace('&#91;', '[').replace('&#93;', ']')
    usr_id=event.user_id
    try:
        scope={}
        with open('redirect.txt','w') as f:
            oldstdout=sys.stdout    #print重定向
            sys.stdout=f
            exec(code,scope)
            sys.stdout=oldstdout
        with open('redirect.txt','r') as f:
            data=f.read()
    except Exception as e:
        data=str(e)
    finally:
        if data==None:
            data="Something got wrong,return None!"
        await bot.call_api("send_private_msg",**{
            'user_id':usr_id,
            'message':data,
            'auto_escape':True
        })