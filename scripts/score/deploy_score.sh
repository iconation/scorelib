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
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    exitcode=$?
    echo -e "${txresult}"

    if [ ${exitcode} -eq 0 ] ; then
        # Write the new score address to the configuration
        score_address=$(get_score_address "${txresult}")
        if [ "${score_address}" != "" ] ; then
            echo -e "New SCORE address detected : ${score_address}"
            echo -ne "${score_address}" > "./config/${network}/score_address.txt"
        fi
    fi
}

# Parameters
while getopts "n::" option; do
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