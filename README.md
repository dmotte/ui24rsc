# ui24rsc

![device](device.png)

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dmotte/ui24rsc/release?logo=github&style=flat-square)](https://github.com/dmotte/ui24rsc/actions)
[![PyPI](https://img.shields.io/pypi/v/ui24rsc?logo=python&style=flat-square)](https://pypi.org/project/ui24rsc/)

**Ui24R** **S**napshot **C**onverter.

new way to ui24r snapshots as code. the Soundcraft JSON format is very hard to understand and so manually editing snapshots from code is uncomfortable

This script lets you convert snapshots exported from the mixer Web UI from the Soundcraft JSON format to other more human-readable formats

Tested with firmware version: 3.3.8293-ui24

TODO overview of all possible actions

input/output supported formats: JSON, YAML

Example commands:

- `ui24rsc --help`
- `ui24rsc diff,tree in.json out.yml`
- `ui24rsc dots,full in.yml out.json`

TODO sections: installation, development

```bash
ui24rsc tree,sort default-init.json default-init.yml
diff <(jq --sort-keys < default-init.json) <(ui24rsc dots default-init.yml | jq --sort-keys)

diff <(jq --sort-keys < snapshot01.json) <(ui24rsc dots,full snapshot01.yml | jq --sort-keys)
```

TODO pip3 install -e . --user This will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment (https://stackoverflow.com/a/35064498)
