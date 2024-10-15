""" PagerMaid module to handle sticker collection. """

from PIL import Image
from os.path import exists
from os import sep
from random import randint

from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid
from pyrogram.types import User, Chat

from pagermaid.dependence import sqlite, client
from pagermaid.enums import Message
from pagermaid.listener import listener
from pagermaid.utils import lang, safe_remove

from collections import defaultdict
import json

git_source = "https://raw.githubusercontent.com/midori01/PagerMaid-Plugins/v2/eat/"
positions = {
    "1": [297, 288],
    "2": [85, 368],
    "3": [127, 105],
    "4": [76, 325],
    "5": [256, 160],
    "6": [298, 22],
    "tui": [5, 125],
    "jm": [267, 89, "jm1"],
    "jm1": [51, 87],
    "jgg": [286, 41],
    "ez": [126, 303, "ez1"],
    "ez1": [288, 92],
    "sh": [83, 274],
    "sa": [239, 114],
    "xchi": [164, 285],
    "qv": [30, 180],
    "xkl": [117, 488],
    "ko": [170, 95],
    "tc": [55, 286, "tc1"],
    "tc1": [224, 173],
    "sb": [134, 210],
    "av": [187, 71],
    "sp": [32, 186],
    "dl": [39, 280],
    "ssha": [23, 338],
    "stun": [243, 56],
    "stun1": [110, 84],
    "schi": [292, 201],
    "syao": [42, 141],
    "sy": [13, 266],
    "sz": [96, 13],
    "st": [59, 220],
    "ss": [62, 378],
    "ri": [64, 87],
    "zou": [171, 328, "zou1"],
    "zou1": [444, 339],
    "ada": [223, 314, "ada1"],
    "ada1": [283, 146],
    "gnn": [223, 314, "gnn1"],
    "gnn1": [283, 146],
    "qx": [85, 263],
    "tx": [82, 97],
    "kg": [17,292],
    "bb": [106,276],
    "qm": [382,135],
    "jy": [216,285],
    "dsb": [358,311],
    "dsb1": [198,372],
    "xf": [217,342],
    "dl2": [275,321],
    "love": [381, 228],
    "cy": [398, 224],
    "sn": [37, 265],
    "cb": [282, 351],
    "wenh": [118, 171],
    "hq": [95, 416],
    "cs": [42, 248],
    "bbt": [107, 233],
    "cg": [273, 280],
    "xhs": [150, 172],
    "cy2": [5, 237],
    "diaoy": [56, 397],
    "shuy": [107, 21],
    "shuy2": [107, 21],
    "baib": [7, 269],
    "daif": [225, 32],
    "jtx": [92, 214],
    "rbq": [180, 746],
    "rrbq": [180, 746],
    "bll":[0,230],
    "gdx":[377,241],
    "sese":[162,157],
    "tm":[5,205],
    "chui":[-30,158],
    "huai":[100,-15],
    "cbb":[77,60],
    "zhi":[0,0,"zhi1"],
    "zhi1":[0,0],
    "lp":[14,138],
    "lp1":[15,130],
    "hu":[-25,-40],
    "jtx1":[85,269],
    "ji":[334,60],
    "nz":[84,-5],
    "jtx2":[80,70],
    "tm1":[-28,167],
    "pr":[-15,209],
    "kf":[115,0]
}
notifies = {
    "6": "踢人",
    "tui": "tuì～",
    "jm": "揪咪～",
    "jgg": "举高高",
    "ez": "儿贼～",
    "sh": "鲨画",
    "sa": "啊～",
    "xchi": "小熊吃饼干",
    "qv": "去你的",
    "xkl": "小恐龙",
    "ko": "打人",
    "tc": "老汉推车",
    "sb": "鲨抱送葬",
    "av": "女优",
    "sp": "鲨炮",
    "dl": "多啦打人",
    "ssha": "鲨了你",
    "stun": "嗝",
    "stun1": "一口吞了你",
    "syao": "咬死你",
    "sy": "鲨鱼",
    "sz": "赞一下",
    "st": "踢你哦",
    "ss": "坑爹啊",
    "ri": "日一下",
    "zou": "揍你哦",
    "ada": "给爷死",
    "gnn": "姑奶奶",
    "qx": "骑熊熊～",
    "tx": "踢熊熊～",
    "kg": "快滚～",
    "bb": "抱抱～",
    "qm": "骑马儿～",
    "jy": "监狱圈禁～",
    "dsb": "大傻逼啊～",
    "dsb1": "大傻逼～",
    "xf": "真下饭～",
    "dl2": "大佬！～",
    "love": "爱你！～",
    "cy": "大哥抽烟！～",
    "sn": "等我磨好刀！你没了！",
    "cb": "吃饱了！～",
    "wenh": "你什么意思？～",
    "hq": "真晦气！踩到屎了！～",
    "cs": "吃屎吧你！～",
    "bbt": "吃棒棒糖啦！～",
    "cg": "吃瓜瓜！～",
    "xhs": "看的什么小黄书？～",
    "cy2": "大哥抽烟！～",
    "diaoy": "姜太公钓鱼，愿者上钩！～",
    "shuy": "想你的液！～",
    "shuy2": "想你的液！～",
    "baib": "拜拜大佬！～",
    "daif": "起飞！！大佬带飞！～",
    "jtx": "举个头像",
    "rbq": "绒布球",
    "rrbq": "认做绒布球",
    "bll":"变萝莉",
    "gdx":"狗东西",
    "sese":"不可以涩涩",
    "tm":"舔猫",
    "chui":"锤死你",
    "huai":"一肚子坏水",
    "cbb":"吃粑粑",
    "zhi":"指一下",
    "lp":"老婆快来~",
    "lp1":"老婆快来~",
    "hu":"虎一下",
    "jtx1":"举个头像",
    "ji":"寄",
    "nz":"就不用脑子",
    "jtx2":"举个头像",
    "tm1":"汤姆看书",
    "pr":"prpr~",
    "kf":"狂粉~"
}
extensionConfig = {
    "jgg": {
      "isSwap": True
    },
    "jm": {
      "isSwap": True
    },
    "tui": {
      "isSwap": True
    },
    "qx": {
      "isSwap": True
    },
    "tx": {
      "isSwap": True
    },
    "bb": {
      "isSwap": True
    },
    "qm": {
      "isSwap": True
    },
    "jy": {
      "isSwap": True
    },
    "xf": {
      "isSwap": True
    },
    "sn": {
      "isSwap": True
    },
    "cb": {
      "isSwap": True
    },
    "hq": {
      "isSwap": True
    },
    "cs": {
      "isSwap": True
    },
    "bbt": {
      "isSwap": True
    },
    "cg": {
      "isSwap": True
    },
    "xhs": {
      "isSwap": True
    },
    "diaoy": {
      "isSwap": True
    },
    "shuy": {
      "isSwap": True
    },
    "shuy2": {
      "isSwap": True
    }
}
max_number = len(positions)
configFilePath = f"plugins{sep}eat{sep}config.json"
configFileRemoteUrlKey = "eat.configFileRemoteUrl"


