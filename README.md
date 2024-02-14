# backend-template

## Using different parameters

```bash
curl --request POST \
    "http://localhost:8181/sample/my_path_name?query_age=33&query_name=my_query_name&body_name=body_name_from_query" \
    --header 'Content-Type: application/json' \
    --data '{"body_age": "35", "body_name": "my_body_name"}'
```
