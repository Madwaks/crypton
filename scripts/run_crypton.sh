#!/bin/bash -e

if [[ "$1" == "publish" ]]
then
    APPS=$(python /app/manage.py shell -c 'from django.conf import settings; print(settings.LOCAL_APPS)' | tr -d '[],')

    WINEDB_DEBUG=True python /app/manage.py collectstatic --noinput --clear

    for app in ${APPS}
    do
        # shellcheck disable=SC2046
        python /app/manage.py makemigrations $(echo $app | tr -d "'")
    done

    python /app/manage.py migrate

    for app in ${APPS}
    do
        # shellcheck disable=SC2046
        ls /app/$(echo $app | tr -d "'")/migrations > /dev/null 2>&1 && python /app/manage.py migrate $(echo $app | tr -d "'")
    done

    python /app/manage.py compilemessages

    # shellcheck disable=SC2199
    if [[ " ${@:2} " =~ " -b " ]]
    then
        gunicorn "${@:2}" matcha.wsgi
    else
        BIND_HOSTNAME=$([[ -z "${WINEDB_HOSTNAME}" ]] && echo "127.0.0.1" || echo "${WINEDB_HOSTNAME}")
        BIND_PORT=$([[ -z "${WINEDB_PORT}" ]] && echo "8000" || echo "${WINEDB_PORT}")
        gunicorn "${@:2}" -b "${BIND_HOSTNAME}:${BIND_PORT}" matcha.wsgi
    fi
elif [[ "${1}" == "generate_diff_from_snapshot" ]]
then
    bash ./generate_diff_from_snapshot.sh "${@:2}"
else
    python /app/manage.py "$@"
fi
