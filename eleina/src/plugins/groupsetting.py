from os import stat, times
import re
import random
from typing_extensions import runtime
from nonebot import on_command,on_keyword,on_notice,on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot,Message,GroupMessageEvent,GroupIncreaseNoticeEvent,PokeNotifyEvent

#群禁词系统
keywords=["艹","草","tql"]

keyword_Event=on_keyword(keywords,rule=None,priority=5)

@keyword_Event.handle()
async def kw_ban(bot:Bot,event:GroupMessageEvent,state:T_State):
    try:#管理员撤不了群主的消息，
        id=str(event.get_user_id())
        msg_id=str(event.message_id)
        at_target='[CQ:at,qq={}]'.format(id)
        msg=at_target+'互联网并非法外之地'
        msg=Message(msg)
        await bot.call_api("delete_msg",**{
            'message_id':msg_id
        })
        await keyword_Event.finish(msg)
    except:
        pass

#欢迎新成员
welc_new_friend=on_notice()
@welc_new_friend.handle()
async def wecl_n_f(bot:Bot,event:GroupIncreaseNoticeEvent,state:T_State):
    id=str(event.user_id)
    at_target='[CQ:at,qq={}]'.format(id)
    msg=at_target+'好耶，是新的rbq~'
    msg=Message(msg)
    await welc_new_friend.finish(msg)


#设置禁言，禁言对象必填，时长选填默认30s
#保留，面向对象时
async def ban_speak(group_id,user_id,time=30):
    try:   
        await Bot.call_api("set_group_ban",**{
            'group_id':int(group_id),
            'user_id':int(user_id),
            'duration':int(time)
        })
        at_target='[CQ:at,qq={}]'.format(user_id)
        msg=at_target+'哈哈，又有一个人被禁言了，封嘴{}s'.format(time)
        await Bot.call_api("send_msg",**{
            'group_id':int(group_id),
            'message':msg
        })
    except Exception as e:
        pass

ban=on_command('ban',rule=None)

@ban.handle()
async def handle_ban(bot:Bot,event:GroupMessageEvent,state:T_State):
    msg=str(event.raw_message)
    group_id=event.group_id
    id=re.findall(r"\d+",msg)
    for match in id:
        #await ban_speak(group_id,match,random.randint(5,60))
        time=random.randint(5,60)
        try:   
            await bot.call_api("set_group_ban",**{
                'group_id':int(group_id),
                'user_id':int(match),
                'duration':int(time)
            })
            at_target='[CQ:at,qq={}]'.format(match)
            msg=at_target+'哈哈，又有一个人被禁言了，封嘴{}s'.format(time)
            await bot.call_api("send_msg",**{
                'group_id':int(group_id),
                'message':msg
            })
        except Exception as e:
            pass
    
#设置精华消息
#指令格式：回复-msg @bot /sg
set_point=on_command('sp',rule=to_me())
del_point=on_command('dp',rule=to_me())
@set_point.handle()
async def sg_p(bot:Bot,event:GroupMessageEvent,state:T_State):
    msg=str(event.raw_message)
    msg_id=event.message_id
    id=re.findall(r"\d+",msg)
    check=False
    try:
        await bot.call_api("set_essence_msg",**{
            'message_id':'-{}'.format(id[0])
        })
    except:
        check=True
    try:
        await bot.call_api("set_essence_msg",**{
            'message_id':id[0]
        })
    except:
        if check:
            reply='[CQ:reply,id={}]'.format(msg_id)
            msg=Message(reply+"Invalid")
            await set_point.finish(msg)

@del_point.handle()
async def dp_p(bot:Bot,event:GroupMessageEvent,state:T_State):
    msg=str(event.raw_message)
    msg_id=event.message_id
    id=re.findall(r"\d+",msg)
    check=True
    try:
        await bot.call_api("delete_essence_msg",**{
            'message_id':'-{}'.format(id[0])
        })
        await del_point.finish("已移出")
        check=False
    except:
        pass
    try:
        await bot.call_api("delete_essence_msg",**{
            'message_id':id[0]
        })
        await del_point.finish("已移出")
        check=False
    except:
        pass
    finally:
        if check==False:
            reply='[CQ:reply,id={}]'.format(msg_id)
            msg=Message(reply+"Invalid")
            await set_point.finish(msg)

#生成xml-cardimage大图
generate_cardimage=on_command("generate_image",rule=to_me())

@generate_cardimage.got("msg",prompt="请发送想要转换的图片")
async def g_c_g(bot:Bot,event:GroupMessageEvent,state:T_State):
    try:
        msg=state["msg"]
        msg=msg.replace('CQ:image','CQ:cardimage',1)
        group_id=event.group_id
        await bot.call_api("send_group_msg",**{
            'group_id':group_id,
            'message':msg
        })
    except:
        pass

#json代码在线生成json卡片
#尚不完善，理论上可行
generate_json=on_command("generate_json",rule=to_me())

@generate_json.got("msg",prompt="请传输json代码")
async def g_j_g(bot:Bot,event:GroupMessageEvent,state:T_State):
    try:
        msg=state["msg"]
        cq_json='[CQ:json,data={}]'.format(msg)
        group_id=event.group_id
        await bot.call_api("send_group_message",**{
            'group_id':group_id,
            'message':cq_json
        })
    except Exception as e:
        if str(e)==None:
            await generate_json.finish("Something got wrong~")
        else:
            await generate_json.finish(str(e))

#闪图返回图片
flash_img = on_message(block=False)
@flash_img.handle()
async def _(bot: Bot, event:GroupMessageEvent,state:T_State):
    msg = str(event.raw_message)
    if 'type=flash,' in msg:
        msg = msg.replace('type=flash,', '')
        await flash_img.finish(message=Message("不要发闪照辣，好东西就要分享。" + msg), at_sender=True)

#戳一戳
poke = on_notice(rule=to_me(), block=False)
@poke.handle()
async def _poke(bot: Bot, event: PokeNotifyEvent, state: dict) -> None:
    msg = random.choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
        "?", "差不多得了😅", "欺负咱这好吗？这不好", "我希望你耗子尾汁"
    ])
    await poke.finish(msg, at_sender=True)

#随机数选择 /roll 1,6
roll=on_command("roll")
@roll.handle()
async def roll_h(bot:Bot,event:GroupMessageEvent,state:T_State):
    args=str(event.message).strip()
    num=args.split(',') #仅支持半角逗号
    try:
        res=random.randint(int(num[0]),int(num[1])) #需要强制类型转换不然会报错
    except Exception as e:
        res=str(e)
    if res!=None:
        await roll.finish(str(res))