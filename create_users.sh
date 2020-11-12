for user in "$@"
do
	curl -X POST -H 'Content-Type: application/json' -d '{"username":"'$user'", "email":"'$user'@z.com", "password":"asdf;lkj"}' http://127.0.0.1:8000/api/register/;
done
