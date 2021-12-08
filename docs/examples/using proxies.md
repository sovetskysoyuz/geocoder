# Using Proxies

Using proxies will hide the IP address of the client computer when calling a request using the Python Geocoder.

```python
>>> import geocoderliqr as geocoder
>>> proxies = {'http':'http://108.165.33.12:3128'}
>>> g = geocoder.google('New York City', proxies=proxies)
>>> g.json
...
```