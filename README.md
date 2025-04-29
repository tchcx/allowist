## allowist (WIP)

Allowist! For allow... lists.

Lambda function for aggregating allow lists individually or by category. Curated to ensure an appropriate balance between specificity (too restrictive) and generality (too permissive).

The ultimate goal is to recieve a GET request, parse the URL query parameters, combine the requested lists, and return the aggregate allow list. For instance:

`https://some.lambda.site/blahblah?token=1234567890&include=ca,captcha,cdn,ntp,push,pwmgr`
