## ============================================================
## Agent17 内置修改器 v7.4.5
## UI重构 - 左侧竖向导航栏 + 右侧内容区布局
## v7.2 - 新手引导 / 快捷上手页 / 分组导航 / 操作反馈 / F9 热键
## v7.3 - 「Aurora」视觉重制：石墨黑底 + 琥珀金强调、卡片色条、细分隔线
## v7.4 - 布局重做：双栏仪表盘、等宽瓦片、栅格对齐、内容页滚动条
## ============================================================
## 文件内逻辑分区（C1 折中：受「只改单文件」约束，不做外部拆分）：
##   1) cheat_logic   - 状态变量、基础工具、兼容防御层、修改逻辑（init python）
##   2) cheat_styles  - GUI 常量、样式表（init python + style 语句）
##   3) cheat_ui      - cm_card 卡片组件与 13 个标签页 screen（含主界面）
## ============================================================

init python:
    g_cheat_open = False
    g_cheat_tab = "quick"
    g_cheat_toast = ""
    g_cheat_help = False
    g_cheat_onboard_skip = False
    g_cheat_actor_list = list()
    g_cheat_selected_actor = None
    g_cheat_input_1 = ""
    g_cheat_input_2 = ""
    g_cheat_input_3 = ""
    g_cheat_item_search = ""
    g_cheat_item_results = list()
    g_cheat_item_searched = False
    g_cheat_item_count_input = ""
    g_cheat_actor_filter = ""
    g_cheat_quest_filter = ""
    g_cheat_gallery_key = ""
    g_cheat_var_filter = ""
    g_cheat_var_value = ""
    g_cheat_global_search = ""
    g_cheat_global_results = list()

    import os as _cheat_os

    def _cheat_pick_font():
        for f in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc"):
            try:
                if _cheat_os.path.exists(f):
                    return f.replace("\\", "/")
            except Exception:
                pass
        return None

    _cheat_cn_font = _cheat_pick_font()

    # ---- v7.2: 新手引导 / 标签说明 / 操作反馈 ----
    _cheat_tab_hints = {
        "quick": "常用功能一页搞定：点按钮立即生效，底部会弹出结果提示。",
        "money": "金钱、银行卡与特殊资源。输入数字后点「设定」，或直接点 +1万 快速增加。",
        "player": "玩家自身状态与随身数值，改动即时生效。",
        "actor": "先在左侧选角色，再改好感 / 胁迫 / 心情 / 身体数值；选错了重新点一个即可。",
        "skill": "技能与装备槽：一键解锁或满级，也可单独重置某项技能。",
        "item": "输入关键词搜索物品，再点「添加」或「+99」；数量框留空时默认 +1。",
        "other": "时间、天气、剧情进度与杂项开关，属于高风险改动，建议先快照存档。",
        "quest": "任务列表：可开始、一键完成或移除，也能批量完成全部未完成任务。",
        "daily": "每日限制（角色锁 / 动作锁 / 房间锁）一键清空，方便反复触发事件。",
        "gallery": "图鉴收集：一键解锁相机、图片、书籍、贴纸、音乐、卡片、日记与拼图。",
        "room": "房间与地牢：打开 / 关闭房间、重置全部房间、地牢秒杀敌人。",
        "vars": "高级：直接读写存档变量。改之前务必先快照，不了解的变量不要动。",
        "snapshot": "安全网：改大数值前先「快照存档」，出问题可以回到快照。",
    }

    def Cheat_TabHint(tab):
        return _cheat_tab_hints.get(str(tab), "")

    def Cheat_Toast(msg):
        global g_cheat_toast
        g_cheat_toast = str(msg)

    def Cheat_HelpOpen():
        global g_cheat_help
        g_cheat_help = True

    def Cheat_HelpClose():
        global g_cheat_help, g_cheat_onboard_skip
        g_cheat_help = False
        g_cheat_onboard_skip = True

    def Cheat_Esc():
        global g_cheat_help, g_cheat_onboard_skip
        if g_cheat_help or (not g_cheat_onboard_skip and not Cheat_OnboardSeen()):
            Cheat_HelpClose()
        else:
            Cheat_OpenClose()

    def Cheat_OnboardSeen():
        try:
            return bool(getattr(persistent, "cheat_onboarded", False))
        except Exception:
            return False

    def Cheat_OnboardDone():
        global g_cheat_help, g_cheat_onboard_skip
        g_cheat_help = False
        g_cheat_onboard_skip = True
        try:
            persistent.cheat_onboarded = True
        except Exception:
            pass

    def Cheat_TranslateCN(s):
        try:
            ss = str(s) if s is not None else ""
            if not ss:
                return ss
            r = renpy.translate_string(ss)
            return r if r else ss
        except Exception:
            try:
                return str(s) if s is not None else ""
            except Exception:
                return ""

    _cheat_actor_cn = {
        "e": "埃文", "evan": "埃文", "erica": "艾莉卡", "ericac": "艾莉卡",
        "ruby": "露比", "sakura": "樱", "icequeen": "萨菲尔", "saphire": "萨菲尔",
        "anriel": "安莉尔", "amelia": "阿梅莉亚", "adel": "阿黛尔", "dana": "达娜",
        "chloe": "克洛伊", "nora": "诺拉", "mia": "米娅", "avery": "艾弗里",
        "blue": "布鲁", "katarina": "卡塔琳娜", "zuzana": "祖扎娜", "agent17": "特工17",
        "agent17c": "特工17", "xman": "X先生", "aman": "阿曼", "guide": "向导",
        "goldman": "戈德曼", "jackson": "杰克逊", "trevo": "特雷弗", "cop": "警察",
        "prisoner": "囚犯", "harry": "哈里", "george": "乔治", "pinggy": "平吉",
        "headmaster": "校长", "teacher": "老师", "doctor": "医生", "guard": "警卫",
    }

    def Cheat_ActorNameCN(key):
        try:
            k = str(key)
            if k in _cheat_actor_cn:
                return _cheat_actor_cn[k]
            tb = Cheat_SafeGlobal("TB_Actor", None)
            if tb and key in tb:
                v = tb[key]
                if isinstance(v, dict):
                    for f in ("name", "Name"):
                        if v.get(f):
                            return Cheat_TranslateCN(str(v[f]))
                elif isinstance(v, (list, tuple)) and len(v) >= 2:
                    return Cheat_TranslateCN(str(v[1]))
                elif v:
                    return Cheat_TranslateCN(str(v))
            return str(key)
        except Exception:
            return str(key)

    def Cheat_ActorPortrait(key):
        try:
            tb = Cheat_SafeGlobal("TB_Actor", None)
            if tb and key in tb:
                v = tb[key]
                if isinstance(v, dict) and v.get("portrait"):
                    return str(v["portrait"])
                if isinstance(v, (list, tuple)) and len(v) >= 3 and v[2]:
                    return str(v[2])
            return ""
        except Exception:
            return ""

    def Cheat_InitActorList():
        global g_cheat_actor_list
        g_cheat_actor_list = list()
        _KNOWN_ACTORS = [
            "adel","agent17","alice","amelia","anna","anriel","aria","avery",
            "candy","cecilia","chloe","dana","drugman","elsa","emily","erica",
            "evan","grace","headmaster","helen","hexatail","icequeen",
            "jelly","jihye","katarina","lamia","lan","loretta","luna","lynn",
            "madeleine","mali","matilda","melissa","moring","mother","nora",
            "ophelia","otaku","pearl","redrose","rodmam","romatem","ruby",
            "rusty","sakura","sophia","thomas","violet","zuzana",
        ]
        for key in _KNOWN_ACTORS:
            try:
                GetActor(key)
                g_cheat_actor_list.append(key)
            except:
                pass
        g_cheat_actor_list.sort()

    def Cheat_SelectActor(actorKey):
        global g_cheat_selected_actor
        g_cheat_selected_actor = actorKey

    def Cheat_FilterActorList():
        if not g_cheat_actor_filter:
            return g_cheat_actor_list
        fl = g_cheat_actor_filter.strip().lower()
        return [a for a in g_cheat_actor_list if fl in a.lower() or fl in Cheat_ActorNameCN(a).lower()]

    def Cheat_OpenClose():
        global g_cheat_open
        g_cheat_open = not g_cheat_open
        if g_cheat_open:
            Cheat_InitActorList()
            global g_cheat_selected_actor
            g_cheat_selected_actor = None
        else:
            SelectScreenReset()

    def Cheat_SafeSound(filename="audio/effect/clear.wav"):
        try:
            renpy.sound.play(filename)
        except:
            pass

    def Cheat_SafeSetGlobal(varName, value):
        try:
            store.__setattr__(varName, value)
            if varName in ("g_gold",):
                SetEncryption(value)
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SafeAddGlobal(varName, amount):
        try:
            cur = getattr(store, varName, 0)
            store.__setattr__(varName, cur + amount)
            if varName == "g_gold":
                SetEncryption(cur + amount)
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SafeSetActor(actorKey, attr, value):
        try:
            setattr(GetActor(actorKey), attr, value)
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SafeAddActor(actorKey, attr, amount):
        try:
            actor = GetActor(actorKey)
            cur = getattr(actor, attr, 0)
            setattr(actor, attr, cur + amount)
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SetActorLove(actorKey, valueStr):
        try:
            val = int(valueStr)
            actor = GetActor(actorKey)
            if val > actor.max_love:
                actor.max_love = val
            actor.love = val
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SetActorMaxLove(actorKey, valueStr):
        try:
            val = int(valueStr)
            GetActor(actorKey).max_love = val
            Cheat_SafeSound()
        except:
            pass

    def Cheat_MaxAllLove():
        for akey in g_cheat_actor_list:
            actor = GetActor(akey)
            actor.max_love = 999
            actor.love = 999
        Cheat_Toast("全部角色好感已拉满")
        Cheat_SafeSound()

    def Cheat_MaxAllDuress():
        for akey in g_cheat_actor_list:
            GetActor(akey).duress = 999
        Cheat_Toast("全部角色胁迫已拉满")
        Cheat_SafeSound()

    def Cheat_MaxAllFriendship():
        for akey in g_cheat_actor_list:
            GetActor(akey).friendship = 999
        Cheat_Toast("全部角色友谊已拉满")
        Cheat_SafeSound()

    def Cheat_KnowAll():
        for akey in g_cheat_actor_list:
            GetActor(akey).know = 1
        Cheat_Toast("全部角色已标记为认识")
        Cheat_SafeSound()

    def Cheat_ResetActorCounts(actorKey):
        keys = ["count_hand","count_sex","count_suck","count_anal","count_foot",
                "count_kiss","count_leg","count_breast","count_face","count_mouth",
                "count_cream","count_eat","count_in_anal","count_pantie_masturbate"]
        for k in keys:
            setattr(GetActor(actorKey), k, 0)
        Cheat_SafeSound()

    def Cheat_SearchItem(searchText):
        global g_cheat_item_results, g_cheat_item_searched
        g_cheat_item_results = list()
        g_cheat_item_searched = True
        txt = (searchText or "").strip()
        if not txt:
            Cheat_Toast("请输入要搜索的物品关键词")
            return
        sl = txt.lower()
        for item in ItemData.getAll():
            try:
                raw_name = str(item.Name())
                raw_desc = str(item.Desc())
                key = str(item.GetKey()).lower()
                if sl in raw_name.lower() or sl in raw_desc.lower() or sl in key:
                    g_cheat_item_results.append(item)
                    continue
                cn_name = Cheat_TranslateCN(raw_name)
                cn_desc = Cheat_TranslateCN(raw_desc)
                if cn_name and sl in cn_name.lower():
                    g_cheat_item_results.append(item)
                    continue
                if cn_desc and sl in cn_desc.lower():
                    g_cheat_item_results.append(item)
                    continue
            except Exception:
                pass
        if g_cheat_item_results:
            Cheat_Toast("找到 %d 个物品" % len(g_cheat_item_results))
        else:
            Cheat_Toast("未找到物品：可换韩文名 / 物品 ID；书籍、菜谱请用顶部「全局搜索」")

    def Cheat_SearchItemFromStore():
        # 点击时再读取当前输入值，避免 screen 渲染时机导致的旧值问题
        Cheat_SearchItem(store.g_cheat_item_search)

    def Cheat_ShowAllItems():
        # 不依赖输入法：直接列出全部物品，供中文输入不可用时浏览
        global g_cheat_item_results, g_cheat_item_searched
        g_cheat_item_searched = True
        try:
            g_cheat_item_results = ItemData.getAll()
        except Exception:
            g_cheat_item_results = list()
        if g_cheat_item_results:
            Cheat_Toast("已列出全部 %d 个物品" % len(g_cheat_item_results))
        else:
            Cheat_Toast("物品表为空")

    _CHEAT_SPONSOR_KEY = "516448140ee8ecdb9411b2662dc6246dc68f92ff1f01ec339988732005fe2d3f"

    def Cheat_AddItem(itemKey, countStr):
        # v6.0: 优先调用 PutItem；开发模式非赞助物品被拦截时自动降级为安全直写（与游戏原理一致，不弹 security_warning）
        try:
            cnt = int(countStr)
            if cnt <= 0:
                cnt = 1
            if (config.console or config.developer) and not IsHaveItem(_CHEAT_SPONSOR_KEY, 1) and Sha256(itemKey) != _CHEAT_SPONSOR_KEY:
                item = GetItem(itemKey)
                if item:
                    item.Add(cnt)
                else:
                    item = ItemData(itemKey)
                    g_InventoryItem.append(item)
                    item.Add(cnt)
            else:
                PutItem(itemKey, cnt)
            Cheat_SafeSound("audio/effect/getitem.wav")
            Cheat_Toast("已添加：%s × %d" % (itemKey, cnt))
        except Exception:
            try:
                PutItem(itemKey, int(countStr) if countStr else 1)
            except Exception:
                pass

    def Cheat_AddItemNoSponsor(itemKey, countStr):
        # 通用降级方式：避开开发模式拦截直接加物品
        try:
            cnt = int(countStr)
            if cnt <= 0:
                cnt = 1
            item = GetItem(itemKey)
            if item:
                item.Add(cnt)
            else:
                item = ItemData(itemKey)
                g_InventoryItem.append(item)
                item.Add(cnt)
            Cheat_SafeSound("audio/effect/getitem.wav")
        except Exception:
            pass

    def Cheat_UnlockAllSkills():
        for dataKey in TB_Skill.keys():
            skill = GetSkill(dataKey)
            if skill.GetLevel() == 0:
                skill.LevelUp()
        Cheat_Toast("全部技能已解锁")
        Cheat_SafeSound()

    def Cheat_MaxAllSkills():
        for dataKey in TB_Skill.keys():
            skill = GetSkill(dataKey)
            while skill.GetLevel() < skill.GetMaxLevel():
                skill.LevelUp()
        Cheat_Toast("全部技能已满级")
        Cheat_SafeSound()

    def Cheat_ResetSkill(dataKey):
        try:
            skill = GetSkill(dataKey)
            skill.level = 0
            skill.exp = 0
            Cheat_Toast("技能已重置")
            Cheat_SafeSound()
        except:
            pass

    def Cheat_SkipDay(count):
        # v6.0: 跳日通过调用正规 NextDay() 流程，补跑每日重置（锁定/地图/图鉴/一次性/角色状态）
        try:
            for i in range(int(count)):
                NextDay()
            Cheat_Toast("时间前进 %d 天" % int(count))
            Cheat_SafeSound()
        except Exception:
            try:
                global g_day
                g_day += int(count)
            except Exception:
                pass

    def Cheat_SetTime(t):
        global g_time
        if 1 <= t <= 5:
            g_time = t
            Cheat_Toast("时段已设为 %s" % Cheat_TimeName(t))

    def Cheat_SetDay(d):
        global g_day
        if d >= 1:
            g_day = d

    def Cheat_ClearPrison():
        global g_prisonDay, g_prisonGold
        g_prisonDay = 0
        g_prisonGold = 0
        Cheat_Toast("监狱状态已清空")
        Cheat_SafeSound()

    def Cheat_ClearAllDaily():
        # v6.0: 优先调用游戏正规重置 API
        try:
            ResetDailyFlag()
        except Exception:
            global gd_DailyFlag
            gd_DailyFlag = {}
        try:
            ResetOpenRoomToday()
        except Exception:
            global g_OpenRoomToday
            g_OpenRoomToday = list()
        try:
            ResetLock()
            ResetLockActionToday()
            ResetLockActionTime()
            ResetActorLocationAll()
            ResetTodayOnce()
        except Exception:
            pass
        try:
            global g_LockActorToday, g_LockActionToday, g_today_once, g_LockActorTime, g_LockActionTime
            g_LockActorToday = list()
            g_LockActionToday = list()
            g_today_once = list()
            if not hasattr(store, "g_LockActorTime"):
                g_LockActorTime = list()
            if not hasattr(store, "g_LockActionTime"):
                g_LockActionTime = list()
        except Exception:
            pass
        Cheat_Toast("每日限制已清空")
        Cheat_SafeSound()

    def Cheat_UnlockAllActors():
        # 解除今日/时段角色锁定
        try:
            global g_LockActorToday, g_LockActorTime
            g_LockActorToday = list()
            if hasattr(store, "g_LockActorTime"):
                g_LockActorTime = list()
            ResetLock()
            ResetLockActionToday()
            ResetLockActionTime()
            Cheat_Toast("角色锁定已解除")
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_SetIntSafe(attr, val):
        try:
            setattr(store, attr, int(val))
            Cheat_SafeSound()
        except:
            pass

    def Cheat_TimeName(t):
        names = {1: "\u65e9\u4e0a", 2: "\u4e2d\u5348", 3: "\u508d\u665a", 4: "\u591c\u665a", 5: "\u5348\u591c"}
        return names.get(t, str(t))

    def Cheat_WeatherName(w):
        names = {0: "\u6674\u5929", 1: "\u9634\u5929", 2: "\u96fe\u5929", 3: "\u96e8\u5929"}
        return names.get(w, str(w))

    def Cheat_SetWeather(w):
        global g_weather
        g_weather = w
        Cheat_Toast("天气已设为 %s" % Cheat_WeatherName(w))
        Cheat_SafeSound()

    _CHEAT_SKILL_NAME_MAP = {
        "lockpick": "\u5f00\u9501", "massage": "\u6309\u6469", "discount": "\u6298\u6263",
        "repair": "\u7ef4\u4fee", "stealth": "\u6f5c\u884c", "drug": "\u5236\u836f",
        "knowledge": "\u77e5\u8bc6", "cook": "\u70f9\u996a",
    }
    def Cheat_GetSkillNameCN(skill):
        try:
            key = skill.GetKey()
            return _CHEAT_SKILL_NAME_MAP.get(key, key)
        except:
            return str(skill)

    _CHEAT_SLOT_NAME_MAP = {
        "skip": "\u8df3\u65f6", "onahole": "\u98de\u673a\u676f", "cloth": "\u670d\u88c5",
        "car": "\u6c7d\u8f66", "lockpick": "\u5f00\u9501\u5de5\u5177", "hook": "\u9493\u7aff",
        "whip": "\u97ad\u5b50", "shovel": "\u94f2\u5b50", "mortar": "\u7814\u94b5",
        "telescope": "\u671b\u8fdc\u955c", "sword": "\u6b66\u5668", "sleep": "\u5b89\u7720\u7269\u54c1",
    }
    def Cheat_GetSlotNameCN(slot):
        try:
            if hasattr(slot, 'GetKey'):
                key = slot.GetKey()
            else:
                key = str(slot)
            return _CHEAT_SLOT_NAME_MAP.get(key, key)
        except:
            return str(slot)


