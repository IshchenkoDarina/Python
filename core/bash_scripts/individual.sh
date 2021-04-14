echo "List of active services:"
service --status-all | grep "+"

echo "Stop services:"
for var in "$@"
do
    echo "Stop $var"
    sudo service $var stop
done


echo "Start services:"
for var in "$@"
do
    echo "Start $var"
    sudo service $var start
done

echo "Count active services:"
service --status-all | grep -c "+"

echo "Services for service:"
service --status-all | grep -e " cron$" -e " nginx$"