async def eat_it(context, user, base, mask, photo, number, layer=0):
    mask_size = mask.size
    photo_size = photo.size
    if mask_size[0] < photo_size[0] and mask_size[1] < photo_size[1]:
        scale = photo_size[1] / mask_size[1]
        photo = photo.resize(
            (int(photo_size[0] / scale), int(photo_size[1] / scale)), Image.LANCZOS
        )
    photo = photo.crop((0, 0, mask_size[0], mask_size[1]))
    mask1 = Image.new("RGBA", mask_size)
    mask1.paste(photo, mask=mask)
    numberPosition = positions[str(number)]
    isSwap = False
    # 处理头像，放到和背景同样大小画布的特定位置
    try:
        isSwap = extensionConfig[str(number)]["isSwap"]
    except:
        pass
    if isSwap:
        photoBg = Image.new("RGBA", base.size)
        photoBg.paste(mask1, (numberPosition[0], numberPosition[1]), mask1)
        photoBg.paste(base, (0, 0), base)
        base = photoBg
    else:
        base.paste(mask1, (numberPosition[0], numberPosition[1]), mask1)

    # 增加判断是否有第二个头像孔
    isContinue = len(numberPosition) > 2 and layer == 0
    if isContinue:
        await context._client.download_media(
            user.photo.big_file_id, f"plugins{sep}eat{sep}{str(user.id)}.jpg"
        )

        try:
            markImg = Image.open(f"plugins{sep}eat{sep}{str(user.id)}.jpg")
            maskImg = Image.open(
                f"plugins{sep}eat{sep}mask{str(numberPosition[2])}.png"
            ).convert("RGBA")
        except:
            await context.edit(f"图片模版加载出错，请检查并更新配置：mask{str(numberPosition[2])}.png")
            return base
        base = await eat_it(
            context, user, base, maskImg, markImg, numberPosition[2], layer + 1
        )

    temp = base.size[0] if base.size[0] > base.size[1] else base.size[1]
    if temp != 512:
        scale = 512 / temp
        base = base.resize(
            (int(base.size[0] * scale), int(base.size[1] * scale)), Image.LANCZOS
        )

    return base