init 10 python:
    # F9 全局开关（F1~F4/F7/F8/F11 已被 Ren'Py 默认键位占用，Esc 由菜单内 key 捕获）
    try:
        config.keymap["cheat_menu_toggle"] = ["K_F9"]
        config.underlay.append(renpy.display.behavior.Keymap(cheat_menu_toggle=Function(Cheat_OpenClose)))
    except Exception:
        pass


## ============================================================
## A1 卡片化分组组件（C2 落地）：统一卡片骨架 + 标题主题条
## ============================================================
screen cm_card(title):
    frame:
        style "cmt_card"
        xfill True
        vbox:
            spacing 9
            hbox:
                spacing 9
                add Solid(_cm_c_accent) xsize 3 ysize 14 yalign 0.5
                text title style "cmt_card_title" yalign 0.5
            frame:
                background _cm_c_border
                xfill True
                ysize 1
            null height 1
            transclude


## ============================================================
## 主界面
## ============================================================
## ============================================================
## 主界面（v7.0 主流 GUI 重构：style_prefix "cm" 命名空间）
## ============================================================
screen cheat_menu_main():
    zorder 200
    modal True
    style_prefix "cm"

    key "game_menu" action Function(Cheat_Esc)

    # 全屏遮罩
    frame:
        style "cm_dim"
        xfill True
        yfill True

    # 主容器：标题栏 + 左侧导航 + 右侧内容区
    frame:
        style "cm_root"
        xsize _cm_main_w
        ysize _cm_main_h
        xmaximum _cm_main_w
        ymaximum _cm_main_h
        xalign 0.5
        yalign 0.5

        vbox:
            xfill True
            yfill True
            spacing 0

            # ---- 顶部标题栏 ----
            frame:
                style "cm_hdr"
                xfill True
                ysize _cm_hdr_h

                hbox:
                    xfill True
                    spacing 8

                    frame:
                        style "cm_logo"
                        xsize 26
                        ysize 26
                        yalign 0.5
                        padding (3, 2)

                        text "A17" size 9 color "#0a0a1a" bold True xalign 0.5 yalign 0.5

                    text "Agent17 修改器" style "cm_title" yalign 0.5
                    text "v7.4.5" style "cm_version" yalign 0.5
                    add Solid(_cm_c_border) xsize 1 ysize 22 yalign 0.5
                    text "全局搜索" style "cm_search_label" yalign 0.5
                    frame:
                        background "#1B2029"
                        padding (8, 4)
                        xsize 210
                        input:
                            copypaste True
                            value VariableInputValue("g_cheat_global_search")
                            length 24
                            xfill True
                            yalign 0.5
                            style "cmt_input"
                    textbutton "搜索" style "cm_search_btn" action Function(Cheat_GlobalSearch) yalign 0.5
                    null xfill True
                    textbutton "?" style "cm_help" action Function(Cheat_HelpOpen) yalign 0.5
                    textbutton "X" style "cm_close" text_align 0.5 action Function(Cheat_OpenClose) yalign 0.5

            frame:
                background _cm_c_border
                xfill True
                ysize 1

            # ---- 当前标签说明条（v7.4）----
            frame:
                style "cm_hint_bar"
                xfill True
                hbox:
                    spacing 8
                    text "◆" style "cm_tab_hint" color _cm_c_accent size 9 yalign 0.5
                    text "[Cheat_TabHint(g_cheat_tab)]" style "cm_tab_hint" yalign 0.5
                    null xfill True
                    text "F9 开关 · Esc 关闭" style "cm_tab_hint" yalign 0.5 color "#4E5668"

            # ---- 主体：导航 + 内容 ----
            hbox:
                xfill True
                yfill True
                spacing 0

                # 左侧导航栏（12 标签页，viewport 滚动防溢出裁切）
                frame:
                    style "cm_nav"
                    xsize _cm_nav_w
                    yfill True

                    side "c r":
                        viewport:
                            id "cm_vp_1"
                            mousewheel True
                            draggable True
                            xfill True
                            yfill True

                            vbox:
                                spacing 4
                                xfill True

                                text "常用" style "cm_nav_section"
                                textbutton "★ 快捷" action SetVariable("g_cheat_tab", "quick") style "cm_nav_btn" selected (g_cheat_tab == "quick")
                                textbutton "金钱" action SetVariable("g_cheat_tab", "money") style "cm_nav_btn" selected (g_cheat_tab == "money")
                                textbutton "角色" action SetVariable("g_cheat_tab", "actor") style "cm_nav_btn" selected (g_cheat_tab == "actor")
                                textbutton "物品" action SetVariable("g_cheat_tab", "item") style "cm_nav_btn" selected (g_cheat_tab == "item")

                                text "成长" style "cm_nav_section"
                                textbutton "玩家" action SetVariable("g_cheat_tab", "player") style "cm_nav_btn" selected (g_cheat_tab == "player")
                                textbutton "技能" action SetVariable("g_cheat_tab", "skill") style "cm_nav_btn" selected (g_cheat_tab == "skill")
                                textbutton "任务" action SetVariable("g_cheat_tab", "quest") style "cm_nav_btn" selected (g_cheat_tab == "quest")
                                textbutton "每日" action SetVariable("g_cheat_tab", "daily") style "cm_nav_btn" selected (g_cheat_tab == "daily")

                                text "收集" style "cm_nav_section"
                                textbutton "图鉴" action SetVariable("g_cheat_tab", "gallery") style "cm_nav_btn" selected (g_cheat_tab == "gallery")
                                textbutton "房间" action SetVariable("g_cheat_tab", "room") style "cm_nav_btn" selected (g_cheat_tab == "room")

                                text "系统" style "cm_nav_section"
                                textbutton "其他" action SetVariable("g_cheat_tab", "other") style "cm_nav_btn" selected (g_cheat_tab == "other")
                                textbutton "变量" action SetVariable("g_cheat_tab", "vars") style "cm_nav_btn" selected (g_cheat_tab == "vars")
                                textbutton "快照" action SetVariable("g_cheat_tab", "snapshot") style "cm_nav_btn" selected (g_cheat_tab == "snapshot")

                        vbar:
                            style "cmt_vbar"
                            yfill True
                            value YScrollValue("cm_vp_1")

                # 右侧内容区（13 标签页分发）
                frame:
                    style "cm_content"
                    xfill True
                    yfill True

                    if g_cheat_tab == "quick":
                        use cheat_tab_quick()
                    elif g_cheat_tab == "money":
                        use cheat_tab_money()
                    elif g_cheat_tab == "player":
                        use cheat_tab_player()
                    elif g_cheat_tab == "actor":
                        use cheat_tab_actor()
                    elif g_cheat_tab == "skill":
                        use cheat_tab_skill()
                    elif g_cheat_tab == "item":
                        use cheat_tab_item()
                    elif g_cheat_tab == "other":
                        use cheat_tab_other()
                    elif g_cheat_tab == "quest":
                        use cheat_tab_quest()
                    elif g_cheat_tab == "daily":
                        use cheat_tab_daily()
                    elif g_cheat_tab == "gallery":
                        use cheat_tab_gallery()
                    elif g_cheat_tab == "room":
                        use cheat_tab_room()
                    elif g_cheat_tab == "vars":
                        use cheat_tab_vars()
                    elif g_cheat_tab == "snapshot":
                        use cheat_tab_snapshot()

    # ---- 搜索结果浮层（覆盖式，不挤压主体；对齐内容区顶部）----
    if g_cheat_global_results:
        frame:
            style "cm_search_results"
            xsize _cm_content_w
            xpos _cm_root_x + _cm_nav_w
            ypos _cm_root_y + _cm_hdr_h + 6
            vbox:
                spacing 2
                text "找到 [len(g_cheat_global_results)] 条结果，点击跳转" style "cm_search_hint"
                for gres in g_cheat_global_results:
                    textbutton "[gres[2]]" style "cm_search_item" action Function(Cheat_GlobalJump, gres[0], gres[1])

    # ---- 操作反馈提示条（v7.2）----
    if g_cheat_toast:
        frame:
            style "cm_toast"
            xalign 0.5
            yalign 0.94
            hbox:
                spacing 10
                add Solid(_cm_c_accent) xsize 3 ysize 16 yalign 0.5
                text "[g_cheat_toast]" style "cm_toast_txt" yalign 0.5
        timer 2.6 action SetVariable("g_cheat_toast", "")

    # ---- 首次使用引导（v7.2）----
    if g_cheat_help or (not g_cheat_onboard_skip and not Cheat_OnboardSeen()):
        use cheat_onboard


