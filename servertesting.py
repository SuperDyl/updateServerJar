#!/usr/bin/python3
import requests
from typing import List, Dict, Optional

FABRIC_API = 'https://meta.fabricmc.net/v2'
GAME_VERSIONS = f'{FABRIC_API}/versions/game'


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


def test_get_stable_mc_versions(verbose: bool = False) -> bool:
    responses_stable = get_mc_versions()
    responses_unstable = get_mc_versions(allow_snapshots=True)

    if verbose:
        print(f'test_get_mc_versions: {responses_stable=}')
        print(f'test_get_mc_versions: {responses_unstable=}')

    return bool(responses_stable and responses_unstable)


def get_server_jar(mc_version: str) -> Optional[str]:
    server_jar = f'{FABRIC_API}/versions/loader/{mc_version}/server'
    response = requests.get(server_jar)
    if response.status_code != 200:
        return None
    json_data = response.json()
    return json_data['downloads']['server']['url']


def test_get_server_jar(mc_versions: str, verbose: bool = False):
    response = get_server_jar(mc_versions)

    if verbose:
        print(f'test_get_server_jar: {response=}')

    return bool(response)


def test(verbose: bool) -> bool:
    result: bool = bool(
        test_get_stable_mc_versions(verbose=verbose)
        and test_get_server_jar('1.19.4', verbose=verbose)
    )

    print(f'Test result was {result}')
    return result


test(verbose=True)
