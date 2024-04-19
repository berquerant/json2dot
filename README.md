# json2dot

```
❯ python -m json2dot.cli -h
usage: json2dot [-h] [--penwidth_min PENWIDTH_MIN] [--penwidth_max PENWIDTH_MAX] [--arrowsize_min ARROWSIZE_MIN] [--arrowsize_max ARROWSIZE_MAX] [--weight_min WEIGHT_MIN] [--weight_max WEIGHT_MAX]
                [--fontsize_min FONTSIZE_MIN] [--fontsize_max FONTSIZE_MAX] [--display_selfloop] [--name_key NAME_KEY] [--group_key GROUP_KEY] [--out OUT] [--debug] [--version]

Generate dot source from jsonl considering node degrees and edge weights.

Load edges from stdin, format:

  {"src": NODE, "dst": NODE}

src is head, dst is tail.
NODE fomat:

  {"id": NODE_ID, "other_key": OTHER_VALUE, ...}

NODE_ID is string. Other keys are optional node descriptions.
No need to give descriptions to all nodes, descriptions of nodes with the same NODE_ID are merged.

options:
  -h, --help            show this help message and exit
  --penwidth_min PENWIDTH_MIN
                        Default: 1
  --penwidth_max PENWIDTH_MAX
                        Default: 5
  --arrowsize_min ARROWSIZE_MIN
                        Default: 1
  --arrowsize_max ARROWSIZE_MAX
                        Default: 2
  --weight_min WEIGHT_MIN
                        Default: 1
  --weight_max WEIGHT_MAX
                        Default: 100
  --fontsize_min FONTSIZE_MIN
                        Default: 8
  --fontsize_max FONTSIZE_MAX
                        Default: 48
  --display_selfloop, -s
  --name_key NAME_KEY, -k NAME_KEY
                        select node name from node desc
  --group_key GROUP_KEY, -g GROUP_KEY
                        select group name from node desc
  --out OUT, -o OUT     filename for saving the rendered image
  --debug
  --version             print version
```

# Example

Generate an example image from [source](tests/test.json).

```
pipenv sync
pipenv shell
make tmp/debug.svg
```
