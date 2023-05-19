from servertesting import *


def test_get_stable_mc_versions(verbose: bool = False) -> bool:
    responses_stable = get_mc_versions()
    responses_unstable = get_mc_versions(allow_snapshots=True)

    if verbose:
        print(f'test_get_mc_versions,stable: {responses_stable=}')
        print(f'test_get_mc_versions,unstable: {responses_unstable=}')

    return bool(responses_stable and responses_unstable)


def test_get_loader_versions(mc_versions: str, verbose: bool = False) -> bool:
    response_stable = get_loader_versions(mc_versions)
    response_unstable = get_loader_versions(mc_versions, allow_unstable=True)

    if verbose:
        print(f'test_get_loader_versions,stable: {response_stable=}')
        print(f'test_get_loader_versions,unstable: {response_unstable=}')

    return bool(response_stable)


def test_get_installer_versions(verbose: bool = False) -> bool:
    response_stable = get_installer_versions()
    response_unstable = get_installer_versions(allow_unstable=True)

    if verbose:
        print(f'test_get_installer_versions,stable: {response_stable=}')
        print(f'test_get_installer_versions,unstable: {response_unstable=}')

    return bool(response_stable)


def test_get_server_jar(mc_versions: str, loader_version: str, installer_version: str, verbose: bool = False):
    response = get_server_jar(mc_versions, loader_version, installer_version)

    if verbose:
        print(f'test_get_server_jar: {response[0:20]=}')

    return bool(response)


def test_get_latest_server_jar(verbose: bool = False):
    response = get_latest_server_jar('/dev/null')

    if verbose:
        print(f'test_get_latest_server_jar: {response[0:20]=}')

    return bool(response)


def test(verbose: bool) -> bool:
    mc_version: str = '1.19.4'
    loader_version: str = '0.14.19'
    installer_version: str = '0.11.2'

    result: bool = bool(
        test_get_stable_mc_versions(verbose=verbose)
        and test_get_loader_versions(mc_version, verbose=verbose)
        and test_get_installer_versions(verbose=verbose)
        and test_get_server_jar(mc_version, loader_version, installer_version, verbose=verbose)
        and test_get_latest_server_jar(verbose=verbose)
    )

    print(f'Test result was {result}')
    return result


if __name__ == '__main__':
    test(verbose=True)
