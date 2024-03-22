import email
import re
import nltk
# nltk.download('punkt')

def parseMail(email_message):
    email_headers = dict(email_message.items())
    email_body = email_message.get_payload(decode=False)
    return [email_headers, email_body]

def preProcessSubject(email_subject):
    header_without_punctuation = re.sub(r'[^\w\s]', '', email_subject)
    header_tokens = nltk.word_tokenize(header_without_punctuation)
    header_tokens = list(map(lambda word : word.lower(), header_tokens))
    header_without_punctuation = " ".join(header_tokens)
    return header_tokens, header_without_punctuation

def preProcessContent(email_content):
    content_without_punctuation = re.sub(r'[^\w\s]', '', email_content)
    content_tokens = nltk.word_tokenize(content_without_punctuation)
    content_tokens = list(map(lambda word : word.lower(), content_tokens))
    content_without_punctuation = " ".join(content_tokens)
    return content_tokens, content_without_punctuation

def subjectCheck(email_subject):
    subjectRegEx = r'\b(urgent|important|required|limited time offer|free|overnight|miracle|overnight)\b'
    return bool(re.search(subjectRegEx, email_subject))

def contentCheck(content_tokens, content_without_punctuation):
    reg1 = r'\b(important|action required|limited time offer|exclusive deal)\b'
    reg2 = r'\b(urgent|act now|don\'t miss out|limited time|save big)\b'
    reg3 = r'\b(\d+% off|exclusive offer|limited time discount|discount|incredible)\b'
    reg4 = r'\b(account\s*verification|update your information|click\s*here\s*to\s*verify)\b'
    reg5 = r'\b(unsubscribe|opt\s*out|you\s*are\s*receiving\s*this\s*email|unsubscribe\s*here)\b'
    reg6 = r'\b(shocking|amazing|unbelievable|you\s*won)\b'

    failedChecks = 0
    failedRegex = 0
    totalRegex = 6
    totalChecks = len(content_tokens)

    if (re.search(reg1, content_without_punctuation)):
        failedRegex += 1
    if (re.search(reg2, content_without_punctuation)):
        failedRegex += 1
    if (re.search(reg3, content_without_punctuation)):
        failedRegex += 1
    if (re.search(reg4, content_without_punctuation)):
        failedRegex += 1
    if (re.search(reg5, content_without_punctuation)):
        failedRegex += 1
    if (re.search(reg6, content_without_punctuation)):
        failedRegex += 1

    spamWords = [
        "free", "get it for free", "free offer", "free trial", "goodbye", "buy"
        "free gift", "discount", "limited time offer", "special offer",
        "save money", "exclusive offer", "best deal", "act now", "millionaire", "dreamed"
        "limited", "time", "only", "hurry", "don't miss out", "last chance", "urgent",
        "make money", "earn money", "get rich quick", "cash prize", "guaranteed income", "rich"
        "financial freedom", "lose weight", "diet", "weight loss", "health insurance", "anti-aging"
        "miracle", "bank account", "password", "your account", "account verification", "update", "information",
        "order", "instant", "revolutionary", "battling", 'overnight', 'transform', 'struggling', 'tired'
    ]

    for word in content_tokens:
        if word in spamWords:
            failedChecks += 1

    return failedChecks, failedRegex, totalChecks, totalRegex

def spamConclusion(failedChecks, failedRegex, totalChecks, totalRegex):
    print("Number of spam words:", failedChecks, "out of", totalChecks)
    print("Number of regex failures:", failedRegex, "out of", totalRegex)
    wordsFail = failedChecks/totalChecks
    regexFail = failedRegex/totalRegex
    if (wordsFail>=0.10 and regexFail>=0.10):
        print("This is a spam mail")
    elif wordsFail > 0.10 or regexFail >= 0.10:
        print("This is a probable spam mail")
    else:
        print("This is not a spam mail")
    return None

def menu():
    print("Welcome to Spam Mail Detector")
    print("-1 to exit")
    while (True):
        mailChoice = int(input("Enter choice of file (1-5): "))
        if (mailChoice == -1):
            print("Thank you")
            break

        if mailChoice == 1:
            file_path = "spam1.eml"
        elif mailChoice == 2:
            file_path = "notSpam2.eml"
        elif mailChoice == 3:
            file_path = "notSpam3.eml"
        elif mailChoice == 4:
            file_path = "spam4.eml"
        elif mailChoice == 5:
            file_path = "spam5.eml"
        elif mailChoice == 6:
            file_path = "test2.eml"
        else:
            print("Enter valid choice")
            continue

        with open(file_path, "r") as f:
            email_message = email.message_from_file(f)
        email_header, email_body = parseMail(email_message)
        subjectTokens, subjectWithoutPunctuation = preProcessSubject(email_header["Subject"])
        content_tokens, content_without_punctuation = preProcessContent(email_body)

        subjectCheckResult = subjectCheck(subjectWithoutPunctuation)
        print("Spam keywords in subject line? ->", subjectCheckResult)

        failedChecks, failedRegex, totalChecks, totalRegex = contentCheck(content_tokens, content_without_punctuation)
        spamConclusion(failedChecks, failedRegex, totalChecks, totalRegex)
        print("\n")

menu()