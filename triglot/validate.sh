#!/usr/bin/env bash
set -eo pipefail

wrong() {
  printf "EXTREMELY LOUD INCORRECT BUZZER!!!\n"
}
trap wrong ERR

code=$(cat)
echo 'perl'
printf '%s' "$code" | perl -c

echo 'py'
printf '%s' "$code" | python3 -c 'import sys,ast; ast.parse(sys.stdin.read())'
echo 'js'
printf '%s' "$code" | node -e "const fs=require('fs'), src=fs.readFileSync(0,'utf8'); require('vm').createScript(src)"

perl_out=$(printf '%s' "$code" | perl -)
py_out=$(printf '%s' "$code" | python3 -)
js_out=$(printf '%s' "$code" | node -)

if [[ "$perl_out" == "$py_out" && "$perl_out" == "$js_out" ]]; then
  printf "Your triglot compiles!! Here's your output:\n"
  printf '%s\n' "$perl_out"
else
  exit 1
fi
