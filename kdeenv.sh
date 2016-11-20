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

EMERGE_ENV=($(python3.5 "$craftRoot/bin/CraftSetupHelper.py" --setup --mode bash))

for line in "${EMERGE_ENV[@]}"; do
  if [[ "$line"  =~ "=" ]];then
    export $line
  fi
done

cd "$KDEROOT"
