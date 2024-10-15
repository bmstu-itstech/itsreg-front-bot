from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    uuid: str = "Bot's UUID",
    entry_key: str = "Mailing's entry key",
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/bots/{uuid}/mailings/{entry_key}/start".format(
            uuid=uuid,
            entry_key=entry_key,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Error.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str = "Bot's UUID",
    entry_key: str = "Mailing's entry key",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """Начать рассылку с бота данным UUID и ключом entryKey.

    Args:
        uuid (str):  Default: "Bot's UUID".
        entry_key (str):  Default: "Mailing's entry key".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        entry_key=entry_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str = "Bot's UUID",
    entry_key: str = "Mailing's entry key",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """Начать рассылку с бота данным UUID и ключом entryKey.

    Args:
        uuid (str):  Default: "Bot's UUID".
        entry_key (str):  Default: "Mailing's entry key".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        uuid=uuid,
        entry_key=entry_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str = "Bot's UUID",
    entry_key: str = "Mailing's entry key",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """Начать рассылку с бота данным UUID и ключом entryKey.

    Args:
        uuid (str):  Default: "Bot's UUID".
        entry_key (str):  Default: "Mailing's entry key".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        entry_key=entry_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str = "Bot's UUID",
    entry_key: str = "Mailing's entry key",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """Начать рассылку с бота данным UUID и ключом entryKey.

    Args:
        uuid (str):  Default: "Bot's UUID".
        entry_key (str):  Default: "Mailing's entry key".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            entry_key=entry_key,
            client=client,
        )
    ).parsed