async def updateConfig(context):
    if configFileRemoteUrl := sqlite.get(configFileRemoteUrlKey, ""):
        if downloadFileFromUrl(configFileRemoteUrl, configFilePath) == 0:
            return await loadConfigFile(context, True)
        sqlite[configFileRemoteUrlKey] = configFileRemoteUrl
        return -1
    return 0


async def downloadFileFromUrl(url, filepath):
    try:
        re = await client.get(url)
        with open(filepath, "wb") as ms:
            ms.write(re.content)
    except:
        return -1
    return 0


async def loadConfigFile(context, forceDownload=False):
    global positions, notifyStrArr, extensionConfig
    try:
        with open(configFilePath, "r", encoding="utf8") as cf:
            # 读取已下载的配置文件
            remoteConfigJson = json.load(cf)
            # positionsStr = json.dumps(positions)
            # positions = json.loads(positionsStr)

            # 读取配置文件中的positions
            positionsStr = json.dumps(remoteConfigJson["positions"])
            data = json.loads(positionsStr)
            # 与预设positions合并
            positions = mergeDict(positions, data)

            # 读取配置文件中的notifies
            data = json.loads(json.dumps(remoteConfigJson["notifies"]))
            # 与预设positions合并
            notifyStrArr = mergeDict(notifyStrArr, data)

            # 读取配置文件中的extensionConfig
            try:
                data = json.loads(json.dumps(remoteConfigJson["extensionConfig"]))
                # 与预设extensionConfig合并
                extensionConfig = mergeDict(extensionConfig, data)
            except:
                # 新增扩展配置，为了兼容旧的配置文件更新不出错，无视异常
                pass

            # 读取配置文件中的needDownloadFileList
            data = json.loads(json.dumps(remoteConfigJson["needDownloadFileList"]))
            # 下载列表中的文件
            for file_url in data:
                try:
                    fsplit = file_url.split("/")
                    filePath = f"plugins{sep}eat{sep}{fsplit[len(fsplit) - 1]}"
                    if not exists(filePath) or forceDownload:
                        await downloadFileFromUrl(file_url, filePath)

                except:
                    await context.edit(f"下载文件异常，url：{file_url}")
                    return -1
    except:
        return -1
    return 0


def mergeDict(d1, d2):
    dd = defaultdict(list)

    for d in (d1, d2):
        for key, value in d.items():
            dd[key] = value
    return dict(dd)


