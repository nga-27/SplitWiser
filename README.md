# SplitWiser
That greedy company that manages Splitwise decided that its users should pay way more than its ads, so to avoid the paywall, why not do it myself!

# To Run

From the root of the project, run:

```sh
python app.py
```

For API debugging, you can run `uvicorn` directly:
```sh
uvicorn api.server:app --log-level=warning --port=8765
```
