# auto prefix tailwind classes

    Usage: tailwind-class-prefixer [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --version             -v                                       Show the application's version and exit.              │
    │ --help                                                         Show this message and exit.                           │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ prefix         Process an existing project.                                                                          │
    │ update         Update the tailwind class list from official sources.                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ prefix-Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────╮
    │   path        [PATH]    Path to project root. [default: None]                                                        │
    │   prefix      [PREFIX]  Change the prefix for tailwind classes. [default: tw-] - explicit *empty* removes a prefix   │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


## TODO: support media Queries:

    foobar:sm
    ->
    foobar:tw-sm

## TODO: support vue class bindings inside paranthesis:

    <div :class="{ active: isActive }"></div>
    -> 
    <div :class="{ tw-active: isActive }"></div>


## to clear all prefixes (this is hacky..)

    python .\prefix.py prefix <path> "*empty*"
