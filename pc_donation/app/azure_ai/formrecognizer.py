from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from flask import current_app

from config import FormRecognizeConfig


class Receipt:
    def __init__(self, date, total, merchant_name):
        self.merchant_name = merchant_name
        self.date = date
        self.total = total


def extract_receipt(receipt_url):
    form_recognizer_client = FormRecognizerClient(FormRecognizeConfig.ENDPOINT,
                                                  AzureKeyCredential(FormRecognizeConfig.KEY))
    poller = form_recognizer_client.begin_recognize_receipts_from_url(receipt_url)
    receipts = poller.result()

    receipt = receipts[0]
    total = receipt.fields.get("Total")
    if total is not None:
        total = total.value
    date = receipt.fields.get("TransactionDate")
    if date is not None:
        date = date.value
    merchant_name = receipt.fields.get("MerchantName")
    if merchant_name is not None:
        merchant_name = merchant_name.value

    return Receipt(date, total, merchant_name)


if __name__ == '__main__':
    x = extract_receipt("https://www.awsacademy.com/resource/1576451101000/logo")
    current_app.logger.info(x.__dict__)
    x = extract_receipt(
        "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg")
    current_app.logger.info(x.__dict__)
