> **⚠️ This package is no longer being maintained.**
> `ckit` has been renamed to **[justx](https://github.com/fpgmaas/justx)** and now leverages [just](https://github.com/casey/just)'s justfiles instead of custom YAML syntax.


<p align="center">
  <h1>ckit</h1>
</p>


_ckit_ is a command line utility to help you organise and quickly run frequently used commands.



## Quickstart

### Installation

_ckit_ can be installed by running

```shell
pip install ckit
```

To get started, run

```shell
ckit init
```

which will prompt to add a `ckit/ckit.yaml` file in the user's home directory for global commands, and/or a `ckit.yaml` file in the current directory for commands specific to the current project. 

To use _ckit_ to run any of the pre-configured commands, simply run

```
ckit
```

For more information, see the [documentation](https://fpgmaas.github.io/ckit/).

## Configuration

_ckit_ can look for configuration in the following two locations:

- In a `ckit.yaml` file in the current directory
- In any `.yaml` file in the the global configuration directory, which is defaulted to `~/ckit`, but which can be overridden with the environment variable `ckit_HOME`.

An example `.yaml` file could look as follows:

```yaml
test:
  my-command:
    cmd: "echo Hello! My name is: $name. My favourite fruit is: $fruit"
    echo: false
    args:
      - name
      - fruit: apple
```

Which adds the command group `test` wth a single command called `my-command`. When `my-command` is selected to be run, _ckit_ prompts the user for `name` and `fruit` before running the command specified in `cmd`, where `fruit` is defaulted to `apple` if the user does not give any input.

For more details, see the [configuration](https://fpgmaas.github.io/ckit/configuration) section of the documentation.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
