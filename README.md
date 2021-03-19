# GCSTranscribe.py
## What is this for?
This script will allow you to make use of Google Cloud Speech-To-Text in order to transcribe interviews.

## Is it 100% accurate?
Silly question! Of course, there will be multiple mistakes, but even a "pre-transcript" could save you tons of time (say, you might be able to transcribe an interview within a day as compared to multiple days).

## Is it free?
### Short answer
Yes.

### Long answer
Google gives every new Google Cloud user 300USD worth of credit to try their platform. Plus, the 1st hour of interview transcriptions is free, every month. 1 hour of interview transcriptions costs 2.16USD in the worst case scenario.

With 300USD gifted by Google to spare, it is highly unlikely that you will run into any limits when using this software.

[Read more on Google's Cloud Speech-To-Text Pricing here.](https://cloud.google.com/speech-to-text/pricing)

## How do I set this up?
1. Download or clone this repository
2. [Install Python 3](https://www.python.org/downloads/)
3. In a command line/terminal, change to the GCSTranscribe folder, run `pip3 install -r requirements.txt`
4. [Sign-up for a free Google Cloud account](https://cloud.google.com/free) (make sure to use the link to get the 300USD gift promo)
5. [Enable the Cloud Speech-To-Text API](https://console.cloud.google.com/apis/library/speech.googleapis.com), which will automatically create a Google Cloud Project
6. [Create a service account through the console in your GC project](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console), enter anything you like as a name (I just use "access"), for step 2 choose "Owner", then just click "Continue" for the optional steps
7. Click on the newly created service account, then in the "Keys" tab click on "Add Key", select "JSON", and then click create - move the downloaded JSON file into the folder where GCSTranscribe.py is and rename it to "auth.json" (that is the default name as specified in the config file)
8. [Go to the Google Cloud Storage and create a bucket](https://console.cloud.google.com/storage), this is where you will upload your interview audio in the FLAC format (if your interviews aren't in FLAC, Google is your friend on how to convert them)
9. When done, upload your interviews into the Google Cloud Storage bucket, edit the config.ini to point to the file and then run GCSTranscribe.py on the Terminal/command line
10. After a while, the script should finish running, and you will have a transcript file in your 