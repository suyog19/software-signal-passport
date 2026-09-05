# Development dependency decisions

The distributed Passport is Markdown and has no runtime dependencies. The
maintainer checks use Python's standard library and Markdownlint CLI2. GitHub
Actions also runs the separately pinned canonical engineering process.

## Identity, purpose and licensing

| Dependency | Purpose / source | Identity and license basis |
| --- | --- | --- |
| Python 3.14 Alpine 3.23 | Standard-library checks; official `docker.io/library/python` | Base digest in checks.Dockerfile; Python PSF license, OS packages retain their own licenses |
| Markdownlint CLI2 0.23.2 | Markdown syntax/style; `docker.io/davidanson/markdownlint-cli2` | Base digest and OCI source metadata; upstream MIT license |
| Alpine security patches | libuuid 2.41.6-r0 and OpenSSL libraries 3.5.8-r0 | Official Alpine HTTPS URLs, SHA-256 content checks and signed APK installation; upstream package licenses |
| Software Engineering Process 1.4.1 | Configuration and assurance policy | Immutable Git revision in process.lock; Apache-2.0 |

These licenses describe dependencies, not a relicensing of the whole base image.
The release ships no image, library binary, package manager, or copied dependency
source. Base image digests and patch hashes are fixed in
[checks.Dockerfile](../.github/checks.Dockerfile); no floating package resolution
runs during validation.

## Security findings and remediation

Initial dependency scanning found material vulnerabilities in the older
Markdownlint 0.20 image's parser dependencies, including linkify-it and js-yaml.
The 0.23.2 image updates those libraries. Its remaining scanned findings were in
unused npm tooling and older OS OpenSSL libraries, so the development recipe
removes npm and applies the vendor's exact library updates.

Python checks require no package installation. The Python recipe removes pip
and ensurepip, including their unused vendored dependencies, and updates libuuid.
This avoids shipping known vulnerable installer code into the validation
environment without adding a package-manager runtime requirement.

Validate the resulting images with a current vulnerability database before release,
for example Docker Scout's critical/high scan. Preserve failed reports and the
remediation evidence outside source. A clean scan only covers the scanner's
database and selected severity; it is not proof that an image has no vulnerabilities.

Both targets run as a non-root user, with network disabled, read-only checkout and
root filesystem, dropped capabilities, no privilege escalation and resource limits.
Image retrieval and fixed APK downloads are build transport; executed build steps
have network disabled. No GitHub token or Docker socket enters the check containers.

The recipe targets Linux amd64, matching the configured CI runner. Native
standard-library checks remain available on other platforms. Pinned vendor files
can disappear; a failed download must prompt a reviewed dependency update, never
checksum removal or an unverified fallback.
