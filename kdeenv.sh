emergeRoot="${BASH_SOURCE[0]}"
if [[ -z "$emergeRoot" ]];then
    emergeRoot="$0"
fi
if [[ -z "$emergeRoot" ]];then
    emergeRoot="$_"
fi
if [[ -z "$emergeRoot" ]];then
    echo "Failed to determine interpreter"
    exit 1
fi

if [[ ! -d "$emergeRoot" ]]; then
    emergeRoot=$(dirname $(realpath "$emergeRoot"))
fi

EMERGE_ENV=($(python3.5 "$emergeRoot/bin/EmergeSetupHelper.py" --setup --mode bash))

for line in "${EMERGE_ENV[@]}"; do
  if [[ "$line"  =~ "=" ]];then
    export $line
  fi
done

cd "$KDEROOT"
