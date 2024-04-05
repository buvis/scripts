$target = $args[0]

if (Test-Path $target) {
    rm -r -fo $target
}