## ============================================================
## 新手引导浮层（v7.2）
## ============================================================
screen cheat_onboard():
    zorder 300
    modal True

    button:
        xfill True
        yfill True
        background "#000000cc"
        action NullAction()

    frame:
        style "cm_dialog"
        xsize 660
        ysize 450
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 10
            text "欢迎使用 Agent17 修改器 v7.4.5" style "cm_title"
            add Solid(_cm_c_accent) xsize 44 ysize 2
            text "第一次用？记住这三步就够了。" style "cm_tab_hint"
            null height 4
            text "① 先点一次「快照存档」——改坏了随时能回到这一步。" style "cmt_body"
            text "② 常用操作全在「★ 快捷」页：加钱、满好感、解锁图鉴、跳时间。" style "cmt_body"
            text "③ 更细的调整去左侧对应分类；每个页面顶部都有一行说明。" style "cmt_body"
            null height 2
            text "小技巧：F9 随时开关修改器，Esc 关闭；右上角「?」可再次打开本说明。" style "cmt_note"
            null yfill True
            hbox:
                spacing 10
                xalign 1.0
                textbutton "开始使用（不再提示）" style "cmt_action" action Function(Cheat_OnboardDone)
                textbutton "先看看" style "cmt_mini" action Function(Cheat_HelpClose)


## ============================================================
## 标签0: 快捷上手（v7.2，默认页）
## ============================================================
screen cheat_tab_quick():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_3"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing 12

                # ---------------- 第一行：资源 / 全角色 ----------------
                hbox:
                    spacing 12

                    vbox:
                        xsize _cm_panel_w
                        spacing 12

                        use cm_card("① 资源"):
                            grid 2 2:
                                spacing 8
                                textbutton "金币 +1万" style "cmt_tile_primary" xsize _cm_tile2 action [Function(Cheat_SafeAddGlobal, "g_gold", 10000), Function(Cheat_Toast, "金币 +10000")]
                                textbutton "金币 拉满" style "cmt_tile" xsize _cm_tile2 action [Function(Cheat_SafeSetGlobal, "g_gold", 999999), Function(Cheat_Toast, "金币已设为 999999")]
                                textbutton "银行卡 +1万" style "cmt_tile" xsize _cm_tile2 action [Function(Cheat_SafeAddGlobal, "g_card", 10000), Function(Cheat_Toast, "银行卡 +10000")]
                                textbutton "前往金钱页 →" style "cmt_tile_ghost" xsize _cm_tile2 action SetVariable("g_cheat_tab", "money")

                    vbox:
                        xsize _cm_panel_w
                        spacing 12

                        use cm_card("② 全角色一键拉满"):
                            grid 2 3:
                                spacing 8
                                textbutton "好感全满" style "cmt_tile_primary" xsize _cm_tile2 action Function(Cheat_MaxAllLove)
                                textbutton "胁迫全满" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_MaxAllDuress)
                                textbutton "友谊全满" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_MaxAllFriendship)
                                textbutton "心情全满" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_MaxAllMood)
                                textbutton "全部认识" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_KnowAll)
                                textbutton "前往角色页 →" style "cmt_tile_ghost" xsize _cm_tile2 action SetVariable("g_cheat_tab", "actor")

                # ---------------- 第二行：解锁 / 时间与安全 ----------------
                hbox:
                    spacing 12

                    vbox:
                        xsize _cm_panel_w
                        spacing 12

                        use cm_card("③ 一键解锁"):
                            grid 2 2:
                                spacing 8
                                textbutton "全技能满级" style "cmt_tile_primary" xsize _cm_tile2 action Function(Cheat_MaxAllSkills)
                                textbutton "解锁全图鉴" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_GalleryUnlockAll)
                                textbutton "解除角色锁定" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_UnlockAllActors)
                                textbutton "前往图鉴页 →" style "cmt_tile_ghost" xsize _cm_tile2 action SetVariable("g_cheat_tab", "gallery")

                    vbox:
                        xsize _cm_panel_w
                        spacing 12

                        use cm_card("④ 时间与安全"):
                            grid 2 2:
                                spacing 8
                                textbutton "时间 +1 天" style "cmt_tile_primary" xsize _cm_tile2 action Function(Cheat_SkipDay, 1)
                                textbutton "天气晴" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_SetWeather, 0)
                                textbutton "快照存档" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_SnapshotSave)
                                textbutton "自动存档" style "cmt_tile" xsize _cm_tile2 action Function(Cheat_AutoSave)

                # ---------------- 第三行：常用入口 ----------------
                use cm_card("⑤ 常用入口"):
                    grid 3 2:
                        spacing 8
                        textbutton "角色管理" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "actor")
                        textbutton "搜索物品" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "item")
                        textbutton "任务" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "quest")
                        textbutton "每日限制" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "daily")
                        textbutton "房间 / 地牢" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "room")
                        textbutton "剧情 / 天气" style "cmt_tile" xsize _cm_tile3 action SetVariable("g_cheat_tab", "other")
                    null height 4
                    text "所有按钮立即生效，底部弹出结果提示；改大数值前先点「快照存档」。" style "cmt_note"

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_3")


## ============================================================
## 标签1: 金钱资源
## ============================================================
screen cheat_tab_money():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_4"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                # ---- 金钱 ----
                use cm_card("金钱"):
                    hbox:
                        spacing 10
                        text "当前: $[g_gold]" style "cmt_value" color _cm_c_gold yalign 0.5
                        null xfill True
                        frame:
                            background "#1B2029"
                            padding (8, 4)
                            xsize 100
                            input:
                                copypaste True
                                value VariableInputValue("g_cheat_input_1")
                                length 10
                                allow "0123456789"
                                xfill True
                                style "cmt_input"
                        textbutton "设定" style "cmt_action" action Function(Cheat_SafeSetGlobal, "g_gold", int(g_cheat_input_1 or "0"))
                        textbutton "+1K" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_gold", 1000)
                        textbutton "+1万" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_gold", 10000)
                        textbutton "+99999" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_gold", 99999)

                # ---- 银行卡 ----
                use cm_card("银行卡"):
                    hbox:
                        spacing 10
                        text "当前: $[g_card]" style "cmt_value" color _cm_c_gold yalign 0.5
                        null xfill True
                        frame:
                            background "#1B2029"
                            padding (8, 4)
                            xsize 100
                            input:
                                copypaste True
                                value VariableInputValue("g_cheat_input_1")
                                length 10
                                allow "0123456789"
                                xfill True
                                style "cmt_input"
                        textbutton "设定" style "cmt_action" action Function(Cheat_SafeSetGlobal, "g_card", int(g_cheat_input_1 or "0"))
                        textbutton "+1万" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_card", 10000)
                        textbutton "+99999" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_card", 99999)
                        textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_card", 999999)

                # ---- 特殊资源 ----
                use cm_card("特殊资源"):
                    grid 3 2:
                        spacing 10
                        vbox:
                            spacing 4
                            text "精液点数" style "cmt_label"
                            text "[g_semen_point]" style "cmt_value"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 70
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 6
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_semen_point", int(g_cheat_input_1 or "0"))
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_semen_point", 999)
                        vbox:
                            spacing 4
                            text "精液量" style "cmt_label"
                            text "[g_semen_count]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "归零" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_semen_count", 0)
                                textbutton "+10" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_semen_count", 10)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_semen_count", 999)
                        vbox:
                            spacing 4
                            text "Erica资金" style "cmt_label"
                            text "[g_erica_money]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "+500" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_erica_money", 500)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_erica_money", 99999)
                        vbox:
                            spacing 4
                            text "冰女王债务" style "cmt_label"
                            text "[g_icequeen_debt]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "清零" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_icequeen_debt", 0)
                                textbutton "-10" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_icequeen_debt", -10)
                        vbox:
                            spacing 4
                            text "监狱金币" style "cmt_label"
                            text "[g_prisonGold]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "归零" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_prisonGold", 0)
                                textbutton "+100" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_prisonGold", 100)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_prisonGold", 9999)
                        vbox:
                            spacing 4
                            text "延时药丸" style "cmt_label"
                            text "[g_delay_pills]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "+1" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_delay_pills", 1)
                                textbutton "+10" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_delay_pills", 10)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_delay_pills", 99)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_4")


## ============================================================
## 标签2: 玩家属性
## ============================================================
screen cheat_tab_player():
    style_prefix "cmt"
    $ actor = GetActor("e")

    side "c r":
        viewport:
            id "cm_vp_5"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                # ---- 战斗属性 ----
                use cm_card("战斗属性"):
                    grid 3 1:
                        spacing 10
                        vbox:
                            spacing 4
                            text "攻击力" style "cmt_label"
                            text "[g_player_atk]" style "cmt_value" color _cm_c_red
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_atk", 5)
                                textbutton "+50" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_atk", 50)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_player_atk", 999)
                        vbox:
                            spacing 4
                            text "防御力" style "cmt_label"
                            text "[g_player_def]" style "cmt_value" color "#4ecdc4"
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_def", 5)
                                textbutton "+50" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_def", 50)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_player_def", 999)
                        vbox:
                            spacing 4
                            text "魅力" style "cmt_label"
                            text "[g_player_charm]" style "cmt_value" color _cm_c_pink
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_charm", 5)
                                textbutton "+50" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_player_charm", 50)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_player_charm", 999)

                # ---- 生命与体力 ----
                use cm_card("生命与体力"):
                    grid 2 2:
                        spacing 10
                        vbox:
                            spacing 4
                            text "HP" style "cmt_label"
                            text "[actor.GetHP()] / [actor.GetMaxHP()]" style "cmt_value" color _cm_c_red
                            hbox:
                                spacing 3
                                textbutton "回满" style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "hp", actor.max_hp)
                                textbutton "999" style "cmt_mini" action [Function(Cheat_SafeSetActor, "e", "hp", 999), Function(Cheat_SafeSetActor, "e", "max_hp", 999)]
                                textbutton "上限+100" style "cmt_mini" action Function(Cheat_SafeAddActor, "e", "max_hp", 100)
                        vbox:
                            spacing 4
                            text "酒量HP" style "cmt_label"
                            text "[actor.GetDrinkHP()] / [actor.GetMaxDrinkHP()]" style "cmt_value" color _cm_c_red
                            hbox:
                                spacing 3
                                textbutton "回满" style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "drink_hp", actor.max_drink_hp)
                                textbutton "999" style "cmt_mini" action [Function(Cheat_SafeSetActor, "e", "drink_hp", 999), Function(Cheat_SafeSetActor, "e", "max_drink_hp", 999)]
                        vbox:
                            spacing 4
                            text "性奋值" style "cmt_label"
                            text "[actor.GetCoom()] / [actor.max_coom]" style "cmt_value" color _cm_c_pink
                            hbox:
                                spacing 3
                                textbutton "0" style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "coom_value", 0)
                                textbutton "3" style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "coom_value", 3)
                                textbutton "6" style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "coom_value", 6)
                                textbutton "最大99" style "cmt_mini" action [Function(Cheat_SafeSetActor, "e", "coom_value", 99), Function(Cheat_SafeSetActor, "e", "max_coom", 99)]
                        vbox:
                            spacing 4
                            text "心情" style "cmt_label"
                            text "[actor.mood]" style "cmt_value" color _cm_c_gold
                            hbox:
                                spacing 2
                                for i in range(6):
                                    textbutton str(i) style "cmt_mini" action Function(Cheat_SafeSetActor, "e", "mood", i)

                # ---- 任务资源 ----
                use cm_card("任务资源"):
                    grid 3 1:
                        spacing 10
                        vbox:
                            spacing 4
                            text "拳头" style "cmt_label"
                            text "[g_misstion_fist]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_misstion_fist", 5)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_misstion_fist", 99)
                        vbox:
                            spacing 4
                            text "黑客工具" style "cmt_label"
                            text "[g_misstion_hackingtool]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_misstion_hackingtool", 5)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_misstion_hackingtool", 99)
                        vbox:
                            spacing 4
                            text "行动力" style "cmt_label"
                            text "[g_misstion_action]" style "cmt_value"
                            hbox:
                                spacing 3
                                textbutton "+5" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_misstion_action", 5)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_misstion_action", 99)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_5")


