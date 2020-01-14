from pywebpush import webpush, WebPushException
import logging

WEBPUSH_VAPID_PRIVATE_KEY = 'xxx'

# from PushManager: https://developer.mozilla.org/en-US/docs/Web/API/PushManager
subscription_info = {"endpoint": "https://updates.push.services.mozilla.com/push/v1/gAA...", "keys": {"auth": "k8J...", "p256dh": "BOr..."}}

try:
    webpush(
        subscription_info=subscription_info,
        data="Test 123", # could be json object as well
        vapid_private_key=WEBPUSH_VAPID_PRIVATE_KEY,
        vapid_claims={
            "sub": "mailto:webpush@mydomain.com"
        }
    )
    count += 1
except WebPushException as e:
    logging.exception("webpush fail")