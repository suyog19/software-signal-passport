# Development-only validation images; no product runtime is distributed.
FROM python:3.14-alpine3.23@sha256:8caa2adfeb414dfe68d8b257f7aea9e205a400521c2b13b2d2e5e731fb8e70e5 AS python-checks
ADD --checksum=sha256:d0f0693edbe2164125fbbd71401bf52d2d1ef00a83d26b7775673ab39f591bfe https://dl-cdn.alpinelinux.org/alpine/v3.23/main/x86_64/libuuid-2.41.6-r0.apk /tmp/libuuid.apk
RUN apk add --no-network /tmp/libuuid.apk
# These checks use only the standard library. Remove unused installers and their
# vulnerable vendored dependencies rather than keep unreachable package tooling.
RUN python -c "import pathlib,shutil; roots=[pathlib.Path('/usr/local/lib/python3.14/ensurepip'),*pathlib.Path('/usr/local/lib/python3.14/site-packages').glob('pip*')]; [shutil.rmtree(p) for p in roots if p.is_dir()]"
USER 65534:65534
ENTRYPOINT ["python"]

FROM davidanson/markdownlint-cli2:v0.23.2@sha256:839558fd0d36c46da0e01ea84fd1d20a2822b5a8a60c16dc9708f0bb7c9e903b AS markdown-checks
USER root
# Exact vendor patches. ADD verifies immutable content; package installation runs
# without network and checks signatures using the image's Alpine keyring.
ADD --checksum=sha256:161223a16f042b8e469e9441291e071464fd91d4f4bbe6f496ee8d0abd4e0701 https://dl-cdn.alpinelinux.org/alpine/v3.24/main/x86_64/libcrypto3-3.5.8-r0.apk /tmp/libcrypto3.apk
ADD --checksum=sha256:aca521e5ae4a321322a9d47ed64a1775f5ab1ffd215d1e9fc0433c58f7bfd037 https://dl-cdn.alpinelinux.org/alpine/v3.24/main/x86_64/libssl3-3.5.8-r0.apk /tmp/libssl3.apk
RUN apk add --no-network /tmp/libcrypto3.apk /tmp/libssl3.apk
# Invoke the installed linter directly; npm and its dependency tree are not used.
RUN node -e "require('node:fs').rmSync('/usr/local/lib/node_modules/npm',{recursive:true,force:true})"
USER 65534:65534
