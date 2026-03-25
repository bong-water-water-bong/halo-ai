#!/bin/bash
# Halo AI Banner — source this file to display the colored banner
# Usage: source /srv/ai/assets/banner.sh

CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Read version from VERSION file, default to 1.0.0
HALO_VERSION="1.0.0"
for _vpath in /srv/ai/VERSION "$(dirname "${BASH_SOURCE[0]}")/../VERSION"; do
    if [ -f "$_vpath" ]; then
        HALO_VERSION="$(cat "$_vpath")"
        break
    fi
done
unset _vpath

echo ''
echo -e "${BOLD}${CYAN}"
cat << 'EOF'
            .=============.
           //  .: ✦ :.  \\
          ||               ||
           \\  ': ✦ :'  //
            '============='
                || ||
           ╔════╧══╧════╗
           ║  █▀█  ▀█▀  ║
           ║  █▀█   █   ║
           ║  █ █  ▄█▄  ║
           ╚════════════╝
EOF
echo -e "${NC}"
echo -e "  ${BOLD}${CYAN}H A L O    A I${NC}   ${DIM}v${HALO_VERSION}${NC}"
echo -e "  ${DIM}bare-metal ai stack for amd strix halo${NC}"
echo ''
