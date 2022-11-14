from typing import TypeAlias
from os import environ
from json import loads

from pydantic import BaseModel
from requests import get

from settings.settings import environment_variable_name

blocked_ips: TypeAlias = list[str]
blocked_domains: TypeAlias = list[str]


def check_environ_is_item_loaded(environ_variables: list[environment_variable_name], var_name: environment_variable_name):
    if var_name not in environ_variables:
        raise ValueError(f'You must define {var_name} in environ variables')


def get_data_from_url(var_name: environment_variable_name) -> list:
    request = get(environ[var_name])
    if request.status_code != 200:
        raise RuntimeError(f'Can\'t download data from {environ[var_name]}')
    return loads(request.text)


# for snapshot(daily) monitoring
class AuthorityItem(BaseModel):
    id: int
    name: str


class BlockedItem(BaseModel):
    authority: AuthorityItem
    domains: list[str]
    id: int
    ips: list[str]
    status: str
    urls: list[str]


class SnapshotBlocked(BaseModel):
    item: BlockedItem
    last_updated: str | None


def download_snapshot() -> list[SnapshotBlocked]:
    raise NotImplementedError


# for ip list monitoring
def download_blocked_ips(environ_variables: list[environment_variable_name]) -> blocked_ips:
    param_name = 'rkn_ip_black'
    check_environ_is_item_loaded(environ_variables, param_name)
    return get_data_from_url(param_name)


# for domain list monitoring
def download_blocked_domains(environ_variables: list[environment_variable_name]) -> blocked_domains:
    param_name = 'rkn_domains_black'
    check_environ_is_item_loaded(environ_variables, param_name)
    return get_data_from_url(param_name)
