



init python:
    def CloseSubMenuAction(): 
        HideRoom()


label end_say_d:
    $ restoreSayActorType()
    if g_say_actor_type == "actor":
        $ LockActorToday(g_say_actor)
    elif g_say_actor_type == "action":
        $ LockActionToday(g_say_actor)
    jump end_say

label end_say_t:
    $ restoreSayActorType()
    if g_say_actor_type == "actor":
        $ LockActorTime(g_say_actor)
    elif g_say_actor_type == "action":
        $ LockActionTime(g_say_actor)
    jump end_say

label end_say_r:
    $ restoreSayActorType()
    if g_say_actor_type == "actor":
        $ RemoveActorTime(g_say_actor)

    jump end_say

label end_say:
    scene black
    $ StopSexVoice()
    $ g_action_lock = False

    $ UpdateWorldMapActors(g_mylocationKey)
    $ ResetMusic()

    hide screen screen_otaku_money
    jump room_page

screen null_screen():
    text ""

screen null_screen_return():
    button:
        xsize 1920 ysize 1080
        action Return()


screen close_screen_delay(screen_name):
    text ""


screen home_ui_system_button():
    zorder 103
    $ actor = GetActor("e")

    key "h" action NullAction()

    if g_cheat_open:
        use cheat_menu_main

    vbox:
        xalign 1.0 yalign 0.0
        button:
            xsize 127 ysize 127
            action Function( SelectScreen ,screenName = "setupmenu")
            if g_selectScreen == "setupmenu":
                style "frame_paper_red"
                add "icon_menu" zoom 0.4 xalign 0.5 yalign 0.5
            else:
                style "frame_paper_alpha_red_hover"
                add "icon_menu" zoom 0.4 xalign 0.5 yalign 0.5 alpha 0.7

            text "ᆞᆞᆞᆞᆞ" size 12 xpos 33 ypos 31 color "#333333" font "arial.ttf" bold True

            $ version = config.version.split('.')
            text Bitcord(config.version.split('.')[1]) size 12 xpos 33 ypos 53 color "#333333" font "arial.ttf" bold True


            text Bitcord(config.version.split('.')[2]) size 12 xpos 33 ypos 74 color "#333333" font "arial.ttf" bold True

        ## 内置修改器按钮
        button:
            xsize 127 ysize 127
            action Function( Cheat_OpenClose )
            if g_cheat_open:
                style "frame_paper_red"
            else:
                style "frame_paper_alpha_red_hover"
            add "icon_menu" zoom 0.4 xalign 0.5 yalign 0.5 alpha 0.7
            text "CHEAT" size 12 xpos 20 ypos 55 color "#e94560" font "arial.ttf" bold True

        if g_menu_close == 0:
            button:
                xsize 127 ysize 127
                action Function( SelectScreen ,screenName = "Screen_InventoryQuest")
                if g_selectScreen == "Screen_InventoryQuest":
                    style "frame_paper_red"
                    add "icon_menu_quest" zoom 0.4 xalign 0.5 yalign 0.5
                else:
                    style "frame_paper_alpha_red_hover"
                    add "icon_menu_quest" zoom 0.4 xalign 0.5 yalign 0.5 alpha 0.7

            button:
                xsize 127 ysize 127

                if g_inventoryHide == 1:
                    add "icon_menu_bag" zoom 0.5 xalign 0.5 yalign 0.5 alpha 0.7

                if g_call == 1 and not renpy.get_screen("Screen_InventoryItem"):
                    action Function(BagMenuCall)



                    style "frame_paper_alpha_red_hover"
                    add "icon_menu_phone_call" zoom 0.4 xalign 0.5 yalign 0.5 at bell_phone


















                elif g_phoneHide == 0:
                    action Function( SelectScreen , screenName = "Screen_InventoryItem")

                    if g_selectScreen == "Screen_InventoryItem":
                        style "frame_paper_red"
                        add "icon_menu_bag" zoom 0.4 xalign 0.5 yalign 0.5
                    else:
                        style "frame_paper_alpha_red_hover"
                        add "icon_menu_bag" zoom 0.4 xalign 0.5 yalign 0.5 alpha 0.7


            button:
                xsize 127 ysize 127
                action Function( SelectScreen , screenName = "Screen_InventoryStatus")

                if g_selectScreen == "Screen_InventoryStatus":
                    style "frame_paper_red"
                    if actor.GetCoom() == 6:
                        add actor.GetCoomIcon() zoom 0.4 xalign 0.5 yalign 0.5 at blink_smooth_alpha(0.5,1,0,0.1)
                    else:
                        add actor.GetCoomIcon() zoom 0.4 xalign 0.5 yalign 0.5 at force_alpha(1.0)
                else:
                    style "frame_paper_alpha_red_hover"
                    if actor.GetCoom() == 6:
                        add actor.GetCoomIcon() zoom 0.4 xalign 0.5 yalign 0.5 at blink_smooth_alpha(0.5,1,0,0.1)
                    else:
                        add actor.GetCoomIcon() zoom 0.4 xalign 0.5 yalign 0.5 at force_alpha(0.7)

                if g_EquipSlotHaveEmpty:
                    add 'noti_red_dot' zoom 0.7 yalign 0.05 xalign 0.95































