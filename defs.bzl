load("@bazel_skylib//lib:paths.bzl", "paths")

def _gen_files(ctx):
    filepaths = []
    outputs = []
    tmp = []
    args = ctx.actions.args()
    for file in ctx.files.srcs:
        filepaths.append(file.path)
        filename = paths.basename(file.path)
        if filename.endswith(".j2"):
            filename = paths.replace_extension(filename, "")
        elif filename.endswith(".jinja"):
            filename = paths.replace_extension(filename, "")
        root, ext = paths.split_extension(filename)
        if ctx.attr.extension:
            ext = ctx.attr.extension
        filename = "{}{}{}{}".format(ctx.attr.prefix, root,
                                     ctx.attr.suffix, ext)
        outputs.append(ctx.actions.declare_file(filename))
    args.add_all(filepaths)# template.txt.jinja --out-dir bazel-out/k8-fastbuild/bin --data '{"a":1234}' --prefix pre- --suffix -suf --extension .changed
    args.add_all(["--out-dir", "bazel-out/k8-fastbuild/bin"])
    if ctx.attr.data:
        if ctx.attr.datafile:
            fail("Cannot set 'data and 'datafile' together")
        args.add("--data={}".format(ctx.attr.data))
    elif ctx.attr.datafile:
        if ctx.attr.data:
            fail("Cannot set 'data' and 'datafile' together")
        args.add("--data-path={}".format(ctx.file.datafile.path))
    else:
        fail("One of 'data' or 'datafile' must be set")
    if ctx.attr.prefix:
        args.add("--prefix={}".format(ctx.attr.prefix))
    if ctx.attr.suffix:
        args.add("--suffix={}".format(ctx.attr.suffix))
    if ctx.attr.extension:
        args.add("--extension={}".format(ctx.attr.extension))
    ctx.actions.run(
        outputs = outputs,
        inputs = ctx.files.srcs + ([ctx.file.datafile] if ctx.attr.datafile else []),
        arguments = [args],
        executable = ctx.executable._textforge,
    )
    return DefaultInfo(files = depset(outputs))

generate_files = rule(
    implementation = _gen_files,
    attrs = {
        "srcs": attr.label_list(allow_files = True, mandatory = True),
        "data": attr.string(),
        "datafile": attr.label(allow_single_file = True),
        "prefix": attr.string(default = ""),
        "suffix": attr.string(default = ""),
        "extension": attr.string(default = ""),
        "_textforge": attr.label(
            default = "//:textforge",
            executable = True,
            cfg = "host",
        ),
    },
)