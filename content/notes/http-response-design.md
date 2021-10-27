+++
aliases = ["/comments/20210210-155431/"]
date = "2021-02-10T15:54:31"
epistemic = "sprout"
tags = ["python","errors","design"]
title = "HTTP Response Design"
+++
As Victoria mentions in her [post](https://victoria.dev/blog/do-i-raise-or-return-errors-in-python/), the type of code you're writing affects how you'll handle errors. Her example matches code that integrates with other systems on the same machine (and probably other cases).

The code I'm writing these days, when it's not JavaScript, is for back-end services. I've discovered that services delivered over HTTP/S are best implemented to capture exceptions in the service and return response objects. I'll usually do something like this:

```
{
  "success": false,
  "message": "id 5 does not exist",
  "result": null
}
```

Consumption of this kind of API is straightforward and reduces the amount of error handling necessary in the front-end code. I don't know that I'd recommend this for writing a library to read data from the file share, but for a web API, absolutely. Thoughts?

