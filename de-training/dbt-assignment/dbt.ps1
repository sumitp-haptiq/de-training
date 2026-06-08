# Run dbt with project-local profiles (.dbt/profiles.yml)
$env:DBT_PROFILES_DIR = Join-Path $PSScriptRoot ".dbt"
& dbt @args