async def downloadFileByIds(ids, context):
    idsStr = f',{",".join(ids)},'
    try:
        with open(configFilePath, "r", encoding="utf8") as cf:
            # 读取已下载的配置文件
            remoteConfigJson = json.load(cf)
            data = json.loads(json.dumps(remoteConfigJson["needDownloadFileList"]))
            # 下载列表中的文件
            sucSet = set()
            failSet = set()
            for file_url in data:
                try:
                    fsplit = file_url.split("/")
                    fileFullName = fsplit[len(fsplit) - 1]
                    fileName = (
                        fileFullName.split(".")[0]
                        .replace("eat", "")
                        .replace("mask", "")
                    )
                    if f",{fileName}," in idsStr:
                        filePath = f"plugins{sep}eat{sep}{fileFullName}"
                        if (await downloadFileFromUrl(file_url, filePath)) == 0:
                            sucSet.add(fileName)
                        else:
                            failSet.add(fileName)
                except:
                    failSet.add(fileName)
                    await context.edit(f"下载文件异常，url：{file_url}")
            notifyStr = "更新模版完成"
            if sucSet:
                notifyStr = f'{notifyStr}\n成功模版如下：{"，".join(sucSet)}'
            if failSet:
                notifyStr = f'{notifyStr}\n失败模版如下：{"，".join(failSet)}'
            await context.edit(notifyStr)
    except:
        await context.edit("更新下载模版图片失败，请确认配置文件是否正确")