## ============================================================
## 标签3: 角色管理
## ============================================================
screen cheat_tab_actor():
    style_prefix "cmt"
    $ _filtered_actors = Cheat_FilterActorList()

    hbox:
        spacing 8
        xfill True
        yfill True

        # ---- 左栏：角色列表 ----
        frame:
            style "cmt_card"
            xsize _cm_actor_list_w
            yfill True

            vbox:
                spacing 6

                text "角色列表" style "cmt_card_title"

                hbox:
                    spacing 4
                    text "搜索:" style "cmt_label" yalign 0.5
                    frame:
                        background "#1B2029"
                        padding (8, 4)
                        xsize 100
                        input:
                            copypaste True
                            value VariableInputValue("g_cheat_actor_filter")
                            length 12
                            xfill True
                            style "cmt_input"

                side "c r":
                    ysize _cm_actor_side_h
                    viewport:
                        id "cm_vp_6"
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True

                        vbox:
                            spacing 1
                            for akey in _filtered_actors:
                                $ is_selected = (g_cheat_selected_actor == akey)
                                $ _ap = Cheat_ActorPortrait(akey)
                                button:
                                    style "cmt_actor_btn"
                                    action Function(Cheat_SelectActor, akey)
                                    if is_selected:
                                        background _cm_c_accent
                                    hbox:
                                        spacing 6
                                        if _ap and renpy.has_image(_ap):
                                            add _ap xysize (34, 34) fit "contain" yalign 0.5
                                        text "[Cheat_ActorNameCN(akey)]" yalign 0.5
                    vbar:
                        style "cmt_vbar"
                        value YScrollValue("cm_vp_6")

                frame:
                    background _cm_c_card2
                    xfill True
                    padding (8, 6)

                    vbox:
                        spacing 4
                        text "全角色批量" style "cmt_label"
                        grid 3 2:
                            spacing 4
                            textbutton "全满好感" style "cmt_mini" xsize _cm_actor_btn_w action Function(Cheat_MaxAllLove)
                            textbutton "全满胁迫" style "cmt_mini" xsize _cm_actor_btn_w action Function(Cheat_MaxAllDuress)
                            textbutton "全满友谊" style "cmt_mini" xsize _cm_actor_btn_w action Function(Cheat_MaxAllFriendship)
                            textbutton "全满心情" style "cmt_mini" xsize _cm_actor_btn_w action Function(Cheat_MaxAllMood)
                            textbutton "全认识" style "cmt_mini" xsize _cm_actor_btn_w action Function(Cheat_KnowAll)
                            null

        # ---- 右栏：角色详情 ----
        frame:
            style "cmt_card"
            xfill True
            yfill True

            if g_cheat_selected_actor:
                $ actor = GetActor(g_cheat_selected_actor)

                side "c r":
                    yfill True
                    viewport:
                        id "cm_vp_7"
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True

                        vbox:
                            spacing _cm_gap

                            text "角色: [Cheat_ActorNameCN(g_cheat_selected_actor)] ([g_cheat_selected_actor])" style "cmt_detail_title"

                            # ---- 核心数值 ----
                            frame:
                                style "cmt_group"
                                vbox:
                                    spacing 6
                                    text "核心数值" style "cmt_group_title"
                                    grid 2 2:
                                        spacing 8
                                        vbox:
                                            spacing 3
                                            text "好感: [actor.GetLove()]/[actor.GetMaxLove()]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                frame:
                                                    background "#1B2029"
                                                    padding (8, 4)
                                                    xsize 70
                                                    input:
                                                        copypaste True
                                                        value VariableInputValue("g_cheat_input_1")
                                                        length 6
                                                        allow "0123456789"
                                                        xfill True
                                                        style "cmt_input"
                                                textbutton "设定" style "cmt_mini" action Function(Cheat_SetActorLove, g_cheat_selected_actor, g_cheat_input_1)
                                                textbutton "最大" style "cmt_mini" action Function(Cheat_SetActorLove, g_cheat_selected_actor, "999")
                                        vbox:
                                            spacing 3
                                            text "胁迫: [actor.duress]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                frame:
                                                    background "#1B2029"
                                                    padding (8, 4)
                                                    xsize 70
                                                    input:
                                                        copypaste True
                                                        value VariableInputValue("g_cheat_input_1")
                                                        length 6
                                                        allow "0123456789"
                                                        xfill True
                                                        style "cmt_input"
                                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "duress", int(g_cheat_input_1 or "0"))
                                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "duress", 999)
                                        vbox:
                                            spacing 3
                                            text "友谊: [actor.GetFriendship()]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                frame:
                                                    background "#1B2029"
                                                    padding (8, 4)
                                                    xsize 70
                                                    input:
                                                        copypaste True
                                                        value VariableInputValue("g_cheat_input_1")
                                                        length 6
                                                        allow "0123456789"
                                                        xfill True
                                                        style "cmt_input"
                                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "friendship", int(g_cheat_input_1 or "0"))
                                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "friendship", 999)
                                        vbox:
                                            spacing 3
                                            text "心情: [actor.mood]" style "cmt_body" color _cm_c_gold
                                            hbox:
                                                spacing 2
                                                for i in range(6):
                                                    textbutton str(i) style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "mood", i)

                            # ---- 身体属性 ----
                            frame:
                                style "cmt_group"
                                vbox:
                                    spacing 6
                                    text "身体属性" style "cmt_group_title"
                                    grid 2 2:
                                        spacing 8
                                        vbox:
                                            spacing 3
                                            text "性奋: [actor.GetCoom()]/[actor.max_coom]" style "cmt_body" color _cm_c_red
                                            hbox:
                                                spacing 3
                                                frame:
                                                    background "#1B2029"
                                                    padding (8, 4)
                                                    xsize 70
                                                    input:
                                                        copypaste True
                                                        value VariableInputValue("g_cheat_input_1")
                                                        length 6
                                                        allow "0123456789"
                                                        xfill True
                                                        style "cmt_input"
                                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "coom_value", int(g_cheat_input_1 or "0"))
                                                textbutton "最大" style "cmt_mini" action [Function(Cheat_SafeSetActor, g_cheat_selected_actor, "coom_value", 99), Function(Cheat_SafeSetActor, g_cheat_selected_actor, "max_coom", 99)]
                                        vbox:
                                            spacing 3
                                            text "HP: [actor.GetHP()]/[actor.GetMaxHP()]" style "cmt_body" color _cm_c_red
                                            hbox:
                                                spacing 3
                                                textbutton "回满" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "hp", actor.max_hp)
                                                textbutton "999" style "cmt_mini" action [Function(Cheat_SafeSetActor, g_cheat_selected_actor, "hp", 999), Function(Cheat_SafeSetActor, g_cheat_selected_actor, "max_hp", 999)]
                                        vbox:
                                            spacing 3
                                            text "酒量: [actor.GetDrinkHP()]/[actor.GetMaxDrinkHP()]" style "cmt_body" color _cm_c_red
                                            hbox:
                                                spacing 3
                                                textbutton "回满" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "drink_hp", actor.max_drink_hp)
                                                textbutton "最大" style "cmt_mini" action [Function(Cheat_SafeSetActor, g_cheat_selected_actor, "drink_hp", 999), Function(Cheat_SafeSetActor, g_cheat_selected_actor, "max_drink_hp", 999)]
                                        vbox:
                                            spacing 3
                                            text "安眠药: [actor.sleep_pills]" style "cmt_body" color _cm_c_red
                                            hbox:
                                                spacing 3
                                                textbutton "0" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "sleep_pills", 0)
                                                textbutton "3" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "sleep_pills", 3)
                                                textbutton "99" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "sleep_pills", 99)

                            # ---- 状态标记 ----
                            frame:
                                style "cmt_group"
                                vbox:
                                    spacing 6
                                    text "状态标记" style "cmt_group_title"
                                    grid 3 1:
                                        spacing 8
                                        vbox:
                                            spacing 3
                                            text "认识: [actor.know]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                textbutton "不认识" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "know", 0)
                                                textbutton "认识" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "know", 1)
                                        vbox:
                                            spacing 3
                                            text "锁定: [actor.lock]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                textbutton "解锁" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "lock", 0)
                                        vbox:
                                            spacing 3
                                            text "移除日: [actor.remove_day]" style "cmt_body"
                                            hbox:
                                                spacing 3
                                                textbutton "清零" style "cmt_mini" action Function(Cheat_SafeSetActor, g_cheat_selected_actor, "remove_day", 0)

                            # ---- H计数 ----
                            frame:
                                style "cmt_group"
                                vbox:
                                    spacing 5
                                    text "H计数" style "cmt_group_title"
                                    grid 2 1:
                                        spacing 10
                                        vbox:
                                            spacing 2
                                            text "手交:[actor.count_hand] 性交:[actor.count_sex] 口交:[actor.count_suck]" style "cmt_note"
                                            text "肛交:[actor.count_anal] 足交:[actor.count_foot] 接吻:[actor.count_kiss]" style "cmt_note"
                                            text "腿交:[actor.count_leg] 乳交:[actor.count_breast] 颜射:[actor.count_face]" style "cmt_note"
                                        vbox:
                                            spacing 2
                                            text "口爆:[actor.count_mouth] 中出:[actor.count_cream] 吞精:[actor.count_eat]" style "cmt_note"
                                            text "肛内:[actor.count_in_anal] 内裤自慰:[actor.count_pantie_masturbate]" style "cmt_note"
                                    textbutton "全部清零" style "cmt_action" action Function(Cheat_ResetActorCounts, g_cheat_selected_actor)
                    vbar:
                        style "cmt_vbar"
                        value YScrollValue("cm_vp_7")

            else:
                text "请从左侧列表选择角色" style "cmt_empty" xalign 0.5 yalign 0.5
## ============================================================
## 标签4: 技能装备
## ============================================================
screen cheat_tab_skill():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_8"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                # ---- 技能管理 ----
                use cm_card("技能管理"):
                    hbox:
                        spacing 6
                        textbutton "全部解锁" style "cmt_action" action Function(Cheat_UnlockAllSkills)
                        textbutton "全部满级" style "cmt_action" action Function(Cheat_MaxAllSkills)
                    if g_InventorySkill:
                        text "已学技能:" style "cmt_label"
                        vbox:
                            spacing 2
                            for skill in g_InventorySkill:
                                if skill.GetLevel() > 0:
                                    hbox:
                                        spacing 8
                                        text "[Cheat_GetSkillNameCN(skill)] Lv.[skill.GetLevel()]/[skill.GetMaxLevel()]" style "cmt_body"
                                        null xfill True
                                        textbutton "重置" style "cmt_mini" action Function(Cheat_ResetSkill, skill.GetKey())

                # ---- 装备槽 ----
                use cm_card("装备槽"):
                    if g_InventoryEquipSlotDic:
                        hbox:
                            spacing 14
                            box_wrap True
                            for dataKey, slot in g_InventoryEquipSlotDic.items():
                                vbox:
                                    spacing 2
                                    text "[Cheat_GetSlotNameCN(dataKey)]" style "cmt_label" color _cm_c_accent bold True
                                    text "[slot.ItemName()] x[slot.GetCount()]" style "cmt_body" color _cm_c_sub

                # ---- 背包容量 ----
                use cm_card("背包容量"):
                    hbox:
                        spacing 6
                        text "最大格数: [g_InventoryItemMaxSlot]" style "cmt_body"
                        null xfill True
                        textbutton "200" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_InventoryItemMaxSlot", 200)
                        textbutton "500" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_InventoryItemMaxSlot", 500)
                        textbutton "999" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_InventoryItemMaxSlot", 999)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_8")


## ============================================================
## 标签5: 物品获取
## ============================================================
screen cheat_tab_item():
    style_prefix "cmt"

    vbox:
        spacing _cm_gap
        xfill True
        yfill True

        # ---- 搜索区（固定）----
        frame:
            style "cmt_card"
            hbox:
                spacing 8
                text "搜索物品:" style "cmt_card_title" yalign 0.5
                frame:
                    background "#1B2029"
                    padding (8, 4)
                    xsize 260
                    input:
                        copypaste True
                        value VariableInputValue("g_cheat_item_search")
                        length 30
                        xfill True
                        style "cmt_input"
                textbutton "搜索" style "cmt_action" action Function(Cheat_SearchItemFromStore)
                textbutton "显示全部" style "cmt_mini" action Function(Cheat_ShowAllItems)

        # ---- 结果列表（滚动区）----
        frame:
            style "cmt_card"
            xfill True
            yfill True

            if g_cheat_item_results:
                side "c r":
                    yfill True
                    viewport:
                        id "cm_vp_9"
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True

                        vbox:
                            spacing 3
                            for item in g_cheat_item_results:
                                frame:
                                    style "cmt_row"
                                    hbox:
                                        spacing 10
                                        xfill True
                                        vbox:
                                            xsize _cm_col_main
                                            text Cheat_TranslateCN(item.Name()) style "cmt_row_name"
                                            text item.Desc() style "cmt_row_id"
                                        null xfill True
                                        hbox:
                                            spacing 3
                                            yalign 0.5
                                            frame:
                                                background "#1B2029"
                                                padding (8, 4)
                                                xsize 55
                                                input:
                                                    copypaste True
                                                    value VariableInputValue("g_cheat_item_count_input")
                                                    length 4
                                                    allow "0123456789"
                                                    xfill True
                                                    style "cmt_input"
                                            textbutton "添加" style "cmt_mini" action Function(Cheat_AddItem, item.GetKey(), g_cheat_item_count_input)
                                            textbutton "+1" style "cmt_mini" action Function(Cheat_AddItem, item.GetKey(), "1")
                                            textbutton "+99" style "cmt_mini" action Function(Cheat_AddItem, item.GetKey(), "99")
                    vbar:
                        style "cmt_vbar"
                        value YScrollValue("cm_vp_9")

            else:
                if g_cheat_item_searched:
                    text "没有找到匹配的物品。\n可换用韩文名 / 物品 ID，或点「显示全部」浏览；书籍、菜谱请用顶部「全局搜索」。" style "cmt_empty" xalign 0.5 yalign 0.5 text_align 0.5
                else:
                    text "输入关键词搜索物品（1 个字符即可）" style "cmt_empty" xalign 0.5 yalign 0.5


