@echo off
set COUNTRY=AB
set STATE=XY
set LOCALITY=Test Locality
set ORGANIZATION=Test Organization

set CA_EMAIL_ADDRESS=abc@def.com
set SERVER_EMAIL_ADDRESS=ghi@jkl.com
set CLIENT_EMAIL_ADDRESS=mno@pqr.com

set CA_COMMON_NAME=Test CA
set SERVER_COMMON_NAME=test_server
set CLIENT_COMMON_NAME=test_client

set SERVER_FILENAME=server
set CLIENT_FILENAME=client

@echo on
REM Generating private keys ...
openssl genrsa -out ca.key
openssl genrsa -out "server/%SERVER_FILENAME%.key"
openssl genrsa -out "client/%CLIENT_FILENAME%.key"

REM Generating CA certificate ...
openssl req -new -x509 -key ca.key -out ca.crt -subj /emailAddress="%CA_EMAIL_ADDRESS%"/C="%COUNTRY%"/ST="%STATE%"/L="%LOCALITY%"/O="%ORGANIZATION%"/CN="%CA_COMMON_NAME%"

REM Generating server certificate signing request ...
openssl req -new -key "server/%SERVER_FILENAME%.key" -out "server/%SERVER_FILENAME%.csr" -subj /emailAddress="%SERVER_EMAIL_ADDRESS%"/C="%COUNTRY%"/ST="%STATE%"/L="%LOCALITY%"/O="%ORGANIZATION%"/CN="%SERVER_COMMON_NAME%"
REM Generating server certificate ...
openssl x509 -req -in "server/%SERVER_FILENAME%.csr" -out "server/%SERVER_FILENAME%.crt" -CA ca.crt -CAkey ca.key -CAcreateserial

REM Generating client certificate signing request ...
openssl req -new -key "client/%CLIENT_FILENAME%.key" -out "client/%CLIENT_FILENAME%.csr" -subj /emailAddress="%CLIENT_EMAIL_ADDRESS%"/C="%COUNTRY%"/ST="%STATE%"/L="%LOCALITY%"/O="%ORGANIZATION%"/CN="%CLIENT_COMMON_NAME%"
REM Generating client certificate ...
openssl x509 -req -in "client/%CLIENT_FILENAME%.csr" -out "client/%CLIENT_FILENAME%.crt" -CA ca.crt -CAkey ca.key -CAcreateserial

REM Copying CA certificate to server and client ...
copy ca.crt "server/ca.crt"
copy ca.crt "client/ca.crt"