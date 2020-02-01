def check_internet():
    import requests
    url='http://www.google.com/'
    timeout=5
    try:
        print(requests.get(url, timeout=timeout))
        return True
    except requests.ConnectionError:
        print("Nöööööööööööööööööö kein Netzt nööööööööööööö")
        return False
check_internet()
