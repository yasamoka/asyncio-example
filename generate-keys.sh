COUNTRY="AB"
STATE="XY"
LOCALITY="Test Locality"
ORGANIZATION="Test Organization"

CA_EMAIL_ADDRESS="abc@def.com"
SERVER_EMAIL_ADDRESS="ghi@jkl.com"
CLIENT_EMAIL_ADDRESS="mno@pqr.com"

CA_COMMON_NAME="Test CA"
SERVER_COMMON_NAME="test_server"
CLIENT_COMMON_NAME="test_client"

SERVER_FILENAME="server"
CLIENT_FILENAME="client"

set -x
echo "Generating private keys ..."
openssl genrsa -out ca.key
openssl genrsa -out "server/$SERVER_FILENAME.key"
openssl genrsa -out "client/$CLIENT_FILENAME.key"

echo "Generating CA certificate ..."
openssl req -new -x509 -key ca.key -out ca.crt -subj /emailAddress="$CA_EMAIL_ADDRESS"/C="$COUNTRY"/ST="$STATE"/L="$LOCALITY"/O="$ORGANIZATION"/CN="$CA_COMMON_NAME"

echo "Generating server certificate signing request ..."
openssl req -new -key "server/$SERVER_FILENAME.key" -out "server/$SERVER_FILENAME.csr" -subj /emailAddress="$SERVER_EMAIL_ADDRESS"/C="$COUNTRY"/ST="$STATE"/L="$LOCALITY"/O="$ORGANIZATION"/CN="$SERVER_COMMON_NAME"
echo "Generating server certificate ..."
openssl x509 -req -in "server/$SERVER_FILENAME.csr" -out "server/$SERVER_FILENAME.crt" -CA ca.crt -CAkey ca.key -CAcreateserial

echo "Generating client certificate signing request ..."
openssl req -new -key "client/$CLIENT_FILENAME.key" -out "client/$CLIENT_FILENAME.csr" -subj /emailAddress="$CLIENT_EMAIL_ADDRESS"/C="$COUNTRY"/ST="$STATE"/L="$LOCALITY"/O="$ORGANIZATION"/CN="$CLIENT_COMMON_NAME"
echo "Generating client certificate ..."
openssl x509 -req -in "client/$CLIENT_FILENAME.csr" -out "client/$CLIENT_FILENAME.crt" -CA ca.crt -CAkey ca.key -CAcreateserial

echo "Copying CA certificate to server and client ..."
cp ca.crt "server/ca.crt"
cp ca.crt "client/ca.crt"
