
import json

headersArray = {"Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"}
headersArray2 = {"Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko"}

def read_conf():
    conf_file = open("config.json", "r")
    conf_json = json.load(conf_file)
    return conf_json

