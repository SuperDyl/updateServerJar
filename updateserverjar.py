#!/usr/bin/python3
from typing import List, Dict
import sys
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


def get_latest_server_jar(file_name: str, allow_snapshots: bool = False) -> bytes:
    mc_versions = get_mc_versions(allow_snapshots=allow_snapshots)
    if not mc_versions:
        raise Exception('No Minecraft versions available')
    mc_version = mc_versions[0]

    loader_versions = get_loader_versions(mc_version)
    if not loader_versions:
        raise Exception('No loader versions available')
    loader_version = loader_versions[0]

    installer_versions = get_installer_versions()
    if not installer_versions:
        raise Exception('No installer versions available')
    installer_version = installer_versions[0]

    server_jar: bytes = get_server_jar(mc_version, loader_version, installer_version)

    if file_name == '-':
        sys.stdout.buffer.write(server_jar)
    else:
        with open(file_name, 'wb') as file:
            file.write(server_jar)

    return server_jar


if __name__ == '__main__':
    file_name: str = sys.argv[1] if len(sys.argv) > 1 else '-'
    get_latest_server_jar(file_name)