## ============================================================
## 标签6: 其他功能
## ============================================================
screen cheat_tab_other():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_10"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                # ---- 时间与天气 ----
                use cm_card("时间与天气"):
                    grid 3 1:
                        spacing 10
                        vbox:
                            spacing 4
                            text "天数: [g_day]" style "cmt_body"
                            hbox:
                                spacing 3
                                textbutton "+1" style "cmt_mini" action Function(Cheat_SkipDay, 1)
                                textbutton "+7" style "cmt_mini" action Function(Cheat_SkipDay, 7)
                                textbutton "设为1" style "cmt_mini" action Function(Cheat_SetDay, 1)
                        vbox:
                            spacing 4
                            text "时段: [g_time] [Cheat_TimeName(g_time)]" style "cmt_body"
                            hbox:
                                spacing 2
                                for t in range(1, 6):
                                    textbutton str(t) style "cmt_mini" action Function(Cheat_SetTime, t)
                        vbox:
                            spacing 4
                            text "周: [g_week]" style "cmt_body"
                            hbox:
                                spacing 3
                                textbutton "+1" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_week", 1)
                                textbutton "设为1" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_week", 1)
                    hbox:
                        spacing 6
                        text "天气: [Cheat_WeatherName(g_weather)]" style "cmt_body"
                        textbutton "晴" style "cmt_mini" action Function(Cheat_SetWeather, 0)
                        textbutton "阴" style "cmt_mini" action Function(Cheat_SetWeather, 1)
                        textbutton "雾" style "cmt_mini" action Function(Cheat_SetWeather, 2)
                        textbutton "雨" style "cmt_mini" action Function(Cheat_SetWeather, 3)

                # ---- 故事进度 ----
                use cm_card("故事进度"):
                    grid 2 4:
                        spacing 8
                        vbox:
                            spacing 3
                            text "[Cheat_ActorNameCN('erica')]: [g_erica_story]" style "cmt_body"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 60
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 4
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_erica_story", int(g_cheat_input_1 or "0"))
                        vbox:
                            spacing 3
                            text "[Cheat_ActorNameCN('ruby')]: [g_ruby_story]" style "cmt_body"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 60
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 4
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_ruby_story", int(g_cheat_input_1 or "0"))
                        vbox:
                            spacing 3
                            text "[Cheat_ActorNameCN('sakura')]: [g_sakura_story]" style "cmt_body"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 60
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 4
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_sakura_story", int(g_cheat_input_1 or "0"))
                        vbox:
                            spacing 3
                            text "冰女王 [Cheat_ActorNameCN('icequeen')]: [g_icequeen_story]" style "cmt_body"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 60
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 4
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_icequeen_story", int(g_cheat_input_1 or "0"))
                        vbox:
                            spacing 3
                            text "校长（Ruby线）: [g_ruby_headmaster]" style "cmt_body"
                            hbox:
                                spacing 3
                                textbutton "+10" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_ruby_headmaster", 10)
                                textbutton "最大" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_ruby_headmaster", 999)
                        vbox:
                            spacing 3
                            text "[Cheat_ActorNameCN('anriel')]看到: [g_anriel_see]" style "cmt_body"
                            hbox:
                                spacing 3
                                textbutton "0" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_anriel_see", 0)
                                textbutton "1" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_anriel_see", 1)
                        vbox:
                            spacing 3
                            text "[Cheat_ActorNameCN('amelia')]菜单: [g_amelia_menu]" style "cmt_body"
                            hbox:
                                spacing 3
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 60
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_input_1")
                                        length 4
                                        allow "0123456789"
                                        xfill True
                                        style "cmt_input"
                                textbutton "设定" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_amelia_menu", int(g_cheat_input_1 or "0"))

                # ---- 全局标志 ----
                use cm_card("全局标志"):
                    grid 3 2:
                        spacing 8
                        vbox:
                            spacing 3
                            text "剧情标记: [g_flag]" style "cmt_body"
                            hbox:
                                spacing 2
                                for v in [0, 1, 2, 3, 5, 10]:
                                    textbutton str(v) style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_flag", v)
                        vbox:
                            spacing 3
                            text "性标记: [g_sex_flag]" style "cmt_body"
                            hbox:
                                spacing 2
                                for v in [0, 1, 2, 3]:
                                    textbutton str(v) style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_sex_flag", v)
                        vbox:
                            spacing 3
                            text "肮脏等级: [g_dirty]" style "cmt_body"
                            hbox:
                                spacing 2
                                textbutton "0" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_dirty", 0)
                                textbutton "1" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_dirty", 1)
                        vbox:
                            spacing 3
                            text "丁丁状态: [g_dick]" style "cmt_body"
                            hbox:
                                spacing 2
                                for v in [0, 1, 2, 3]:
                                    textbutton str(v) style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_dick", v)
                        vbox:
                            spacing 3
                            text "性步骤/厌恶: [g_sex_step]/[g_sex_hate]" style "cmt_body"
                            hbox:
                                spacing 2
                                textbutton "归零" style "cmt_mini" action [Function(Cheat_SafeSetGlobal, "g_sex_step", 0), Function(Cheat_SafeSetGlobal, "g_sex_hate", 0)]
                        vbox:
                            spacing 3
                            text "乱伦补丁: [g_incestPatch]" style "cmt_body"
                            hbox:
                                spacing 2
                                textbutton "开启" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_incestPatch", True)
                                textbutton "关闭" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_incestPatch", False)

                # ---- 监狱与每日 ----
                use cm_card("监狱与每日"):
                    hbox:
                        spacing 16
                        vbox:
                            spacing 4
                            text "监狱天数: [g_prisonDay]  金币: [g_prisonGold]" style "cmt_body"
                            textbutton "清除监狱" style "cmt_action" action Function(Cheat_ClearPrison)
                        vbox:
                            spacing 4
                            text "每日限制/角色锁定" style "cmt_body"
                            textbutton "清除每日限制" style "cmt_action" action Function(Cheat_ClearAllDaily)

                # ---- 杂项 ----
                use cm_card("杂项"):

                    vbox:
                        spacing 4
                        text "Sakura课程（10节）" style "cmt_label"
                        hbox:
                            spacing 2
                            box_wrap True
                            for i in range(10):
                                textbutton "C[i]" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_sakura_class[" + str(i) + "]", 1)
                            textbutton "全部" style "cmt_mini" action [Function(Cheat_SafeSetGlobal, "g_sakura_class[" + str(i) + "]", 1) for i in range(10)]

                    vbox:
                        spacing 4
                        text "赞助奖励" style "cmt_label"
                        textbutton "全部激活" style "cmt_action" action [Function(Cheat_SafeSetGlobal, "g_sponsor_reward1", 1), Function(Cheat_SafeSetGlobal, "g_sponsor_reward2", 1), Function(Cheat_SafeSetGlobal, "g_sponsor_reward3", 1)]

                    vbox:
                        spacing 4
                        text "Ophelia钓鱼 次数:[g_today_fishing]" style "cmt_label"
                        hbox:
                            spacing 3
                            textbutton "重置" style "cmt_mini" action Function(Cheat_SafeSetGlobal, "g_today_fishing", 0)
                            textbutton "事件开启" style "cmt_mini" action [Function(Cheat_SafeSetGlobal, "g_ophelia_fishing_event", True), Function(Cheat_SafeSetGlobal, "g_ophelia_goggle_event", True)]

                    vbox:
                        spacing 4
                        text "Candy小费: [g_candy_tips]/[g_candy_tips_now]" style "cmt_label"
                        hbox:
                            spacing 3
                            textbutton "+1" style "cmt_mini" action Function(Cheat_SafeAddGlobal, "g_candy_tips", 1)
                            textbutton "重置" style "cmt_mini" action [Function(Cheat_SafeSetGlobal, "g_candy_tips", 0), Function(Cheat_SafeSetGlobal, "g_candy_tips_now", 0)]

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_10")
## ============================================================
## GUI 常量与样式（v7.4 「Aurora」重制）
## 采用 Ren'Py 默认 GUI 体系：集中常量 + style_prefix 命名空间 + 标准滚动容器
## ============================================================

