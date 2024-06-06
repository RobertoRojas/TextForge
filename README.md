![TextForge](.github\img\imagen.webp)

# TextForge

TextForge is a Bazel module designed to generate files from a list of templates and a set of data in JSON format, which can be provided as a string or a file. TextForge uses Jinja2 to render the data into the templates, producing an output with the applied changes.

## How to use it

To define the dependency in MODULE.bazel, follow these steps:

Locate the MODULE.bazel file: This file is typically found at the root of your Bazel workspace.

Specify the dependency: Use the bazel_dep function to add the dependency. The syntax is as follows:

```Bazel
bazel_dep(name = "textforge", version = "1.0.0")
```

After adding the dependency to your MODULE.bazel file, you can load the rule into your BUILD.bazel file. Example:

```Bazel
load("@textforge//:defs.bzl", "generate_files")


generate_files(
...
)
```

### Rule attributes

| Name | Description |
|:-:|:-:|
| srcs | The templates files |
| data | The data on a string with JSON format |
| datafile | The path of the JSON file with the data |
| prefix | Prefix to add to the output files |
| suffix | Suffix to add to the output files |
| extension | Extension for the output files |

## Example

_templates/templateA.txt.jinja_
```Jinja2
Template A value: {{ a }}
```
_templates/templateB.txt.jinja_
```Jinja2
Template B value: {{ b }}
```
_templates/templateC.txt.jinja_
```Jinja2
Template C value: {{ c }}
```

_data/data.json_
```JSON
{
    "a": 123,
    "b": 456,
    "c": 789
}
```

_BUILD.bazel_
```Bazel
load("@textforge//:defs.bzl", "generate_files")

filegroup(
    name = "templates",
    srcs = glob([
        "templates/*.jinja",
    ]),
    visibility = ["//visibility:private"],
)

generate_files(
    name = "files",
    srcs = [
        ":templates"
    ],
    datafile = "data/data.json",
    visibility = ["//visibility:public"],
)
```

### Generated content

_bazel-bin/templateA.txt_
```Plain
Template A value: 123
```

_bazel-bin/templateB.txt_
```Plain
Template B value: 456
```

_bazel-bin/templateC.txt_
```Plain
Template C value: 789
```

### License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](https://github.com/RobertoRojas/TextForgeTool/blob/main/LICENSE) file for details.

### Authors

- [Roberto Rojas](https://github.com/RobertoRojas)