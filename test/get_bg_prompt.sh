#!/bin/bash

curl --request POST \
  --url http://127.0.0.1:8010/getBackgroundPromptByOssPath \
  --header 'content-type: application/json' \
  --data '{
    "oss_path": "spider/liblibai_images/e76990ad5a21331ca87156e5468a6ee0c1e1f836fa44db1b63c05e089088c63b.png"
  }'
