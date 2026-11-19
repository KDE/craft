
# Determine the script root
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

check_python_version() {
    "$1" -c "import sys; from pathlib import Path; p = Path(sys.base_prefix).resolve(); sys.exit(sys.version_info < (3, 11) or any((d / 'etc/CraftSettings.ini').exists() for d in (p, *p.parents)))" >/dev/null 2>&1
}

# Python detection
if [ -n "$CRAFT_PYTHON_BIN" ]; then
    if check_python_version "$CRAFT_PYTHON_BIN"; then
        echo "Using user-provided CRAFT_PYTHON_BIN: $CRAFT_PYTHON_BIN"
    else
        echo "User-provided Python ($CRAFT_PYTHON_BIN) must be a system Python >= 3.11, not one built by Craft"
        exit 1
    fi
else
    # Preferred Python versions, newest first
    for py in "$(dirname "$craftRoot")/../etc/virtualenv/craft/bin/python3" python3 $(ls -1 ${PATH//:/\/python3.* }/python3.* 2>/dev/null | sort -V -r); do
        if check_python_version "$py"; then
            CRAFT_PYTHON_BIN="$(command -v "$py")"
            break
        fi
    done

    if [ -z "$CRAFT_PYTHON_BIN" ]; then
        echo "Failed to find a system Python >= 3.11"
        exit 1
    fi

    echo "Using Python: $("$CRAFT_PYTHON_BIN" --version)"
fi

export CRAFT_PYTHON_BIN

# Determine craftRoot directory if it's a file
if [[ ! -d "$craftRoot" ]]; then
    craftRoot=$(${CRAFT_PYTHON_BIN} -c "import os; import sys; print(os.path.dirname(os.path.abspath(sys.argv[1])));" "$craftRoot")
fi

export craftRoot

# Load environment variables from CraftSetupHelper.py
while read -r -d '' env_var; do
    # environment variable keys may not contain =, therefore parsing is relatively easy
    key="$(cut -d= -f1 <<<"$env_var")"
    value="$(cut -d= -f2- <<<"$env_var")"
    export "$key"="$value"
done < <("${CRAFT_PYTHON_BIN}" "$craftRoot/bin/CraftSetupHelper.py" --setup --format null)

# Prefix prompt if interactive
if [[ -n "$PS1" ]]; then
    export PS1="CRAFT: $PS1"
fi

# Helper functions for craft
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
