from typing import TypeAlias, TypedDict

Doamin: TypeAlias = str
IPLocation: TypeAlias = str
class IPDict(TypedDict):
    domains: list[Doamin]
    ips: dict[IPLocation, list[Doamin]]
