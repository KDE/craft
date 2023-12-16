craftRoot="${BASH_SOURCE[0]}"
if [[ -z "$craftRoot" ]];then
    craftRoot="$0"
fi
if [[ -z "$craftRoot" ]];then
    craftRoot="$_"
fi
if [[ -z "$craftRoot" ]];then
    echo "Failed to determine interpreter"
    exit 1
fi

if [ -n "$CRAFT_PYTHON_BIN" ]; then
    echo "Using user-provided CRAFT_PYTHON_BIN: $CRAFT_PYTHON_BIN";
elif command -v python3.7 >/dev/null; then
    CRAFT_PYTHON_BIN=$(command -v python3.7)
elif command -v python3.6 >/dev/null; then
    CRAFT_PYTHON_BIN=$(command -v python3.6)
else
    # could not find python 3.6, try python3
    if ! command -v python3 >/dev/null; then
        echo "Failed to python Python 3.6+"
        exit 1
    fi
    # check if python3 is at least version 3.6:
    python_version=$(python3 --version)
    # sort -V knows how to compare version numbers
    # Note: this is just a sanity check. craft.py should check sys.version
    comparison=$(printf '%s\nPython 3.6.0\n' "$python_version" | sort -V)
    if [ "$(echo "${comparison}" | head -n1)" != "Python 3.6.0" ]; then
        echo "Found Python3 version ${python_version} is too old. Need at least 3.6"
        exit 1
    fi
    CRAFT_PYTHON_BIN=$(command -v python3)
fi
export CRAFT_PYTHON_BIN

if [[ ! -d "$craftRoot" ]]; then
    craftRoot=$(${CRAFT_PYTHON_BIN} -c "import os; import sys; print(os.path.dirname(os.path.abspath(sys.argv[1])));" "$craftRoot")
fi

export craftRoot


while read -r -d '' env_var; do
    # environment variable keys may not contain =, therefore parsing is relatively easy
    key="$(cut -d= -f1 <<<"$env_var")"
    value="$(cut -d= -f2- <<<"$env_var")"
    export "$key"="$value"
done < <("${CRAFT_PYTHON_BIN}" "$craftRoot/bin/CraftSetupHelper.py" --setup --format null)

if [[ -n "$PS1" ]]; then
    export PS1="CRAFT: $PS1"
fi


craft() {
    local python="$KDEROOT/dev-utils/bin/python3"
    if [[ ! -f "$python" ]]; then
      local python=${CRAFT_PYTHON_BIN}
    fi
    ${python} "$craftRoot/bin/craft.py" "$@"
}

cs() {
    if ! dir="$(craft -q --ci-mode --get "sourceDir()" "$1")"; then
        echo "$dir"
    else
        cd "$dir" || exit 2
    fi
}

cb() {
    if ! dir="$(craft -q --ci-mode --get "buildDir()" "$1")"; then
        echo "$dir"
    else
        cd "$dir" || exit 2
    fi
}

cr() {
    cd "$KDEROOT" || exit 2
}

cr

declare -x -F cs cb cr
