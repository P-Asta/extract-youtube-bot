from nextcord import *
from nextcord.ext import commands as cmds
import os
import play2048 as p_2048
import json
from typing import Coroutine, Union, Optional  
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("TOKEN")
CLIENT = Client()


CUSTOM = p_2048.customs.ORIGINAL.value

@CLIENT.slash_command(description = "2048을 플레이합니다", name = "2048")
async def play2048(inter: Interaction):
    _2048 = p_2048.Game()
    views = [
        Play2048(disabled = True), Play2048(label = "w", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, custom_id="up", type=type), Play2048(disabled = True), Play2048(label = "end", style = ButtonStyle.red, user = inter.user, _2048 = _2048, custom_id="end", type=type),
        Play2048(label = "a", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="left", type=type), Play2048(label = "s", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="down", type=type), Play2048(label = "d", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="right", type=type), Play2048(disabled = True, row = 2)
    ]
    await inter.response.send_message(f"점수: **0점**", file = File(_2048.encodingImage(CUSTOM).image_bytes, f"point_0.png"), view = Play2048s(views, _2048, inter))
    
class Play2048s(ui.View):
    def __init__(self , comps: list[ui.Button], _2048: p_2048.Game, inter: Union[Interaction, cmds.context.Context]):
        super().__init__(timeout = 300)
        for comp in comps:
            self.add_item(comp)
        self.inter = inter
        self._2048 = _2048

    async def on_timeout(self) -> None:
        self.inter.message.edit(view = None)

class Play2048(ui.Button):
    def __init__(self, *, type: str = "img", user: Member = None, _2048: p_2048.Game = None, style:ButtonStyle = ButtonStyle.secondary, label: Optional[str] = "ㅤ", disabled: bool = False, custom_id: Optional[str] = None, url: Optional[str] = None, emoji: Optional[Union[str, Emoji, PartialEmoji]] = None, row: Optional[int] = None):
        if user != None:
            super().__init__(style = style, label = label, disabled = disabled, custom_id = f"{custom_id}|{user.id}", url = url, emoji = emoji, row = row)
        else:
            super().__init__(style = style, label = label, disabled = disabled, custom_id = custom_id, url = url, emoji = emoji, row = row)
        self.__2048 = _2048
        
    async def callback(self, inter: Interaction):
        if self.custom_id.split("|")[1] != str(inter.user.id): return await inter.response.send_message("자신의것을 사용하세요!", ephemeral = True)
        await inter.response.defer()
        movement = 0
        if self.custom_id.startswith("up"):    movement  = p_2048.move.UP
        if self.custom_id.startswith("down"):  movement  = p_2048.move.DOWN
        if self.custom_id.startswith("left"):  movement  = p_2048.move.LEFT
        if self.custom_id.startswith("right"): movement  = p_2048.move.RIGHT
        
        if movement != 0:
            self.__2048.move(movement)
            img = File(self.__2048.encodingImage(CUSTOM).image_bytes, f"point_{self.__2048.point}.png")
        
            await inter.message.edit(f"점수: **{self.__2048.point}점**", file = img)
                
                

        if self.custom_id.startswith("end"):
            await inter.message.edit(view = None)



if __name__ == "__main__":
    CLIENT.run(TOKEN)