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

if [[ ! -d "$craftRoot" ]]; then
    craftRoot=$(dirname $craftRoot)
fi

export craftRoot

CRAFT_ENV=($(python3.6 "$craftRoot/bin/CraftSetupHelper.py" --setup))

for line in "${CRAFT_ENV[@]}"; do
  if [[ "$line"  =~ "=" ]] && [[ $line != _=* ]];then
    export $line || true
  fi
done

cs() {
    dir=$($craftRoot/bin/craft -q --ci-mode --get "sourceDir()" $1)
    if (($? > 0));then
        echo $dir
    else
        cd "$dir"
    fi
}

cb() {
    dir=$($craftRoot/bin/craft -q --ci-mode --get "buildDir()" $1)
    if (($? > 0));then
        echo $dir
    else
        cd "$dir"
    fi
}

cr() {
    cd "$KDEROOT"
}

cr

declare -x -F cs cb cr
