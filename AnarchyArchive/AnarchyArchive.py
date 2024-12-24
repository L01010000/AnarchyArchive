from termcolor import cprint
import requests
from bs4 import BeautifulSoup
import os

def search_and_download(book_name, download_dir="AnarchyArchive"):
 
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    full_download_dir = os.path.join(desktop_path, download_dir)

    search_url = "https://www.bing.com/search"
    params = {"q": f"{book_name} filetype:pdf"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }


    response = requests.get(search_url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return


    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True) if "http" in a['href']]
    print()
    cprint(f"Found {len(links)} links. Searching for downloadable content...", 'blue')
    

    for link in links:
        try:

            cprint(f"Checking: {link}", 'blue', attrs=['underline'])
            file_response = requests.get(link, headers=headers, stream=True)
            content_type = file_response.headers.get("Content-Type", "")
            if "application/pdf" in content_type:  
                cprint(f"PDF found: {link}",'red')


                os.makedirs(full_download_dir, exist_ok=True)  
                file_path = os.path.join(full_download_dir, f"{book_name.replace(' ', '_')}.pdf")
                with open(file_path, "wb") as f:
                    for chunk in file_response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print()
                cprint(f"Book downloaded successfully: {file_path}", 'red', attrs=['bold'])
                return
        except Exception as e:
            cprint(f"Error while processing {link}: {e}", 'red')
    
    cprint("No downloadable PDF found.", 'red')


os.system('cls' if os.name == 'nt' else 'clear')

cprint('''                                                                                                                               
                _                    _          _          _    _         
               /_\  _ _  __ _ _ _ __| |_ _  _  /_\  _ _ __| |_ (_)_ _____ 
              / _ \| ' \/ _` | '_/ _| ' \ || |/ _ \| '_/ _| ' \| \ V / -_)
             /_/ \_\_||_\__,_|_| \__|_||_\_, /_/ \_\_| \__|_||_|_|\_/\___|
                                         |__/    Made by 0p1um     

                Knowledge and courage contribute in turn to greatness. 
    Since they are immortal, they immortalize. A person without knowledge is a world in darkness.     
                                                        - Baltasar Gracian                    
''','red')

def main():
    while True:
        cprint('Enter the book name: ', 'blue', attrs=['bold'], end='')  
        book_name = input()
        
        search_and_download(book_name)
        cprint("Enter 0 to exit or 1 to restart.", 'yellow', attrs=['bold'])
        x=int(input())
        if x==0:
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif x==1:
            continue

if __name__ == "__main__":
    main()
