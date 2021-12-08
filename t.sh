hello=awfwafa_port23423
final=$hello
re='(.+)_port[0-9]'
while [[ $hello =~ $re ]]; do
  hello=${BASH_REMATCH[1]}
done
echo "$hello"
echo "$final"