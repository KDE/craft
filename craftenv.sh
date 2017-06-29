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
    craftRoot=$(dirname $(realpath "$craftRoot"))
fi

export craftRoot

CRAFT_ENV=($(python3.6 "$craftRoot/bin/CraftSetupHelper.py" --setup))

for line in "${CRAFT_ENV[@]}"; do
  if [[ "$line"  =~ "=" ]];then
    export $line || true
  fi
done

cd "$KDEROOT"
