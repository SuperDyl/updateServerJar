#!/usr/bin/python3
from typing import List, Dict

import requests

FABRIC_API = 'https://meta.fabricmc.net/v2'
GAME_VERSIONS = f'{FABRIC_API}/versions/game'
INSTALLER_VERSIONS = f'{FABRIC_API}/versions/installer'


def get_mc_versions(allow_snapshots: bool = False) -> List[str]:
    response = requests.get(GAME_VERSIONS)
    if response.status_code != 200:
        return []

    json_data: List[Dict] = response.json()
    return [
        item['version']
        for item in json_data
        if (allow_snapshots or item['stable'])
    ]


def get_loader_versions(mc_version: str, allow_unstable: bool = False) -> List[str]:
    loader_versions = f'{FABRIC_API}/versions/loader/{mc_version}'
    response = requests.get(loader_versions)
    if response.status_code != 200:
        return []

    json_data: List[Dict] = response.json()
    return [
        item['loader']['version']
        for item in json_data
        if (allow_unstable or item['loader']['stable'])
    ]


def get_installer_versions(allow_unstable: bool = False) -> List[str]:
    response = requests.get(INSTALLER_VERSIONS)
    if response.status_code != 200:
        return []

    json_data: List[Dict] = response.json()
    return [
        item['version']
        for item in json_data
        if (allow_unstable or item['stable'])
    ]


def get_server_jar(mc_version: str, loader_version: str, installer_version: str) -> bytes:
    # /v2/versions/loader/:game_version/:loader_version/:installer_version/server/jar
    server_jar = f'{FABRIC_API}/versions/loader/{mc_version}/{loader_version}/{installer_version}/server/jar'
    response = requests.get(server_jar)
    if response.status_code != 200:
        raise Exception('Failed to get server jar!')

    return response.content


def get_latest_server_jar(allow_snapshots: bool = False):
    try:
        mc_version = get_mc_versions(allow_snapshots=allow_snapshots)[0]
        loader_version = get_loader_versions(mc_version)[0]
        installer_version = get_installer_versions()[0]
    except Exception:
        raise Exception('Failed to get a version number from meta.fabricmc.net')
    return get_server_jar(mc_version, loader_version, installer_version)


if __name__ == '__main__':
    get_latest_server_jar()