init python:

    def SelectScreenReset():
        global g_selectScreen
        renpy.hide_screen("Screen_InventoryItem")
        renpy.hide_screen("Screen_InventoryQuest")
        renpy.hide_screen("Screen_InventoryPhone")
        renpy.hide_screen("Screen_InventoryStatus")
        renpy.hide_screen("setupmenu")
        renpy.hide_screen("cheat_menu_main")
        
        HideEquipmentChangeWindow()
        
        
        
        
        
        
        
        
        
        g_selectScreen = ""
        
        SetMissionRestList()

    def SelectScreen( screenName ):
        global g_selectScreen
        
        renpy.sound.play( "audio/effect/puzzle_clear.wav")
        
        
        
        if renpy.get_screen(screenName):
            SelectScreenReset()
            renpy.hide_screen(screenName)
        else:
            SelectScreenReset()
            g_selectScreen = screenName
            renpy.show_screen(screenName)


screen action_button_green(name, icon, func_type, func, active, delay):
    button:
        xsize 200 ysize 290
        if active:
            style "frame_green_mini_round_alpha_hover"
            at action_card_in(delay*0.08)
        else:
            style "frame_white_mini_round_alpha_lock"
        add icon zoom 0.7 xalign 0.5 yalign 0.3
        text name size 35 color "#FFFFFF" yalign 0.95 xalign 0.5
        if active:
            if func_type == "toggle":
                action ToggleVariable(func)
            elif func_type == "jump":
                action Jump(func)
            elif func_type == "function":
                action Function(func)

screen action_button_red(name, icon, func_type, func, active, delay):
    button:
        xsize 200 ysize 290
        if active:
            style "frame_red_mini_round_alpha_hover"
            at action_card_in(delay*0.08)
        else:
            style "frame_white_mini_round_alpha_lock"
        add icon zoom 0.7 xalign 0.5 yalign 0.3
        text name size 35 color "#FFFFFF" yalign 0.95 xalign 0.5
        if active:
            if func_type == "toggle":
                action ToggleVariable(func)
            elif func_type == "jump":
                action Jump(func)
            elif func_type == "function":
                action Function(func)

screen exit_screen_icon(icon, type, name, value=None):
    zorder 101
    hbox:
        yalign 1.0
        hbox:
            xpos 20 ypos -10
            spacing 15
            button:
                xsize 160 ysize 178
                style "frame_middle_shadow"
                at exit_card_in()
                if type == "end_say":
                    key "mousedown_6" action Function(exit_screen, name)
                elif type == "return":
                    key "mousedown_6" action [Hide(name), Return()]
                elif type == "function_return":
                    key "mousedown_6" action [Function(name), Return()]
                elif type == "function":
                    key "mousedown_6" action Function(name)
                elif type == "hide":
                    key "mousedown_6" action Hide(name)
                elif type == "jump":
                    key "mousedown_6" action Jump(name)
                elif type == "action":
                    key "mousedown_6" action name

                button:
                    xsize 150 ysize 168
                    add AlphaMask(Transform(Crop((800,200, 375 , 668), RoomData(g_mylocationKey).RoomImage()), zoom = 0.4), "frame_back_mask")
                    frame:
                        xsize 150 ysize 168
                        style "frame_back"
                    add icon zoom 0.5 xalign 0.5 yalign 0.5
                    if type == "end_say":
                        action Function(exit_screen, name)
                    elif type == "return":
                        action [Hide(name), Return()]
                    elif type == "function_return":
                        action [Function(name), Return()]
                    elif type == "function":
                        if value:
                            action Function(name, value)
                        else:
                            action Function(name)
                    elif type == "hide":
                        action Hide(name)
                    elif type == "jump":
                        action Jump(name)

                    elif type == "action":
                        action name


screen exit_screen(name, type="hide"):
    use exit_screen_icon("icon_back", type, name)


screen ExitButton(label_name):
    zorder 101
    hbox:
        yalign 1.0
        hbox:
            xpos 20 ypos -20
            spacing 15
            button:
                xsize 150 ysize 270
                style "frame_blink"
                add RoomData(g_mylocationKey).RoomImage() zoom 0.4 crop (800,200, 375 , 668)
                frame:
                    xsize 150 ysize 270
                    style "frame_back"
                at move_out_card_in(0.1)
                text _("그만하기") size 30 color "#000000" hover_color "#FFFFFF" yalign 0.97 xalign 0.5

                action [Hide("ExitButton"), Jump(label_name)]
                key "mousedown_6" action [Hide("ExitButton"), Jump(label_name)]
return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
