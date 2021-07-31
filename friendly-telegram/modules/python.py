#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import traceback
import sys
import itertools
import types
from meval import meval

import telethon

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class PythonMod(loader.Module):
    """Python stuff"""
    strings = {"name": "Python",
               "evaluated": "<b>Выполненное выражение:</b>\n<code>{}</code>\n<b>Возвращено:</b>\n<code>{}</code>",
               "evaluate_fail": ("<code>eval:</code> <b>Не удалось выполнить выражение:</b>\n<code>{}</code>"
                                 "\n\n<b>Ошибка:</b>\n<code>{}</code>"),
               "execute_fail": ("<code>exec:</code> <b>Не удалось выполнить выражение:</b>\n<code>{}</code>"
                                "\n\n<b>Ошибка:</b>\n<code>{}</code>"),
               "n_protect": "НОМЕР_СКРЫТ"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.owner
    async def evalcmd(self, message):
        """.eval <выражение>
           Выполняет выражение Python"""
        ret = self.strings("evaluated", message)
        try:
            it = await meval(utils.get_args_raw(message), globals(), **await self.getattrs(message))
        except Exception:
            exc = sys.exc_info()
            exc = "".join(traceback.format_exception(exc[0], exc[1], exc[2].tb_next.tb_next.tb_next))
            await utils.answer(message, self.strings("evaluate_fail", message)
                               .format(utils.escape_html(utils.get_args_raw(message)), utils.escape_html(exc)))
            return
        ret = ret.format(utils.escape_html(utils.get_args_raw(message)), utils.escape_html(it))
        await utils.answer(message, ret)

    @loader.owner
    async def execcmd(self, message):
        """.exec <код>
           Выполняет код Python"""
        try:
            await meval(utils.get_args_raw(message), globals(), **await self.getattrs(message))
        except Exception:
            exc = sys.exc_info()
            exc = "".join(traceback.format_exception(exc[0], exc[1], exc[2].tb_next.tb_next.tb_next))
            await utils.answer(message, self.strings("execute_fail", message)
                               .format(utils.escape_html(utils.get_args_raw(message)), utils.escape_html(exc)))
            return

    async def getattrs(self, message):
        return {"message": message, "client": self.client, "self": self, "db": self.db,
                "reply": await message.get_reply_message(), **self.get_types(), **self.get_functions()}

    def get_types(self):
        return self.get_sub(telethon.tl.types)

    def get_functions(self):
        return self.get_sub(telethon.tl.functions)

    def get_sub(self, it, _depth=1):
        """Получить все вызываемые объекты с большой буквы в объекте рекурсивно, игнорируя _ *"""
        return {**dict(filter(lambda x: x[0][0] != "_" and x[0][0].upper() == x[0][0] and callable(x[1]),
                              it.__dict__.items())),
                **dict(itertools.chain.from_iterable([self.get_sub(y[1], _depth + 1).items() for y in
                                                      filter(lambda x: x[0][0] != "_"
                                                             and isinstance(x[1], types.ModuleType)
                                                             and x[1] != it
                                                             and x[1].__package__.rsplit(".", _depth)[0]
                                                             == "telethon.tl",
                                                             it.__dict__.items())]))}
