#!/bin/bash

function error {
    echo -ne "\e[91m"
    echo -e  "${1}"
    echo -ne "\e[39m"
}

function info {
    echo -ne "\e[32m"
    echo -e  "${1}"
    echo -ne "\e[39m"
}

function warning {
    echo -ne "\e[93m"
    echo -e  "${1}"
    echo -ne "\e[39m"
}

function debug {
    echo -ne "\e[94m"
    echo -e  "${1}"
    echo -ne "\e[39m"
}

function highlight {
    echo -ne "\e[96m"
    echo -e  "${1}"
    echo -ne "\e[39m"
}

function usage_header {
    info "\n> Usage:"
    debug " \`-> ${1} [options]"
    info "\n> Options:"
}

function usage_option {
    debug "${1}"
}

function usage_footer {
    debug "\n"
}

function get_package_name {
    package=$(cat $(find . -maxdepth 2 -name "package.json" | tail -1) | jq '.main_score')
    echo ${package}
}

function get_score_address {
    score_address=`echo -ne "${1}" | grep "scoreAddress" | awk -F 'cx' '{print $2}' | sed 's/",//g'`
    echo cx${score_address}
}

function get_tx_hash {
    txhash=`echo -n ${1} | awk -F '0x' '{print $2}'`
    echo 0x${txhash}
}