for user in "$@"
do
	curl -X POST -H 'Content-Type: application/json' -d '{"username":"'$user'", "email":"'$user'@m.com", "password":"12341234"}' http://127.0.0.1:8000/api/register/;
done
