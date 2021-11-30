To run the server, run the following command
```
python3 http_server.py -c certs/web-platform.test.pem -k certs/web-platform.test.key --host 127.0.0.1 -q logs demo:app
```

To run the client
```
python3 http_client.py https://127.0.0.1:4433/<command> --output_dir downloads/
```