@listener(
    is_plugin=True,
    outgoing=True,
    command="eat",
    description="生成一张 吃头像 图片\n"
    "可选：当第二个参数是数字时，读取预存的配置；\n\n"
    "当第二个参数是.开头时，头像旋转180°，并且判断r后面是数字则读取对应的配置生成\n\n"
    "当第二个参数是/开头时，在/后面加url则从url下载配置文件保存到本地，如果就一个/，则直接更新配置文件，删除则是/delete；或者/后面加模版id可以手动更新指定模版配置\n\n"
    "当第二个参数是-开头时，在-后面加上模版id，即可设置默认模版-eat直接使用该模版，删除默认模版是-eat -\n\n"
    "当第二个参数是!或者！开头时，列出当前可用模版",
    parameters="[username/uid] [随意内容]",
)
async def eat(client_: Client, context: Message):
    if len(context.parameter) > 2:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    diu_round = False
    if context.from_user:
        from_user_id = context.from_user.id
    else:
        from_user_id = context.sender_chat.id
    if context.reply_to_message:
        if context.reply_to_message.from_user:
            user = context.reply_to_message.from_user
        else:
            user = context.reply_to_message.sender_chat
        if not user:
            return await context.edit(f"{lang('error_prefix')}{lang('profile_e_no')}")
    else:
        if len(context.parameter) == 1:
            user = context.parameter[0]
            if user.isdigit():
                user = int(user)
        else:
            if context.from_user:
                user = context.from_user
            else:
                user = context.sender_chat
        if context.entities is not None:
            if context.entities[0].type == MessageEntityType.TEXT_MENTION:
                user = context.entities[0].user
            elif context.entities[0].type == MessageEntityType.PHONE_NUMBER:
                user = int(context.parameter[0])
            elif context.entities[0].type == MessageEntityType.BOT_COMMAND:
                if context.from_user:
                    user = context.from_user
                else:
                    user = context.sender_chat
            else:
                return await context.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        if not (isinstance(user, User) or isinstance(user, Chat)):
            if user[:1] in [".", "/", "-", "!"]:
                if context.from_user:
                    user = context.from_user
                else:
                    user = context.sender_chat
            else:
                try:
                    try:
                        user = await client_.get_users(user)
                    except IndexError:
                        user = await client_.get_chat(user)  # noqa
                except (UsernameNotOccupied, UsernameInvalid):
                    return await context.edit(
                        f"{lang('error_prefix')}{lang('profile_e_nou')}"
                    )
                except OverflowError:
                    return await context.edit(
                        f"{lang('error_prefix')}{lang('profile_e_long')}"
                    )
                except Exception as exception:
                    return await context.edit(
                        f"{lang('error_prefix')}{lang('profile_e_nof')}"
                    )
    target_user_id = user.id
    if not user.photo:
        return await context.edit("出错了呜呜呜 ~ 此用户无头像。")
    photo = await client_.download_media(
        user.photo.big_file_id,
        f"plugins{sep}eat{sep}" + str(target_user_id) + ".jpg",
    )

    reply_to = context.reply_to_message.id if context.reply_to_message else None
    if exists(f"plugins{sep}eat{sep}" + str(target_user_id) + ".jpg"):
        for num in range(1, max_number + 1):
            if not exists(f"plugins{sep}eat{sep}eat" + str(num) + ".png"):
                re = await client.get(f"{git_source}eat/eat" + str(num) + ".png")
                with open(f"plugins{sep}eat{sep}eat" + str(num) + ".png", "wb") as bg:
                    bg.write(re.content)
            if not exists(f"plugins{sep}eat{sep}mask" + str(num) + ".png"):
                re = await client.get(f"{git_source}eat/mask" + str(num) + ".png")
                with open(f"plugins{sep}eat{sep}mask" + str(num) + ".png", "wb") as ms:
                    ms.write(re.content)
        number = randint(1, max_number)
        try:
            p1 = 0
            p2 = 0
            if len(context.parameter) == 1:
                p1 = context.parameter[0]
                if p1[0] == ".":
                    diu_round = True
                    if len(p1) > 1:
                        try:
                            p2 = int("".join(p1[1:]))
                        except:
                            # 可能也有字母的参数
                            p2 = "".join(p1[1:])
                elif p1[0] == "-":
                    if len(p1) > 1:
                        try:
                            p2 = int("".join(p1[1:]))
                        except:
                            # 可能也有字母的参数
                            p2 = "".join(p1[1:])
                    if p2:
                        sqlite["eat.default-config"] = p2
                        await context.edit(f"已经设置默认配置为：{p2}")
                    else:
                        del sqlite["eat.default-config"]
                        await context.edit(f"已经清空默认配置")
                    return
                elif p1[0] == "/":
                    await context.edit(f"正在更新远程配置文件")
                    if len(p1) > 1:
                        # 获取参数中的url
                        p2 = "".join(p1[1:])
                        if p2 == "delete":
                            del sqlite[configFileRemoteUrlKey]
                            await context.edit(f"已清空远程配置文件url")
                            return
                        if p2.startswith("http"):
                            # 下载文件
                            if (await downloadFileFromUrl(p2, configFilePath)) != 0:
                                await context.edit(f"下载配置文件异常，请确认url是否正确")
                                return
                            else:
                                # 下载成功，加载配置文件
                                sqlite[configFileRemoteUrlKey] = p2
                                if await loadConfigFile(context, True) != 0:
                                    await context.edit(f"加载配置文件异常，请确认从远程下载的配置文件格式是否正确")
                                    return
                                else:
                                    await context.edit(f"下载并加载配置文件成功")
                        else:
                            # 根据传入模版id更新模版配置，多个用"，"或者","隔开
                            # 判断redis是否有保存配置url

                            splitStr = "，"
                            if "," in p2:
                                splitStr = ","
                            ids = p2.split(splitStr)
                            if len(ids) > 0:
                                # 下载文件
                                configFileRemoteUrl = sqlite.get(
                                    configFileRemoteUrlKey, ""
                                )
                                if configFileRemoteUrl:
                                    if (
                                        await downloadFileFromUrl(
                                            configFileRemoteUrl, configFilePath
                                        )
                                    ) != 0:
                                        await context.edit(f"下载配置文件异常，请确认url是否正确")
                                        return
                                    else:
                                        # 下载成功，更新对应配置
                                        if await loadConfigFile(context) != 0:
                                            await context.edit(
                                                f"加载配置文件异常，请确认从远程下载的配置文件格式是否正确"
                                            )
                                            return
                                        else:
                                            await downloadFileByIds(ids, context)
                                else:
                                    await context.edit(f"你没有订阅远程配置文件，更新个🔨")
                    else:
                        # 没传url直接更新
                        if await updateConfig(context) != 0:
                            await context.edit(
                                f"更新配置文件异常，请确认是否订阅远程配置文件，或从远程下载的配置文件格式是否正确"
                            )
                            return
                        else:
                            await context.edit(f"从远程更新配置文件成功")
                    return
                elif p1[0] == "！" or p1[0] == "!":
                    # 加载配置
                    if exists(configFilePath):
                        if await loadConfigFile(context) != 0:
                            await context.edit(f"加载配置文件异常，请确认从远程下载的配置文件格式是否正确")
                            return
                    txt = ""
                    if len(positions) > 0:
                        noShowList = []
                        for key in positions:
                            txt = f"{txt}，{key}"
                            if len(positions[key]) > 2:
                                noShowList.append(positions[key][2])
                        for key in noShowList:
                            txt = txt.replace(f"，{key}", "")
                        if txt != "":
                            txt = txt[1:]
                    await context.edit(f"目前已有的模版列表如下：\n{txt}")
                    return
            defaultConfig = sqlite.get("eat.default-config", "")
            if isinstance(p2, str):
                number = p2
            elif isinstance(p2, int) and p2 > 0:
                number = int(p2)
            elif not diu_round and (
                (isinstance(p1, int) and int(p1) > 0) or isinstance(p1, str)
            ):
                try:
                    number = int(p1)
                except:
                    number = p1
            elif defaultConfig:
                try:
                    defaultConfig = defaultConfig.decode()
                    number = int(defaultConfig)
                except:
                    number = str(defaultConfig)
                    # 支持配置默认是倒立的头像
                    if number.startswith("."):
                        diu_round = True
                        number = number[1:]

        except:
            number = randint(1, max_number)

        # 加载配置
        if exists(configFilePath):
            if await loadConfigFile(context) != 0:
                await context.edit(f"加载配置文件异常，请确认从远程下载的配置文件格式是否正确")
                return

        try:
            notifyStr = notifyStrArr[str(number)]
        except:
            notifyStr = "吃头像"
        final_msg = await context.edit(f"正在生成 {notifyStr} 图片中 . . .")
        markImg = Image.open(f"plugins{sep}eat{sep}" + str(target_user_id) + ".jpg")
        try:
            eatImg = Image.open(f"plugins{sep}eat{sep}eat" + str(number) + ".png")
            maskImg = Image.open(
                f"plugins{sep}eat{sep}mask" + str(number) + ".png"
            ).convert("RGBA")
        except:
            await context.edit(f"图片模版加载出错，请检查并更新配置：{str(number)}")
            return

        if diu_round:
            markImg = markImg.rotate(180)  # 对图片进行旋转
        try:
            number = str(number)
        except:
            pass
        result = await eat_it(
            context, context.from_user, eatImg, maskImg, markImg, number
        )
        result.save(f"plugins{sep}eat{sep}eat.webp")
        safe_remove(f"plugins{sep}eat{sep}" + str(target_user_id) + ".jpg")
        safe_remove(f"plugins{sep}eat{sep}" + str(target_user_id) + ".png")
        safe_remove(f"plugins{sep}eat{sep}" + str(from_user_id) + ".jpg")
        safe_remove(f"plugins{sep}eat{sep}" + str(from_user_id) + ".png")
    else:
        return await context.edit("此用户未设置头像或头像对您不可见。")
    if reply_to:
        try:
            await client_.send_document(
                context.chat.id,
                f"plugins{sep}eat{sep}eat.webp",
                reply_to_message_id=reply_to,
            )
            await final_msg.safe_delete()
        except TypeError:
            await final_msg.edit("此用户未设置头像或头像对您不可见。")
        except:
            await final_msg.edit("此群组无法发送贴纸。")
    else:
        try:
            await client_.send_document(
                context.chat.id,
                f"plugins{sep}eat{sep}eat.webp",
                message_thread_id=context.message_thread_id,
            )
            await final_msg.safe_delete()
        except TypeError:
            await final_msg.edit("此用户未设置头像或头像对您不可见。")
        except:
            await final_msg.edit("此群组无法发送贴纸。")
    safe_remove(f"plugins{sep}eat{sep}eat.webp")
    safe_remove(photo)
