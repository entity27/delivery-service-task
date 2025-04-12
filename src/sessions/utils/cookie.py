from typing import Annotated

from fastapi import Depends, Response


class SessionCookieManager:
    """
    Взаимодействие с cookie сессии
    """

    _key = 'session'

    def set_cookie(self, response: Response, token: str) -> None:
        """
        Устанавливает cookie для response'а

        Notes:
            Не устанавливаем secure, поскольку является учебным примером.
            Устанавливаем httponly, чтобы cookie не были доступны для JS'а
            Устанавливаем 'strict', чтобы сессия могла быть отправлена только нашему API

        """
        response.set_cookie(
            key=self._key,
            value=token,
            path='/',
            httponly=True,
            samesite='strict',
        )


SessionCookieManagerDep = Annotated[SessionCookieManager, Depends()]
