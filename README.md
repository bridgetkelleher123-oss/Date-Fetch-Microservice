Parameter Requirements:

Date format options for input_date parameter and output_date parameter:
|Symbol|Meaning|Example|
|---|---|---|
|%Y|4-digit year|2026|
|%y|2-digit year|26|
|%m|Month as a 2-digit number|11|
|%B|Full month name in writing|November|
|%b|Abbreviated month name|Nov|
|%d|Day of the month (01-31)|10|
|%A|Full weekday name|Tuesday|
|%a|Abbreviated weekday name|Tue|
|%j|Day of the year (001-366)|314|


Example client call to the microservice:
```python
request = {
    "date": "11/10/2026",
    "input_format": "%m/%d/%Y",
    "output_format": "%A, %B %d, %Y"
}

socket.send_json(request)
```

Example output JSON returned to client:
```python
{
“Success”: true
“formatted_date”: "Tuesday, November 10, 2026"
}
```

