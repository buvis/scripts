# Config Migration Guide

Scripts have been migrated to use `buvis-pybase>=0.9.0` with Pydantic-based settings.

## New Config Location

Old: `src/{tool}/config.yaml` or `~/.config/{tool}/config.yml`
New: `~/.config/buvis/buvis-{tool}.yaml`

## Migration Steps

### hello_world
No config file needed (uses defaults).

### pinger
```yaml
# ~/.config/buvis/buvis-pinger.yaml
host: "192.168.1.1"
wait_timeout: 300
```

### zseq
```yaml
# ~/.config/buvis/buvis-zseq.yaml
path_dir: "/path/to/photos"
is_reporting_misnamed: true
```

### muc
```yaml
# ~/.config/buvis/buvis-muc.yaml
limit_flac_bitrate: 1411000
limit_flac_bit_depth: 16
limit_flac_sampling_rate: 44100
tidy_junk_extensions:
  - ".cue"
  - ".db"
```

### bim
```yaml
# ~/.config/buvis/buvis-bim.yaml
path_zettelkasten: "~/bim/zettelkasten/"
```

For `bim sync` command, jira_adapter config goes in global buvis config:
```yaml
# ~/.config/buvis/buvis.yaml
jira_adapter:
  url: "https://jira.example.com"
  # ... other jira settings
```

### fctracker
```yaml
# ~/.config/buvis/buvis-fctracker.yaml
transactions_dir: "~/finance/transactions"
local_currency:
  code: "CZK"
  symbol: "Kč"
  precision: 2
foreign_currencies:
  USD:
    symbol: "$"
    precision: 2
  EUR:
    symbol: "€"
    precision: 2
```

### outlookctl, dot, readerctl
No config files needed (minimal/no settings).

## Environment Variables

All settings can be overridden via env vars with prefix `BUVIS_{TOOL}_`:
```bash
BUVIS_PINGER_HOST=10.0.0.1 pinger wait
BUVIS_FCTRACKER_TRANSACTIONS_DIR=~/data fctracker balance
```

## Precedence

CLI args > ENV vars > YAML config > defaults
