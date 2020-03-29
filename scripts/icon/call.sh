#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -c <command> : The T-Bears command to launch"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$command" == "") ]]; then
        print_usage
    fi

    # Execute T-Bears
    result=`eval ${command}`

    # Display commands
    info "> Command:"
    debug "$ ${command}"

    # Display result
    info "> Result:"
    debug "$ ${result}"
}

# Parameters
while getopts "n:c:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        c)
            command=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process