init python:
    # ---- GUI 常量（v7.4 「Aurora」设计系统）----
    _cm_sw = config.screen_width
    _cm_sh = config.screen_height

    # 主容器尺寸（自适应 + 最小下限）
    _cm_main_w = max(int(_cm_sw * 0.90), 860)
    _cm_main_h = max(int(_cm_sh * 0.88), 620)
    _cm_hdr_h = 52
    _cm_nav_w = max(int(_cm_main_w * 0.18), 184)
    _cm_content_w = _cm_main_w - _cm_nav_w
    _cm_root_x = max((_cm_sw - _cm_main_w) // 2, 0)
    _cm_root_y = max((_cm_sh - _cm_main_h) // 2, 0)
    _cm_actor_list_w = max(int(_cm_content_w * 0.24), 190)
    # 角色页左栏列表高度：扣掉标题/搜索框/底部批量面板后剩余
    _cm_actor_side_h = max(_cm_main_h - _cm_hdr_h - 28 - 1 - 28 - 32 - 226, 180)
    _cm_actor_btn_w = max(int((_cm_actor_list_w - 32 - 16 - 8) / 3), 78)

    # 字号分级
    _cm_fs_title = 25 if _cm_sh >= 900 else 22
    _cm_fs_hdr = 18 if _cm_sh >= 900 else 16
    _cm_fs_card = 19 if _cm_sh >= 900 else 17
    _cm_fs_name = 17 if _cm_sh >= 900 else 15
    _cm_fs_body = 16 if _cm_sh >= 900 else 14
    _cm_fs_small = 13
    _cm_fs_nav = 18
    _cm_fs_btn = 16

    # 间距与控件尺寸
    _cm_gap = 12 if _cm_sh >= 900 else 10
    _cm_card_pad = 14
    _cm_nav_h = 46
    _cm_mini_x = 40
    _cm_act_x = 66

    # 内容列宽
    _cm_col_main = max(int(_cm_content_w * 0.55), 280)
    _cm_col_sub = max(int(_cm_content_w * 0.32), 170)

    # 栅格：内容区内宽 / 双栏面板 / 2、3 列等宽瓦片
    _cm_content_iw = _cm_content_w - 36
    _cm_panel_w = max(int((_cm_content_iw - 12) / 2), 420)
    _cm_tile2 = max(int((_cm_panel_w - 32 - 8) / 2), 170)
    _cm_tile3 = max(int((_cm_content_iw - 32 - 16) / 3), 160)

    # ---- 配色（石墨黑 + 琥珀金，低饱和、层级靠明度拉开）----
    _cm_c_bg = "#0A0B0F"
    _cm_c_bg2 = "#0E1015"
    _cm_c_nav = "#0C0E13"
    _cm_c_hdr = "#0C0E13"
    _cm_c_card = "#14171F"
    _cm_c_card2 = "#181B23"
    _cm_c_row = "#12151C"
    _cm_c_border = "#252A36"
    _cm_c_txt = "#ECEFF7"
    _cm_c_sub = "#9AA3B8"
    _cm_c_dim = "#69718A"
    _cm_c_accent = "#E8B25C"
    _cm_c_accent2 = "#8AB4F8"
    _cm_c_gold = "#F5C66A"
    _cm_c_red = "#E06C75"
    _cm_c_pink = "#E8B25C"
    _cm_c_btn = "#1B1F29"
    _cm_c_btn_hover = "#2A3040"
    _cm_c_btn_sel = "#E8B25C"
    _cm_c_input = "#0B0D12"
    _cm_c_close = "#1B1F29"
    _cm_c_close_hover = "#E06C75"
    _cm_c_nav_txt = "#9AA3B8"
    _cm_c_thumb = "#2A3040"
    _cm_c_sel_bg = "#E8B25C1C"
    _cm_c_hover_bg = "#FFFFFF0A"
    _cm_c_search_bg = "#101319"
    _cm_c_search_btn = "#1B1F29"
    _cm_c_search_btn_hover = "#2A3040"
    _cm_c_search_panel = "#101319"
    _cm_c_search_item = "#12151C"


# ============================================================
# 主界面样式（style_prefix "cm"）
# ============================================================
style cm_dim:
    background "#000000B8"

style cm_root:
    background _cm_c_bg

style cm_dialog:
    background "#14171F"
    padding (28, 22)

style cm_hdr:
    background _cm_c_hdr
    padding (18, 8)

style cm_logo:
    background _cm_c_accent

style cm_title:
    color "#F2F4FA"
    size _cm_fs_title
    bold True
    font _cheat_cn_font

style cm_version:
    color _cm_c_dim
    size 11
    font _cheat_cn_font

style cm_close:
    background _cm_c_close
    hover_background _cm_c_close_hover
    xsize 34
    ysize 30
    padding (4, 2)
    text_align 0.5
    font _cheat_cn_font
    color "#C9D0E0"
    hover_color "#0A0B0F"
    size 13
    bold True

style cm_nav:
    background _cm_c_nav
    padding (12, 12)

style cm_nav_section:
    color "#5C6478"
    size 10
    bold True
    font _cheat_cn_font
    padding (12, 14, 4, 4)

style cm_nav_btn:
    background None
    hover_background _cm_c_hover_bg
    selected_background _cm_c_sel_bg
    xfill True
    ysize _cm_nav_h
    padding (12, 2)
    text_align 0.0
    color _cm_c_nav_txt
    hover_color "#ECEFF7"
    selected_color _cm_c_accent
    selected_bold True
    size _cm_fs_nav

style cm_search_bar:
    background _cm_c_search_bg
    padding (10, 4)

style cm_search_label:
    color _cm_c_dim
    size _cm_fs_body
    font _cheat_cn_font

style cm_search_hint:
    color _cm_c_accent
    size _cm_fs_small
    font _cheat_cn_font

style cm_search_btn:
    background _cm_c_search_btn
    hover_background _cm_c_search_btn_hover
    color "#C9D0E0"
    hover_color _cm_c_accent
    size _cm_fs_btn
    padding (10, 4)
    yalign 0.5
    font _cheat_cn_font

style cm_search_results:
    background _cm_c_search_panel
    padding (8, 6)

style cm_search_item:
    background _cm_c_search_item
    hover_background _cm_c_btn
    color "#C9D0E0"
    hover_color _cm_c_accent
    size _cm_fs_body
    padding (10, 5)
    xfill True
    font _cheat_cn_font

style cm_content:
    background _cm_c_bg2
    padding (18, 14)

style cm_hint_bar:
    background "#0C0E13"
    padding (18, 3)
    ysize 28

style cm_tab_hint:
    color _cm_c_sub
    size _cm_fs_small
    font _cheat_cn_font

style cm_help:
    background _cm_c_btn
    hover_background _cm_c_accent
    xsize 30
    ysize 30
    padding (4, 2)
    text_align 0.5
    font _cheat_cn_font
    color _cm_c_sub
    hover_color "#17140E"
    bold True
    size 13

style cm_toast:
    background "#161A22F2"
    padding (18, 10)

style cm_toast_txt:
    color "#F2F4FA"
    size 12
    bold True
    font _cheat_cn_font


# ============================================================
# Tab 内容样式（style_prefix "cmt"）
# ============================================================
style cmt_card:
    background _cm_c_card
    padding (16, 14)

style cmt_card_title:
    color "#F2F4FA"
    size _cm_fs_card
    bold True
    font _cheat_cn_font

style cmt_group:
    background _cm_c_card2
    padding (12, 10)

style cmt_group_title:
    color _cm_c_accent
    size _cm_fs_body
    bold True
    font _cheat_cn_font

style cmt_label:
    color _cm_c_dim
    size _cm_fs_small
    font _cheat_cn_font

style cmt_note:
    color _cm_c_dim
    size _cm_fs_small
    font _cheat_cn_font

style cmt_body:
    color "#D7DCEA"
    size _cm_fs_body
    font _cheat_cn_font

style cmt_value:
    color "#F2F4FA"
    size _cm_fs_name
    bold True
    font _cheat_cn_font

style cmt_empty:
    color "#5C6478"
    size 13
    font _cheat_cn_font

style cmt_detail_title:
    color "#F2F4FA"
    size _cm_fs_hdr
    bold True
    font _cheat_cn_font

style cmt_mini:
    background "#222734"
    hover_background "#2F3646"
    xminimum _cm_mini_x
    ysize 32
    padding (8, 2)
    text_align 0.5
    color "#C9D0E0"
    hover_color "#FFFFFF"
    size _cm_fs_btn
    font _cheat_cn_font

style cmt_action:
    background _cm_c_accent
    hover_background "#F2C477"
    xminimum _cm_act_x
    ysize 34
    padding (12, 2)
    text_align 0.5
    color "#17140E"
    hover_color "#17140E"
    size _cm_fs_btn
    bold True
    font _cheat_cn_font

style cmt_tile:
    background "#1B1F29"
    hover_background "#262C3A"
    ysize 44
    padding (10, 2)
    text_align 0.5
    color "#D7DCEA"
    hover_color "#FFFFFF"
    size _cm_fs_btn
    font _cheat_cn_font

style cmt_tile_primary:
    background _cm_c_accent
    hover_background "#F2C477"
    ysize 34
    padding (10, 2)
    text_align 0.5
    color "#17140E"
    hover_color "#17140E"
    size _cm_fs_btn
    bold True
    font _cheat_cn_font

style cmt_tile_ghost:
    background "#14171F"
    hover_background "#222734"
    ysize 34
    padding (10, 2)
    text_align 0.5
    color _cm_c_dim
    hover_color _cm_c_accent
    size _cm_fs_btn
    font _cheat_cn_font

style cmt_input:
    padding (0, 0)
    text_align 0.0
    color "#F2F4FA"
    size _cm_fs_body
    caret Solid("#E8B25C", xsize=2, ysize=16)
    font _cheat_cn_font

style cmt_row:
    background _cm_c_row
    hover_background "#181C25"
    padding (12, 8)

style cmt_row_name:
    color _cm_c_txt
    size _cm_fs_name
    bold True
    font _cheat_cn_font

style cmt_row_id:
    color _cm_c_dim
    size _cm_fs_small
    font _cheat_cn_font

style cmt_actor_btn:
    background _cm_c_row
    hover_background "#1B1F29"
    selected_background _cm_c_sel_bg
    font _cheat_cn_font
    xfill True
    padding (10, 5)
    color _cm_c_nav_txt
    hover_color "#ECEFF7"
    selected_color _cm_c_accent
    selected_bold True

style cmt_vbar:
    xsize 6
    unscrollable "hide"
    base_bar Solid("#0F1117")
    thumb Solid("#394154")
    hover_thumb Solid("#E8B25C")

style cmt_vbar_vthumb:
    background _cm_c_thumb
    hover_background _cm_c_accent


# ============================================================
# v7.4.1 按钮文字样式
# 说明：textbutton 的文字子样式是 <按钮样式>_text；不显式定义时
# 会落到游戏自己的 button_text（大字号），导致导航/瓦片文字溢出。
# ============================================================
style cm_nav_btn_text:
    font _cheat_cn_font
    size _cm_fs_nav
    bold True
    color _cm_c_nav_txt
    hover_color "#ECEFF7"
    selected_color _cm_c_accent
    text_align 0.0
    yalign 0.5

style cm_close_text:
    font _cheat_cn_font
    size 13
    bold True
    color "#C9D0E0"
    hover_color "#0A0B0F"
    yalign 0.5
    text_align 0.5
    xalign 0.5

style cm_help_text:
    font _cheat_cn_font
    size 13
    bold True
    color _cm_c_sub
    hover_color "#17140E"
    yalign 0.5
    text_align 0.5
    xalign 0.5

style cm_search_btn_text:
    font _cheat_cn_font
    size _cm_fs_btn
    color "#C9D0E0"
    hover_color _cm_c_accent
    yalign 0.5

style cm_search_item_text:
    font _cheat_cn_font
    size _cm_fs_body
    color "#C9D0E0"
    hover_color _cm_c_accent
    yalign 0.5

style cmt_mini_text:
    font _cheat_cn_font
    size _cm_fs_btn
    bold True
    color "#C9D0E0"
    hover_color "#FFFFFF"
    yalign 0.5

style cmt_action_text:
    font _cheat_cn_font
    size _cm_fs_btn
    bold True
    color "#17140E"
    hover_color "#17140E"
    yalign 0.5

style cmt_tile_text:
    font _cheat_cn_font
    size _cm_fs_btn
    bold True
    color "#D7DCEA"
    hover_color "#FFFFFF"
    text_align 0.5
    yalign 0.5

style cmt_tile_primary_text:
    font _cheat_cn_font
    size _cm_fs_btn
    bold True
    color "#17140E"
    hover_color "#17140E"
    text_align 0.5
    yalign 0.5

style cmt_tile_ghost_text:
    font _cheat_cn_font
    size _cm_fs_btn
    color _cm_c_dim
    hover_color _cm_c_accent
    text_align 0.5
    yalign 0.5

style cmt_actor_btn_text:
    font _cheat_cn_font
    size _cm_fs_name
    color _cm_c_nav_txt
    hover_color "#ECEFF7"
    selected_color _cm_c_accent
    selected_bold True
    yalign 0.5


init python:

    # ---------- \u517c\u5bb9\u4e0e\u9632\u5fa1\u5c42 ----------
    def Cheat_SafeGlobal(name, default=None):
        # \u5b89\u5168\u8bfb\u53d6 store \u5168\u5c40\u53d8\u91cf\uff0c\u7f3a\u5931\u65f6\u8fd4\u56de\u9ed8\u8ba4\u503c\uff08\u9632\u65e7\u5b58\u6863\u7f3a\u5b57\u6bb5\u5d29\u6e83\uff09
        try:
            if hasattr(store, name):
                v = getattr(store, name)
                if v is None:
                    return default
                return v
        except Exception:
            pass
        return default

    def Cheat_CompatInit():
        # \u7248\u672c\u9002\u914d\uff1a\u4fee\u6b63\u65e7\u5b58\u6863\u53ef\u80fd\u7f3a\u5931/\u9519\u578b\u7684\u6838\u5fc3\u6570\u636e\u7ed3\u6784
        try:
            if not hasattr(store, "gd_DailyFlag") or not isinstance(gd_DailyFlag, dict):
                gd_DailyFlag = {}
        except Exception:
            gd_DailyFlag = {}
        try:
            if not hasattr(store, "g_LockActorToday") or not isinstance(g_LockActorToday, list):
                g_LockActorToday = list()
        except Exception:
            g_LockActorToday = list()
        try:
            if not hasattr(store, "g_LockActionToday") or not isinstance(g_LockActionToday, list):
                g_LockActionToday = list()
        except Exception:
            g_LockActionToday = list()
        try:
            if not hasattr(store, "g_OpenRoomToday") or not isinstance(g_OpenRoomToday, list):
                g_OpenRoomToday = list()
        except Exception:
            g_OpenRoomToday = list()
        try:
            if not hasattr(store, "g_today_once") or not isinstance(g_today_once, list):
                g_today_once = list()
        except Exception:
            g_today_once = list()
        try:
            if not hasattr(store, "g_InventoryEquipSlotDic") or not isinstance(g_InventoryEquipSlotDic, dict):
                g_InventoryEquipSlotDic = {}
        except Exception:
            g_InventoryEquipSlotDic = {}
        try:
            if not hasattr(store, "g_InventoryPicture") or not isinstance(g_InventoryPicture, list):
                g_InventoryPicture = list()
        except Exception:
            g_InventoryPicture = list()
        try:
            if not hasattr(store, "g_InventoryBook") or not isinstance(g_InventoryBook, list):
                g_InventoryBook = list()
        except Exception:
            g_InventoryBook = list()
        try:
            if not hasattr(store, "g_InventorySticker") or not isinstance(g_InventorySticker, list):
                g_InventorySticker = list()
        except Exception:
            g_InventorySticker = list()
        try:
            if not hasattr(store, "g_InventoryLpMusic") or not isinstance(g_InventoryLpMusic, list):
                g_InventoryLpMusic = list()
        except Exception:
            g_InventoryLpMusic = list()
        try:
            if not hasattr(store, "g_InventoryCard") or not isinstance(g_InventoryCard, list):
                g_InventoryCard = list()
        except Exception:
            g_InventoryCard = list()
        try:
            if not hasattr(store, "g_InventoryDiary") or not isinstance(g_InventoryDiary, list):
                g_InventoryDiary = list()
        except Exception:
            g_InventoryDiary = list()
        try:
            if not hasattr(store, "g_InventoryPuzzle") or not isinstance(g_InventoryPuzzle, list):
                g_InventoryPuzzle = list()
        except Exception:
            g_InventoryPuzzle = list()
        try:
            if not hasattr(store, "g_InventoryQuest") or not isinstance(g_InventoryQuest, list):
                g_InventoryQuest = list()
        except Exception:
            g_InventoryQuest = list()
        try:
            if not hasattr(store, "g_InventorySkill") or not isinstance(g_InventorySkill, list):
                g_InventorySkill = list()
        except Exception:
            g_InventorySkill = list()
        try:
            if not hasattr(store, "g_InventoryItem") or not isinstance(g_InventoryItem, list):
                g_InventoryItem = list()
        except Exception:
            g_InventoryItem = list()
        try:
            if not hasattr(store, "g_cheat_actor_filter"):
                g_cheat_actor_filter = ""
        except Exception:
            pass
        try:
            if not hasattr(store, "g_cheat_item_search"):
                g_cheat_item_search = ""
        except Exception:
            pass

    def Cheat_SnapshotSave():
        # \u98ce\u9669\u64cd\u4f5c\u524d\u5feb\u7167\u5b58\u6863\uff1a\u5199\u5165\u4e13\u7528\u69fd\u4f4d\uff08\u65f6\u95f4\u6233\u547d\u540d\uff09\uff0c\u8fd4\u56de\u69fd\u540d
        try:
            now = renpy.get_game_runtime() and renpy.get_game_runtime() or 0
            import time as _t
            slot = "cheat_snapshot_%d" % int(_t.time())
            renpy.save(slot)
            Cheat_Toast("快照已保存")
            return slot
        except Exception:
            return ""

    def Cheat_AutoSave():
        try:
            renpy.force_autosave()
            Cheat_Toast("已触发自动存档")
            return True
        except Exception:
            return False

    def Cheat_SavedList():
        # \u8fd4\u56de\u5feb\u7167\u69fd\u540d\u5217\u8868\uff08cheat_snapshot_*\uff09\uff0c\u6309\u540d\u79f0\u5012\u5e8f
        try:
            sl = renpy.list_saved_games(regexp="cheat_snapshot.*")
            return sorted(sl, reverse=True)[:8]
        except Exception:
            return list()

    def Cheat_Count(container):
        try:
            if container is None:
                return 0
            return len(container)
        except Exception:
            return 0

    # ---------- \u4efb\u52a1\u7cfb\u7edf ----------
    def Cheat_QuestList():
        # \u8fd4\u56de\u5168\u90e8\u4efb\u52a1 key \u5217\u8868\uff08TB_Quest \u8868\u9a71\u52a8 + \u5f53\u524d\u5df2\u63a5\u4efb\u52a1\u5e76\u96c6\uff09
        keys = list()
        try:
            tb = Cheat_SafeGlobal("TB_Quest", None)
            if tb:
                keys = [str(k) for k in list(tb.keys())]
        except Exception:
            pass
        try:
            for q in Cheat_SafeGlobal("g_InventoryQuest", list()):
                if q is None:
                    continue
                try:
                    k = str(q.tesk is not None and getattr(q, "key", "") or getattr(q, "questKey", ""))
                    if k and k not in keys:
                        keys.append(k)
                except Exception:
                    pass
        except Exception:
            pass
        return sorted(set(keys))

    def Cheat_QuestStatus(key):
        # 0=\u672a\u5f00\u59cb 1=\u8fdb\u884c\u4e2d 2=\u9636\u6bb5\u8fdb\u884c\u4e2d 3=\u5df2\u5b8c\u6210
        try:
            q = GetQuest(key)
            if q is not None and q.tesk is not None:
                return int(q.tesk)
        except Exception:
            pass
        try:
            for q in Cheat_SafeGlobal("g_InventoryQuest", list()):
                if q is None:
                    continue
                if str(getattr(q, "key", "")) == key:
                    return int(getattr(q, "tesk", 0) or 0)
        except Exception:
            pass
        return 0

    def Cheat_QuestNameCN(key):
        try:
            tb = Cheat_SafeGlobal("TB_Quest", None)
            if tb and key in tb:
                v = tb[key]
                if isinstance(v, dict):
                    for f in ("desc", "name", "Name"):
                        if v.get(f):
                            return Cheat_TranslateCN(str(v[f]))
                if isinstance(v, (list, tuple)) and len(v) >= 2:
                    return Cheat_TranslateCN(str(v[1]))
                if v:
                    return Cheat_TranslateCN(str(v))
        except Exception:
            pass
        return key

    def Cheat_QuestStart(key):
        # \u901a\u8fc7\u5408\u6cd5 API \u5f00\u59cb\u4efb\u52a1
        try:
            StartQuest(key)
            Cheat_SafeSound()
        except Exception:
            try:
                GenQuestData(key)
                Cheat_SafeSound()
            except Exception:
                pass

    def Cheat_QuestClear(key):
        # \u901a\u8fc7\u5408\u6cd5 API \u5b8c\u6210\u4efb\u52a1
        try:
            ClearQuest(key)
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_QuestRemove(key):
        # \u901a\u8fc7\u5408\u6cd5 API \u79fb\u9664\u4efb\u52a1
        try:
            RemoveQuest(key)
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_QuestClearAllDone():
        # \u4e00\u952e\u6e05\u7a7a\u6240\u6709\u5df2\u5b8c\u6210\u4efb\u52a1
        cnt = 0
        try:
            for k in Cheat_QuestList():
                if Cheat_QuestStatus(k) == 3:
                    ClearQuest(k)
                    cnt += 1
        except Exception:
            pass
        if cnt:
            Cheat_SafeSound()
        return cnt

    def Cheat_QuestQuestFilter(txt):
        txt = (txt or "").strip().lower()
        out = list()
        for k in Cheat_QuestList():
            if not txt or txt in k.lower() or txt in Cheat_QuestNameCN(k).lower():
                out.append(k)
        return out[:200]

    # ---------- \u6bcf\u65e5\u9650\u5236 ----------
    def Cheat_DailySummary():
        # \u751f\u6210\u6bcf\u65e5\u9650\u5236\u6587\u672c\u6458\u8981
        lines = list()
        try:
            d = Cheat_SafeGlobal("gd_DailyFlag", dict())
            lines.append("\u6bcf\u65e5\u6807\u5fd7: %d \u6761" % Cheat_Count(d))
        except Exception:
            lines.append("\u6bcf\u65e5\u6807\u5fd7: 0 \u6761")
        lines.append("\u4eca\u65e5\u89d2\u8272\u9501: %d \u4e2a" % Cheat_Count(Cheat_SafeGlobal("g_LockActorToday", list())))
        try:
            lines.append("\u4eca\u65e5\u52a8\u4f5c\u9501: %d \u4e2a" % Cheat_Count(Cheat_SafeGlobal("g_LockActionToday", list())))
        except Exception:
            pass
        lines.append("\u4eca\u65e5\u623f\u95f4\u9501: %d \u4e2a" % Cheat_Count(Cheat_SafeGlobal("g_OpenRoomToday", list())))
        lines.append("\u4eca\u65e5\u4e00\u6b21\u6027: %d \u4e2a" % Cheat_Count(Cheat_SafeGlobal("g_today_once", list())))
        return "\n".join(lines)

    def Cheat_ResetDailyOnly():
        # \u4ec5\u6e05\u7a7a\u6bcf\u65e5\u6807\u8bb0\uff08\u4e0d\u91cd\u7f6e\u9501/\u623f\u95f4/\u4e00\u6b21\u6027\uff09
        try:
            ResetDailyFlag()
            Cheat_SafeSound()
        except Exception:
            global gd_DailyFlag
            gd_DailyFlag = {}
            Cheat_SafeSound()

    # ---------- \u56fe\u9274\u6536\u96c6 ----------
    def Cheat_GalleryInfo():
        lines = list()
        lines.append("\u76f8\u673a: %d" % Cheat_Count(Cheat_SafeGlobal("g_CameraGet", list())))
        lines.append("\u56fe\u7247: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryPicture", list())))
        lines.append("\u4e66\u7c4d: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryBook", list())))
        lines.append("\u8d34\u7eb8: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventorySticker", list())))
        lines.append("\u97f3\u4e50: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryLpMusic", list())))
        lines.append("\u5361\u7247: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryCard", list())))
        lines.append("\u65e5\u8bb0: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryDiary", list())))
        lines.append("\u62fc\u56fe: %d" % Cheat_Count(Cheat_SafeGlobal("g_InventoryPuzzle", list())))
        return "\n".join(lines)

    def Cheat_ManualCollect(cat, key):
        # \u901a\u7528\u6536\u96c6\uff1acat in picture/book/sticker/lpmusic/card/diary
        try:
            if cat == "picture":
                PutPicture(key)
            elif cat == "book":
                PutBook(key)
            elif cat == "sticker":
                PutSticker(key)
            elif cat == "lpmusic":
                PutLpMusic(key)
            elif cat == "card":
                PutCard(key)
            elif cat == "diary":
                PutDiary(key)
            else:
                return False
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    def Cheat_GalleryUnlockAll():
        # \u4e00\u952e\u89e3\u9501\u5168\u90e8\u56fe\u9274\uff1a\u76f8\u673a/\u56fe\u7247/\u4e66\u7c4d/\u8d34\u7eb8/\u97f3\u4e50/\u5361\u7247/\u65e5\u8bb0/\u62fc\u56fe
        ok = 0
        fail = 0
        try:
            tb = Cheat_SafeGlobal("TB_Camera", dict())
            for k in list(tb.keys()):
                try:
                    cam = GetCamera(k)
                    if cam is not None:
                        SetItem(k)
                        ok += 1
                except Exception:
                    fail += 1
        except Exception:
            fail += 1
        for cat, tbname, fn in [
            ("picture", "TB_Picture", "PutPicture"),
            ("book", "TB_Book", "PutBook"),
            ("sticker", "TB_Sticker", "PutSticker"),
            ("lpmusic", "TB_LpMusic", "PutLpMusic"),
            ("card", "TB_Card", "PutCard"),
            ("diary", "TB_Diary", "PutDiary"),
        ]:
            try:
                tb = Cheat_SafeGlobal(tbname, dict())
                if not tb:
                    continue
                for k in list(tb.keys()):
                    try:
                        if fn == "PutPicture":
                            PutPicture(k)
                        elif fn == "PutBook":
                            PutBook(k)
                        elif fn == "PutSticker":
                            PutSticker(k)
                        elif fn == "PutLpMusic":
                            PutLpMusic(k)
                        elif fn == "PutCard":
                            PutCard(k)
                        elif fn == "PutDiary":
                            PutDiary(k)
                        ok += 1
                    except Exception:
                        fail += 1
            except Exception:
                fail += 1
        # \u62fc\u56fe\uff1aTB_Puzzle \u5168\u89e3\u9501
        try:
            tb = Cheat_SafeGlobal("TB_Puzzle", dict())
            for k in list(tb.keys()):
                try:
                    pz = GetPuzzle(k)
                    if pz is not None:
                        pz.complite = True
                        pz.firstComplite = False
                        ok += 1
                except Exception:
                    fail += 1
        except Exception:
            fail += 1
        if ok:
            Cheat_SafeSound()
        Cheat_Toast("图鉴解锁完成：成功 %d 项" % ok)
        return (ok, fail)

    # ---------- \u623f\u95f4 / \u5730\u7262 ----------
    def Cheat_RoomList():
        try:
            tb = Cheat_SafeGlobal("TB_Room", dict())
            return sorted([str(k) for k in list(tb.keys())])
        except Exception:
            return list()

    def Cheat_RoomNameCN(key):
        try:
            tb = Cheat_SafeGlobal("TB_Room", dict())
            if key in tb:
                v = tb[key]
                if isinstance(v, dict):
                    for f in ("name", "Name", "desc"):
                        if v.get(f):
                            return Cheat_TranslateCN(str(v[f]))
                if isinstance(v, (list, tuple)) and len(v) >= 2:
                    return Cheat_TranslateCN(str(v[1]))
                if v:
                    return Cheat_TranslateCN(str(v))
        except Exception:
            pass
        return key

    def Cheat_RoomOpenCount():
        return Cheat_Count(Cheat_SafeGlobal("g_OpenRoomToday", list()))

    def Cheat_OpenRoom(key):
        try:
            OpenRoomToday(key)
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_CloseRoom(key):
        try:
            CloseRoomToday(key)
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_ResetAllRooms():
        try:
            ResetOpenRoomToday()
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_DungeonStatus():
        active = Cheat_SafeGlobal("g_dungeon_active", False)
        killed = Cheat_Count(Cheat_SafeGlobal("g_dungeon_killed", list()))
        return "\u5730\u7262\u6d3b\u8dc3: %s    \u5df2\u51fb\u6740\u654c\u4eba: %d" % (str(active), killed)

    def Cheat_DungeonInit():
        try:
            InitDungeon()
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_DungeonExit():
        try:
            ExitDungeon()
            Cheat_SafeSound()
        except Exception:
            pass

    def Cheat_DungeonKillAll():
        # \u51fb\u6740\u5730\u7262\u5185\u5168\u90e8\u5b58\u6d3b\u602a\u7269\uff08\u5408\u6cd5 KillMonster\uff09
        cnt = 0
        try:
            for rk in Cheat_RoomList():
                try:
                    if IsMonsterAlive(rk):
                        KillMonster(rk)
                        cnt += 1
                except Exception:
                    pass
        except Exception:
            pass
        if cnt:
            Cheat_SafeSound()
            Cheat_Toast("已击杀 %d 个敌人" % cnt)
        return cnt

    # ---------- \u5168\u5c40\u53d8\u91cf\u7f16\u8f91\u5668\uff08\u8986\u76d6\u89d2\u8272\u4e13\u5c5e\u6545\u4e8b\u53d8\u91cf/\u5b58\u6863\u6301\u4e45\u5316\u6570\u636e\uff09 ----------
    def Cheat_VarsList(filterText):
        # \u5217\u51fa store \u4e2d\u6240\u6709 g_ \u5f00\u5934\u53d8\u91cf\u540d\uff08\u6700\u591a 400\uff09\uff0c\u652f\u6301\u8fc7\u6ee4
        ft = (filterText or "").strip().lower()
        out = list()
        try:
            for n in dir(store):
                if n.startswith("g_") or n.startswith("gd_") or n.startswith("q_"):
                    if ft and ft not in n.lower():
                        continue
                    out.append(n)
        except Exception:
            pass
        return sorted(out)[:400]

    def Cheat_VarDisplay(name):
        # \u5b89\u5168\u8bfb\u53d6\u53d8\u91cf\u5e76\u8f6c\u4e3a\u53ef\u663e\u793a\u5b57\u7b26\u4e32
        try:
            if not hasattr(store, name):
                return "<\u672a\u5b9a\u4e49>"
            v = getattr(store, name)
            try:
                return repr(v)
            except Exception:
                return str(v)
        except Exception:
            return "<\u8bfb\u53d6\u5931\u8d25>"

    def Cheat_VarSet(name, valueStr):
        # \u89e3\u6790\u7c7b\u578b\u5e76\u5b89\u5168\u5199\u5165\uff08g_gold \u81ea\u52a8\u8054\u52a8\u52a0\u5bc6\uff09
        import re as _re
        try:
            vs = (valueStr or "").strip()
            if vs == "":
                return False
            v = None
            if vs.lower() == "true":
                v = True
            elif vs.lower() == "false":
                v = False
            elif vs.lower() in ("none", "null"):
                v = None
            else:
                try:
                    if _re.fullmatch(r"[+-]?\d+", vs):
                        v = int(vs)
                    elif _re.fullmatch(r"[+-]?\d+\.\d+", vs):
                        v = float(vs)
                    elif vs.startswith("[") and vs.endswith("]"):
                        import json as _json
                        v = _json.loads(vs)
                    elif vs.startswith("{") and vs.endswith("}"):
                        import json as _json
                        v = _json.loads(vs)
                    else:
                        v = vs
                except Exception:
                    v = vs
            setattr(store, name, v)
            if name == "g_gold":
                try:
                    SetEncryption(int(v or 0))
                except Exception:
                    pass
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    # ---------- \u89d2\u8272\u6df1\u5c42\u72b6\u6001\uff08\u4f4d\u7f6e/\u5916\u89c2/Buff/\u8bb0\u5fc6\uff09 ----------
    def Cheat_ActorDeepList():
        # \u89d2\u8272\u5217\u8868\uff08\u4f9b\u6df1\u5c42\u72b6\u6001\u9875\u590d\u7528\uff09
        return Cheat_FilterActorList()

    def Cheat_ActorPosText(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return "<\u65e0>"
            loc = getattr(a, "location", None)
            if loc is None:
                loc = getattr(a, "room", "")
            return str(loc)
        except Exception:
            return "<\u65e0>"

    def Cheat_ActorSetLocation(akey, loc):
        try:
            a = GetActor(akey)
            if a is None:
                return False
            try:
                a.setLocation(loc)
            except Exception:
                a.location = loc
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    def Cheat_ActorResetLocation(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return False
            try:
                a.resetLocation()
            except Exception:
                try:
                    ResetActorLocation(akey)
                except Exception:
                    a.location = ""
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    def Cheat_ActorBuffText(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return "<\u65e0>"
            b = getattr(a, "buff", None)
            if b is None:
                return "<\u65e0>"
            return str(b)
        except Exception:
            return "<\u65e0>"

    def Cheat_ActorClearBuff(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return False
            try:
                a.buff = list()
            except Exception:
                a.buff = []
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    def Cheat_ActorMemoryText(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return "<\u65e0>"
            m = getattr(a, "memory", None)
            if m is None:
                return "<\u65e0>"
            return str(m)[:200]
        except Exception:
            return "<\u65e0>"

    def Cheat_ActorResetMemory(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return False
            try:
                a.ResetMemory()
            except Exception:
                a.memory = list()
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    def Cheat_ActorLookText(akey):
        try:
            a = GetActor(akey)
            if a is None:
                return "<\u65e0>"
            try:
                return str(a.GetLook())
            except Exception:
                return str(getattr(a, "look", ""))
        except Exception:
            return "<\u65e0>"

    def Cheat_ActorSetLook(akey, lookStr):
        try:
            a = GetActor(akey)
            if a is None:
                return False
            try:
                a.SetLook(lookStr)
            except Exception:
                a.look = lookStr
            Cheat_SafeSound()
            return True
        except Exception:
            return False

    # ---------- \u7248\u672c\u9002\u914d\u4fe1\u606f ----------
    def Cheat_VersionInfo():
        try:
            v = config.version
            return "Ren'Py %s" % str(v)
        except Exception:
            return "Ren'Py (unknown)"

    def Cheat_QuestStatusText(s):
        return {0: "\u672a\u5f00\u59cb", 1: "\u8fdb\u884c\u4e2d", 2: "\u9636\u6bb5\u8fdb\u884c\u4e2d", 3: "\u5df2\u5b8c\u6210"}.get(int(s), str(s))

    # ---------- 任务一键完成链（v7.1）----------
    def Cheat_QuestForceDone(key):
        # 一键完成：未开始先走 StartQuest，再走官方 ClearQuest 完成；返回最新状态（3 表示已成功完成）
        try:
            if Cheat_QuestStatus(key) == 0:
                try:
                    StartQuest(key)
                except Exception:
                    pass
            ClearQuest(key)
            Cheat_SafeSound()
        except Exception:
            pass
        return Cheat_QuestStatus(key)

    def Cheat_QuestDoneAll():
        # 一键完成所有未完成任务（状态 0/1/2 -> 3），返回完成数量
        cnt = 0
        for k in Cheat_QuestList():
            try:
                if Cheat_QuestStatus(k) != 3:
                    if Cheat_QuestStatus(k) == 0:
                        try:
                            StartQuest(k)
                        except Exception:
                            pass
                    ClearQuest(k)
                    cnt += 1
            except Exception:
                pass
        if cnt:
            Cheat_SafeSound()
            Cheat_Toast("已一键完成 %d 个任务" % cnt)
        return cnt

    # ---------- 角色关系批量（v7.1）----------
    def Cheat_MaxAllMood():
        # 全部角色心情拉满（0-5 档取 5）
        for akey in g_cheat_actor_list:
            try:
                GetActor(akey).mood = 5
            except Exception:
                pass
        Cheat_Toast("全部角色心情已拉满")
        Cheat_SafeSound()

    # ---------- 全局搜索（v7.1）----------
    def Cheat_GlobalSearch():
        global g_cheat_global_results
        g_cheat_global_results = list()
        txt = (g_cheat_global_search or "").strip().lower()
        if not txt:
            return
        # 角色
        for a in g_cheat_actor_list:
            try:
                name = Cheat_ActorNameCN(a)
                if txt in a.lower() or txt in name.lower():
                    g_cheat_global_results.append(("actor", a, "角色: %s (%s)" % (name, a)))
            except Exception:
                pass
        # 任务
        for k in Cheat_QuestList():
            try:
                nm = Cheat_QuestNameCN(k)
                if txt in k.lower() or txt in nm.lower():
                    g_cheat_global_results.append(("quest", k, "任务: %s (%s)" % (nm, k)))
            except Exception:
                pass
        # 物品（原名 + 中文名 + ID）
        try:
            for item in ItemData.getAll():
                try:
                    raw_name = str(item.Name())
                    key = str(item.GetKey()).lower()
                    cn_name = Cheat_TranslateCN(raw_name)
                    if txt in raw_name.lower() or txt in key or (cn_name and txt in cn_name.lower()):
                        g_cheat_global_results.append(("item", str(item.GetKey()), "物品: %s (%s)" % (cn_name, str(item.GetKey()))))
                except Exception:
                    pass
        except Exception:
            pass
        # 图鉴：书籍 / 图片 / 贴纸 / 音乐 / 卡片 / 日记
        for _cat, _tbname, _label in (
            ("book", "TB_Book", "书籍"),
            ("picture", "TB_Picture", "图片"),
            ("sticker", "TB_Sticker", "贴纸"),
            ("lpmusic", "TB_LpMusic", "音乐"),
            ("card", "TB_Card", "卡片"),
            ("diary", "TB_Diary", "日记"),
        ):
            try:
                _tb = Cheat_SafeGlobal(_tbname, None)
                if not _tb:
                    continue
                for _k in _tb.keys():
                    try:
                        _v = _tb[_k]
                        _nm = ""
                        if isinstance(_v, dict):
                            for _f in ("name", "title"):
                                if _v.get(_f):
                                    _nm = str(_v[_f])
                                    break
                        elif isinstance(_v, (list, tuple)) and len(_v) > 0:
                            _nm = str(_v[0])
                        _cn = Cheat_TranslateCN(_nm) if _nm else ""
                        if txt in str(_k).lower() or (_nm and txt in _nm.lower()) or (_cn and txt in _cn.lower()):
                            g_cheat_global_results.append(("gallery", _k, "%s: %s (%s)" % (_label, _cn or _nm or _k, _k)))
                    except Exception:
                        pass
            except Exception:
                pass
        # 房间
        for rk in Cheat_RoomList():
            try:
                nm = Cheat_RoomNameCN(rk)
                if txt in rk.lower() or txt in nm.lower():
                    g_cheat_global_results.append(("room", rk, "房间: %s (%s)" % (nm, rk)))
            except Exception:
                pass
        # 变量
        for v in Cheat_VarsList(""):
            try:
                if txt in v.lower():
                    g_cheat_global_results.append(("var", v, "变量: %s" % v))
            except Exception:
                pass
        g_cheat_global_results = g_cheat_global_results[:10]
        if g_cheat_global_results:
            Cheat_Toast("找到 %d 条结果" % len(g_cheat_global_results))
        else:
            Cheat_Toast("未找到与「%s」相关的内容" % txt)

    def Cheat_GlobalJump(kind, key):
        global g_cheat_tab, g_cheat_global_results
        try:
            if kind == "actor":
                g_cheat_tab = "actor"
                g_cheat_selected_actor = key
                g_cheat_actor_filter = ""
            elif kind == "quest":
                g_cheat_tab = "quest"
                g_cheat_quest_filter = key
            elif kind == "gallery":
                g_cheat_tab = "gallery"
                g_cheat_gallery_key = key
            elif kind == "item":
                g_cheat_tab = "item"
                g_cheat_item_search = key
                Cheat_SearchItem(key)
            elif kind == "room":
                g_cheat_tab = "room"
            elif kind == "var":
                g_cheat_tab = "vars"
                g_cheat_var_filter = key
        except Exception:
            pass
        g_cheat_global_results = list()

# ---------- \u4efb\u52a1\u6807\u7b7e\u9875 ----------
## ============================================================
## 标签7: 任务管理
## ============================================================
screen cheat_tab_quest():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_11"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                # ---- 任务系统 ----
                use cm_card("任务系统"):

                    hbox:
                        spacing 8
                        textbutton "清空已完成" style "cmt_action" action Function(Cheat_QuestClearAllDone)
                        textbutton "完成全部未完成" style "cmt_action" action Function(Cheat_QuestDoneAll)

                    hbox:
                        spacing 6
                        text "搜索:" style "cmt_label" yalign 0.5
                        frame:
                            background "#1B2029"
                            padding (8, 4)
                            xsize 200
                            input:
                                copypaste True
                                value VariableInputValue("g_cheat_quest_filter")
                                length 20
                                xfill True
                                style "cmt_input"
                        text "当前任务数: [len(g_InventoryQuest)]" style "cmt_body" yalign 0.5

                # ---- 任务列表 ----
                for qk in Cheat_QuestQuestFilter(g_cheat_quest_filter):
                    frame:
                        style "cmt_row"
                        vbox:
                            spacing 3
                            hbox:
                                spacing 8
                                xfill True
                                vbox:
                                    spacing 1
                                    text "[Cheat_QuestNameCN(qk)]" style "cmt_row_name"
                                    text "[qk] - 状态: [Cheat_QuestStatusText(Cheat_QuestStatus(qk))]" style "cmt_row_id"
                                null xfill True
                                hbox:
                                    spacing 3
                                    yalign 0.5
                                    textbutton "开始" style "cmt_mini" action Function(Cheat_QuestStart, qk)
                                    textbutton "一键完成" style "cmt_mini" action Function(Cheat_QuestForceDone, qk)
                                    textbutton "移除" style "cmt_mini" action Function(Cheat_QuestRemove, qk)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_11")


## ============================================================
## 标签8: 每日限制
## ============================================================
screen cheat_tab_daily():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_12"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                use cm_card("每日限制"):

                    text "[Cheat_DailySummary()]" style "cmt_body"

                    hbox:
                        spacing 6
                        textbutton "清空全部每日限制" style "cmt_action" action Function(Cheat_ClearAllDaily)
                        textbutton "仅清每日标记" style "cmt_action" action Function(Cheat_ResetDailyOnly)
                        textbutton "解锁全部角色" style "cmt_action" action Function(Cheat_UnlockAllActors)

                use cm_card("每日标志列表（前60条）"):

                    for k in list(gd_DailyFlag.keys())[:60]:
                        hbox:
                            spacing 6
                            text "[k]" style "cmt_row_name"
                            text "[str(gd_DailyFlag[k])]" style "cmt_row_id"

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_12")


## ============================================================
## 标签9: 图鉴
## ============================================================
screen cheat_tab_gallery():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_13"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                use cm_card("图鉴收集"):

                    text "[Cheat_GalleryInfo()]" style "cmt_body"

                    hbox:
                        spacing 6
                        textbutton "全部解锁" style "cmt_action" action Function(Cheat_GalleryUnlockAll)

                    hbox:
                        spacing 6
                        text "手动 key:" style "cmt_label" yalign 0.5
                        frame:
                            background "#1B2029"
                            padding (8, 4)
                            xsize 180
                            input:
                                copypaste True
                                value VariableInputValue("g_cheat_gallery_key")
                                length 20
                                xfill True
                                style "cmt_input"
                        textbutton "加图片" style "cmt_mini" action Function(Cheat_ManualCollect, "picture", g_cheat_gallery_key)
                        textbutton "加书籍" style "cmt_mini" action Function(Cheat_ManualCollect, "book", g_cheat_gallery_key)
                        textbutton "加贴纸" style "cmt_mini" action Function(Cheat_ManualCollect, "sticker", g_cheat_gallery_key)
                        textbutton "加音乐" style "cmt_mini" action Function(Cheat_ManualCollect, "lpmusic", g_cheat_gallery_key)
                        textbutton "加卡片" style "cmt_mini" action Function(Cheat_ManualCollect, "card", g_cheat_gallery_key)
                        textbutton "加日记" style "cmt_mini" action Function(Cheat_ManualCollect, "diary", g_cheat_gallery_key)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_13")


## ============================================================
## 标签10: 房间/地牢
## ============================================================
screen cheat_tab_room():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_14"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                use cm_card("房间管理"):

                    text "今日已打开: [Cheat_RoomOpenCount()] 个" style "cmt_body"

                    hbox:
                        spacing 6
                        textbutton "重置全部房间" style "cmt_action" action Function(Cheat_ResetAllRooms)

                    for rk in Cheat_RoomList():
                        hbox:
                            spacing 8
                            xfill True
                            text "[Cheat_RoomNameCN(rk)] ([rk])" style "cmt_row_name"
                            null xfill True
                            hbox:
                                spacing 3
                                yalign 0.5
                                textbutton "打开" style "cmt_mini" action Function(Cheat_OpenRoom, rk)
                                textbutton "关闭" style "cmt_mini" action Function(Cheat_CloseRoom, rk)

                use cm_card("地牢"):

                    text "[Cheat_DungeonStatus()]" style "cmt_body"

                    hbox:
                        spacing 6
                        textbutton "初始化地牢" style "cmt_action" action Function(Cheat_DungeonInit)
                        textbutton "退出地牢" style "cmt_action" action Function(Cheat_DungeonExit)
                        textbutton "杀死全部敌人" style "cmt_action" action Function(Cheat_DungeonKillAll)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_14")


## ============================================================
## 标签11: 全局变量
## ============================================================
screen cheat_tab_vars():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_15"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                use cm_card("全局变量编辑器"):

                    text "覆盖角色专属故事变量与存档持久化数据（g_/gd_/q_ 前缀）" style "cmt_body"

                    hbox:
                        spacing 6
                        text "过滤:" style "cmt_label" yalign 0.5
                        frame:
                            background "#1B2029"
                            padding (8, 4)
                            xsize 200
                            input:
                                copypaste True
                                value VariableInputValue("g_cheat_var_filter")
                                length 20
                                xfill True
                                style "cmt_input"

                for vname in Cheat_VarsList(g_cheat_var_filter):
                    frame:
                        style "cmt_row"
                        hbox:
                            spacing 8
                            xfill True
                            vbox:
                                spacing 1
                                text "[vname]" style "cmt_row_name"
                                text "[Cheat_VarDisplay(vname)]" style "cmt_row_id"
                            null xfill True
                            hbox:
                                spacing 3
                                yalign 0.5
                                frame:
                                    background "#1B2029"
                                    padding (8, 4)
                                    xsize 130
                                    input:
                                        copypaste True
                                        value VariableInputValue("g_cheat_var_value")
                                        length 14
                                        xfill True
                                        style "cmt_input"
                                textbutton "保存" style "cmt_mini" action Function(Cheat_VarSet, vname, g_cheat_var_value)

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_15")


## ============================================================
## 标签12: 存档快照
## ============================================================
screen cheat_tab_snapshot():
    style_prefix "cmt"

    side "c r":
        viewport:
            id "cm_vp_16"
            mousewheel True
            draggable True
            xfill True
            yfill True

            vbox:
                spacing _cm_gap

                use cm_card("存档快照"):

                    text "风险操作前建议先快照，快照为独立档位，不影响正常存档" style "cmt_body"

                    hbox:
                        spacing 6
                        textbutton "快照存档" style "cmt_action" action Function(Cheat_SnapshotSave)
                        textbutton "自动存档" style "cmt_action" action Function(Cheat_AutoSave)

                    text "快照列表:" style "cmt_card_title"

                    for slot in Cheat_SavedList():
                        hbox:
                            spacing 6
                            text "[slot]" style "cmt_row_name"

        vbar:
            style "cmt_vbar"
            value YScrollValue("cm_vp_16")


## ============================================================
## 防回归：style 常量引用完整性静态校验（C1）
## 任何 style 块引用了未定义的 _cm_*/_cheat_* 常量，init 阶段即报错，
## 避免再出现 "lint 绿但游戏启动即崩" 的回归路径。
## ============================================================
init python:
    def _cheat_verify_style_tokens():
        import os as _os
        import re as _re
        _path = _os.path.join(config.gamedir, "script", "ActorScript", "cheat_menu.rpy")
        if not _os.path.exists(_path):
            return
        _src = open(_path, encoding="utf-8").read()
        _defined = set(_re.findall(r'(?m)^\s*(_cm_[A-Za-z0-9_]+|_cheat_[A-Za-z0-9_]+)\s*=', _src))

        _defined |= set(_re.findall(r'(?m)^\s*def\s+(_cm_[A-Za-z0-9_]+|_cheat_[A-Za-z0-9_]+)\s*\(', _src))
        _missing = set()
        for _m in _re.finditer(r'(?m)^style\s+\S+:\n((?:(?:[ \t]+[^\r\n]*)?\n)+)', _src):
            _body = _m.group(1)
            for _tok in _re.findall(r'(?<![A-Za-z0-9_])(_cm_[A-Za-z0-9_]+|_cheat_[A-Za-z0-9_]+)', _body):
                if _tok not in _defined:
                    _missing.add(_tok)
        if _missing:
            renpy.display.log.write("[cheat_menu] WARNING: style 引用了未定义常量: %s" % ", ".join(sorted(_missing)))

    _cheat_verify_style_tokens()

