# Update FabricMC Server Jar

Used to update the FabricMC JAR for a Minecraft server

# Setup

This project requires the `requests` library:

```
python3 -m pip install requests
```

It has been tested to in Python3.8, but it may not work in other Python versions

# Usage (Command line)

```
python3 -m updateserver [server_filename | '-'] [mc_version | '']
```

Run the `updateserverjar.py` file and save to the file `server.jar`

```
python3 -m updateserverjar server.jar
```

The JAR can instead be piped to stdout by using `-` as the filename

```
python3 -m updateserverjar - > server.jar
```

# Usage (Module)

Documentation is included with the code (so it stays up to date).

Generally:

`get_mc_versions()`, `get_loader_versions()`, and `get_installer_versions` each return a list of version numbers.

`get_server_jar()` gets the server_jar for the specified versions provided

`get_mc_version_server_jar()` gets the latest server_jar for the specified Minecraft version

`get_latest_server_jar()` gets the most recent jar

# Testing

The provided `updateserverjartests` can be used to test the code. Just run the code:

```
python3 -m updateserverjartests
```

It should print out output similar to this:

```
test_get_mc_versions,stable: responses_stable=['1.19.4', '1.19.3', '1.19.2', '1.19.1', '1.19', '1.18.2', '1.18.1', '1.18', '1.17.1', '1.17', '1.16.5', '1.16.4', '1.16.3', '1.16.2', '1.16.1', '1.16', '1.15.2', '1.15.1', '1.15', '1.14.4', '1.14.3', '1.14.2', '1.14.1', '1.14']
test_get_mc_versions,unstable: responses_unstable[0:LIMIT]=['1.20-pre4', '1.20-pre3', '1.20-pre2', '1.20-pre1', '23w18a', '23w17a', '23w16a', '23w14a', '23w13a_or_b', '23w13a_or_b_original', '23w13a', '23w12a', '1.19.4', '1.19.4-rc3', '1.19.4-rc2', '1.19.4-rc1', '1.19.4-pre4', '1.19.4-pre3', '1.19.4-pre2', '1.19.4-pre1']
test_get_loader_versions,stable: response_stable=['0.14.19']
test_get_loader_versions,unstable: response_unstable[0:LIMIT]=['0.14.19', '0.14.18', '0.14.17', '0.14.16', '0.14.15', '0.14.14', '0.14.13', '0.14.12', '0.14.11', '0.14.10', '0.14.9', '0.14.8', '0.14.7', '0.14.6', '0.14.5', '0.14.4', '0.14.3', '0.14.2', '0.14.1', '0.14.0']
test_get_installer_versions,stable: response_stable=['0.11.2']
test_get_installer_versions,unstable: response_unstable[0:LIMIT]=['0.11.2', '0.11.1', '0.11.0', '0.10.2', '0.10.1', '0.10.0', '0.9.1', '0.9.0', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.6.1.51', '0.6.1.50', '0.6.1.49', '0.6.1.48']
test_get_server_jar: response[0:LIMIT]=b'PK\x03\x04\n\x00\x00\x08\x08\x00\xaaIaV\x00\x00\x00\x00\x02\x00'
test_get_mc_version_server_jar: response[0:LIMIT]=b'PK\x03\x04\n\x00\x00\x08\x08\x00\xaaIaV\x00\x00\x00\x00\x02\x00'
test_get_latest_server_jar: response[0:LIMIT]=b'PK\x03\x04\n\x00\x00\x08\x08\x00\xaaIaV\x00\x00\x00\x00\x02\x00'
Test result was True
```

You can tell all tests passed because the output will end with `Test result was True`
instead of `Test result was False` or `Test result was Exception`

# Missing features and bugs

* There is no testing for file downloading or command line arguments
* If a test fails, all subsequent tests are skipped
* No command line option to have a non-verbose test run
