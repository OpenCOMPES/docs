import json
import sys

if len(sys.argv) != 4:
    sys.exit("Usage: update_switcher.py json_file GITHUB_REF VERSION")

switcher_file = sys.argv[1]
branch = sys.argv[2]
version = sys.argv[3]

present = False
with open(switcher_file, encoding="utf-8") as f:
    data = json.load(f)
    if branch.startswith("refs/tags"):  # add a new version tag
        version_tag = branch.split("/")[-1]
        prerelease = "a" in version_tag
        for item in data:
            if version_tag in item.get("name", ""):
                present = True
            if "latest" in item.get("name", ""):
                item["version"] = version
                item["url"] = "https://opencompes.github.io/docs/sed/" + version_tag
            if "stable" in item.get("name", "") and not prerelease:
                item["version"] = version
                item["url"] = "https://opencompes.github.io/docs/sed/" + version_tag
        if not present:
            new_entry = {}
            new_entry["name"] = version_tag
            new_entry["version"] = version
            new_entry["url"] = "https://opencompes.github.io/docs/sed/" + version_tag
            data.append(new_entry)

    elif branch == "refs/heads/main":  # update latest
        for item in data:
            if "latest" in item.get("name", ""):
                item["version"] = version
                present = True
                break
        if not present:
            new_entry = {}
            new_entry["name"] = "latest"
            new_entry["version"] = version
            new_entry["url"] = "https://opencompes.github.io/docs/sed/latest"
            data.append(new_entry)

    else:  # update develop
        for item in data:
            if "develop" in item.get("name", ""):
                present = True
                item["version"] = version
                break
        if not present:
            new_entry = {}
            new_entry["name"] = "develop"
            new_entry["version"] = version
            new_entry["url"] = "https://opencompes.github.io/docs/sed/develop"
            data.append(new_entry)

    print(data)

    with open(switcher_file, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
