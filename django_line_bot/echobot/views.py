#Django
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

#LINE-SDK
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#Tool
import re
import twder

#API Key
line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)


@csrf_exempt
def callback(request: HttpRequest) -> HttpResponse:
    
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

#處理訊息

@handler.add(MessageEvent, message=TextMessage)
def message_text(event: MessageEvent):
    msg = str(event.message.text)

    if re.match("匯率", msg):
        USD=str(twder.now('USD'))
        EUR=str(twder.now('EUR'))
        CNY=str(twder.now('CNY'))
        JPY=str(twder.now('JPY'))
        exchange = "美金:"+ USD+ "\n" +"\n"+ "歐元:"+ EUR + "\n" +"\n" + "人民幣:"+ CNY + "\n" + "\n"+ "日幣:"+ JPY
        line_bot_api.reply_message(event.reply_token,TextSendMessage(exchange))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg)
    )
