import json
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: update_switcher.py json_file GITHUB_REF")

switcher_file = sys.argv[1]
branch = sys.argv[2]

present = False
with open(switcher_file, encoding="utf-8") as f:
    data = json.load(f)
    if branch.startswith("refs/tags"):  # add a new version tag
        version = branch.split("/")[-1]
        for item in data:
            if version in item.get("name", ""):
                present = True
            if "stable" in item.get("name", ""):
                item["version"] = version[1:]
                item["url"] = "https://opencompes.github.io/docs/sed/" + version
        if not present:
            new_entry = {}
            new_entry["name"] = version
            new_entry["version"] = version[1:]
            new_entry["url"] = "https://opencompes.github.io/docs/sed/" + version
            data.append(new_entry)

    elif branch == "refs/heads/main":  # update latest
        for item in data:
            if "latest" in item.get("name", ""):
                present = True
                break
        if not present:
            new_entry = {}
            new_entry["name"] = "latest"
            new_entry["url"] = "https://opencompes.github.io/docs/sed/latest"
            data.append(new_entry)

    else:  # update develop
        for item in data:
            if "develop" in item.get("name", ""):
                present = True
                item["version"] = branch.split("/")[-1]
                break
        if not present:
            new_entry = {}
            new_entry["name"] = "develop"
            new_entry["version"] = branch.split("/")[-1]
            new_entry["url"] = "https://opencompes.github.io/docs/sed/develop"
            data.append(new_entry)

    print(data)

    with open(switcher_file, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
