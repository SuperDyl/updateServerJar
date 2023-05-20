#!/usr/bin/python3
from typing import List, Dict
import sys
import requests

FABRIC_API = 'https://meta.fabricmc.net/v2'
GAME_VERSIONS = f'{FABRIC_API}/versions/game'
INSTALLER_VERSIONS = f'{FABRIC_API}/versions/installer'


def get_mc_versions(allow_snapshots: bool = False) -> List[str]:
    """
    Gets Minecraft versions supported by FabricMC
    :param allow_snapshots: When set to True, snapshot versions are included in the list
    :return: all current Minecraft versions supported by FabricMC, sorted from most recent to oldest
    """
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
    """
    Gets FabricMC Loader versions
    :param mc_version: Minecraft version you need the loader for
    :param allow_unstable: Adds unstable/untested loader versions to the output
    :return: All FabricMC Loader versions for the specified Minecraft version
    """
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
    """
    Gets FabricMC Installer versions
    :param allow_unstable: Adds unstable installer versions to the output
    :return: All FabricMC installer versions
    """
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
    """
    Collects the bytes for the server jar of the specified version choices
    :param mc_version:
    :param loader_version:
    :param installer_version:
    :return: bytes of the specified FabricMC server jar
    """
    # /v2/versions/loader/:game_version/:loader_version/:installer_version/server/jar
    server_jar = f'{FABRIC_API}/versions/loader/{mc_version}/{loader_version}/{installer_version}/server/jar'
    response = requests.get(server_jar)
    if response.status_code != 200:
        raise Exception('Failed to get server jar!')

    return response.content


def get_mc_version_server_jar(mc_version: str) -> bytes:
    """
    Returns the bytes for the most recent server jar for the specified version of Minecraft.
    :param mc_version: Minecraft version to use for the server jar
    :return: bytes of the most recent FabricMC server jar for the Minecraft version
    """
    loader_versions = get_loader_versions(mc_version)
    if not loader_versions:
        raise Exception(f'No loader versions available for {mc_version=}')
    loader_version = loader_versions[0]

    installer_versions = get_installer_versions()
    if not installer_versions:
        raise Exception(f'No installer versions available for {mc_version=}')
    installer_version = installer_versions[0]

    return get_server_jar(mc_version, loader_version, installer_version)


def get_latest_server_jar(allow_snapshots: bool = False) -> bytes:
    """
    Returns the bytes for the most recent server jar for FabricMC
    :param allow_snapshots: If True, the most recent experimental version or snapshot will be collected
    :return: bytes of the most recent FabricMC server jar
    """
    mc_versions = get_mc_versions(allow_snapshots=allow_snapshots)
    if not mc_versions:
        raise Exception('No Minecraft versions available')
    mc_version = mc_versions[0]
    return get_mc_version_server_jar(mc_version)


if __name__ == '__main__':
    def print_usage():
        print("Usage: python3 -m updateserverjar [file_name | '-' | '-h' | '--help'] [minecraft_version | '']")
        print("\tfile_name: name to save the jar as")
        print("\t'-': outputs the file bytes to stdout instead of a file (so it can be piped using '>' or '|'")
        print("\t'-h' OR '--help': prints this usage guide")
        print("\tIf minecraft_version is omitted, the latest is used instead")


    if len(sys.argv) <= 1:
        print_usage()
        sys.exit()

    output_file: str = sys.argv[1]
    if output_file in ('-h', '--help'):
        print_usage()
        sys.exit()

    file_bytes: bytes

    if len(sys.argv) > 2:
        minecraft_version: str = sys.argv[2]
        file_bytes = get_mc_version_server_jar(minecraft_version)
    else:
        file_bytes = get_latest_server_jar()

    if output_file == '-':
        sys.stdout.buffer.write(file_bytes)
    else:
        with open(output_file, 'wb') as file:
            file.write(file_bytes)
