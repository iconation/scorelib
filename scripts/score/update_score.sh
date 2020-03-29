#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") ]]; then
        print_usage
    fi

    command=$(cat <<-COMMAND
    tbears deploy $(get_package_name)
        -m update
        -o $(cat ./config/${network}/score_address.txt)
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process