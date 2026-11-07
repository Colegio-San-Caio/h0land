# fakzu snap - Launchpad xenial builder failure

## Summary
All xenial arch builds (s390x, ppc64el, arm64, armhf) fail at infra step, before source download. No cURL/CHECKSUM issue.

## Logs
- s390x: 880772320
- ppc64el: 880772524
- arm64: 880772346
- armhf: 880772506

## Verified Checksums (s390x log)
SHA256: 5b35c47516499f82bc23dd85d4146c8b04b9e4dd06141fc73d379817893f234
MD5: 66ecd534dc947e0b04d56e07c950583

## Error
error: cannot communicate with server: dial unix /run/snapd.socket: no such file or directory
snap set system proxy.http=http://10.10.10.1:8222/ failed

## cURL / CHECKSUM Analysis
zcat fakzu_build.log.gz | grep -i curl -> only libcurl3-gnutls 7.47.0-1ubuntu2.19
No source-checksum mismatch, died before fetch.
