import imaplib
import email
from datetime import datetime
from time import sleep

def fetch_code(user, password, imap_url):

    #1. Get email content 
    def get_body(msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)
        
    #2. Function to search for a key value pair
    def search(key, value, con):
        result, data = con.search(None, key, '"{}"'.format(value))
        return data
    
    #3. Function to get the list of emails under this label
    def get_emails(result_bytes):
        msgs = [] # All emails pushed into an array
        for num in result_bytes[0].split():
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)

        return msgs

    FindCodeFlag = True
    breakFlag = False
    Count = 20
    while FindCodeFlag and Count :
        print(Count)
        Count -= 1
        
        sleep(5)

        con = imaplib.IMAP4_SSL(imap_url, 993)
        con.login(user, password)
        con.select('INBOX')

        search_results = search('From', 'noreply@frontdesksuite.com', con ) #Subject Verify your email
        messages = get_emails(search_results)

        #4. Find code from email
    
        for message in messages[::-1]:
            for content in message:
                if type(content) is tuple:

                    # Encoding set as utf-8
                    decoded_content = str(content[1], 'utf-8')
                    data = str(decoded_content)

                    # Extracting the subject from the mail content
                    ReceiveTime = data.split('OriginalArrivalTime: ')[1].split('(UTC)')[0].strip().split('.')[0]
                    ReceiveTime = datetime.strptime(ReceiveTime, '%d %b %Y %H:%M:%S')
                    subject = data.split('Subject: ')[1].split('Mime-Version')[0]

                    if ReceiveTime.day >= datetime.today().day:
                        if "Verify your email" in subject:
                            VrCode = data.split('Your verification code is:')[1].split('The code must be entered on the')[0].strip()
                            print(VrCode)
                            breakFlag = True
                            break
                        else:
                            print('Not found!')

                    # Handling errors related to unicodenecode
                    try:
                        indexstart = data.find("ltr")
                        data2 = data[indexstart +5: len(data)]
                        indexend = data2.find("</div>")

                        # Uncomment to see what the content looks like
                    except UnicodeEncodeError as e:
                        print('Pass')
                        pass
            if breakFlag:
                FindCodeFlag = False
                break
        con.close()
        con.logout()

    if breakFlag:
        return  VrCode
    else:
        return 0