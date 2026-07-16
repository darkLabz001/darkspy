# DarkSpy - Hacker OSINT Intelligence Suite

Email & Domain Intelligence Gathering Tool

## Features

### Domain Reconnaissance
- **Bing Search** - Search for leaked emails on Bing
- **PGP Keys** - Lookup emails from public PGP key servers
- **Certificate Transparency** - Search crt.sh for SSL cert emails
- **DNS Recon** - Enumerate DNS/MX/SPF/NS records
- **GitHub Search** - Find emails in public GitHub code
- **Hunter.io** - Domain email pattern discovery
- **Subdomain Bruteforce** - 90+ prefix subdomain enumeration

### Email Intelligence
- **Shodan Lookup** - Get email server info from Shodan
- **SMTP Verify** - Verify email existence via SMTP
- **Social Enumeration** - Gravatar, GitHub, Keybase, LinkedIn
- **Breach Check** - EmailRep, HIBP, Holehe breach lookup
- **Header Analysis** - Parse .eml files (SPF/DKIM/DMARC, IPs, routing)

### Output
- JSON export (`-o`)
- CSV export (`-c`)
- Custom output directory (`-O`)

### Network
- Tor/SOCKS proxy support (`-T`)
- Session-based HTTP with retries
- Modern User-Agent rotation

## Installation

```bash
git clone https://github.com/darkLabz001/darkspy.git
cd darkspy
python3 -m venv .venv
source .venv/bin/activate
pip install requests dnspython
```

### Global Install (optional)

```bash
ln -sf ~/tools/darkspy/darkspy.py ~/.local/bin/darkspy
```

## Usage

### Interactive TUI (no args)
```bash
darkspy
```

### CLI Flags
```bash
darkspy -t site.com -s all          # Search all sources for domain
darkspy -t site.com -s bing        # Search Bing only
darkspy -t site.com -d             # Enumerate subdomains
darkspy -i user@site.com           # Shodan email info
darkspy -v user@site.com           # SMTP verify
darkspy -p user@site.com           # Social media enum
darkspy -b user@site.com           # Breach check
darkspy -H path/to/email.eml       # Analyze email header
```

### Options
| Flag | Description |
|------|-------------|
| `-t`, `--target` | Domain to search |
| `-s`, `--source` | Source: all, bing, pgp, crtsh, dns, github, hunter, subs |
| `-d`, `--subdomains` | Enumerate subdomains |
| `-i`, `--info` | Email Shodan lookup |
| `-v`, `--verify` | SMTP verify email |
| `-p`, `--social` | Social media enum |
| `-b`, `--breach` | Breach/leak check |
| `-H`, `--header` | Analyze .eml header |
| `-o`, `--json` | Export to JSON |
| `-c`, `--csv` | Export to CSV |
| `-O`, `--output` | Output directory |
| `-T`, `--tor` | Route through Tor |
| `-h`, `--help` | Show help |

## License

MIT
