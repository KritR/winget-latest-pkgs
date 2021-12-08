from pathlib import Path
from packaging.version import parse as parse_version
import yaml
import json

all_packages = Path('./winget-pkgs/manifests').rglob('*.en-US.yaml')

package_map = dict()

OUTPUT_FILE = "out/packages.json"


for filepath in all_packages:
    with open(filepath, 'r') as file:
        pkg = yaml.safe_load(file)
    pkg_id = pkg['PackageIdentifier']
    if pkg_id in package_map:
        old_pkg = package_map[pkg_id]
        old_pkg_ver = str(old_pkg['PackageVersion'])
        pkg_ver = str(pkg['PackageVersion'])
        if parse_version(pkg_ver) > parse_version(old_pkg_ver):
            package_map[pkg_id] = pkg
    else:
        package_map[pkg_id] = pkg

latest_packages = list(package_map.values())


def sanitize_packages(pkgs):
    for pkg in pkgs:
        pkg['PackageVersion'] = str(pkg['PackageVersion'])
        if 'Tags' in pkg:
            pkg['Tags'] = [str(tag) for tag in pkg['Tags']]


sanitize_packages(latest_packages)

with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(list(package_map.values()), outfile)
