import configparser

def get_username() -> str:
    config_ = configparser.ConfigParser()
    config_.read("user.ini")
    return config_["user"]["username"]

def get_password() -> str:
    config_ = configparser.ConfigParser()
    config_.read("user.ini")
    return config_["user"]["password"]

user = get_username()
password = get_password()
host = "127.0.0.1"