# 2019-Predictions-Redis-Python
Predict 2019 with Redis and Python

This repository is to use Redis and Flask to provide future predictions and also to limit the number of user requests,

1) In Redis DB 0, we will include multiple future predictions as values with keys as integers.
2) In Redis DB 1, we will include a request_count key which would contain the current processed request count.
3) In Flask we will build a route URL with GET Request to input a name. Increment the value of request_count key on receiving a request with the key as IP. For an hour, one ip is allowed only to make 10 requests. 
4) If the value of request_count exceeds 10, Return to the user saying “You have exceeded 10 requests per session”.


For more details on how to use this repo, Go to https://nosqlly.com/redis-python-project/
