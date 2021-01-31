import json
import pytest
from unittest.mock import patch, MagicMock

from integrations import notifications

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "Records": [
            {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:297473205123:adt-email-notifications:6ae6707c-f1f1-4712-a5de-ac8e951b751a",
            "Sns": {
                "Type": "Notification",
                "MessageId": "31d96e8f-31f4-5b0b-b45b-36019e83eafe",
                "TopicArn": "arn:aws:sns:us-east-1:297473205123:adt-email-notifications",
                "Subject": "Amazon SES Email Receipt Notification",
                "Message": "{\"notificationType\":\"Received\",\"mail\":{\"timestamp\":\"2021-01-30T00:49:59.401Z\",\"source\":\"julio.r.santos.jr@gmail.com\",\"messageId\":\"rl2j71s6pqi2mc672li386j13ftb2rj1q7umuk81\",\"destination\":[\"doors@automation.everythingbiig.com\"],\"headersTruncated\":false,\"headers\":[{\"name\":\"Return-Path\",\"value\":\"<julio.r.santos.jr@gmail.com>\"},{\"name\":\"Received\",\"value\":\"from mail-lj1-f170.google.com (mail-lj1-f170.google.com [209.85.208.170]) by inbound-smtp.us-east-1.amazonaws.com with SMTP id rl2j71s6pqi2mc672li386j13ftb2rj1q7umuk81 for doors@automation.everythingbiig.com; Sat, 30 Jan 2021 00:49:59 +0000 (UTC)\"},{\"name\":\"X-SES-Spam-Verdict\",\"value\":\"PASS\"},{\"name\":\"X-SES-Virus-Verdict\",\"value\":\"PASS\"},{\"name\":\"Received-SPF\",\"value\":\"pass (spfCheck: domain of _spf.google.com designates 209.85.208.170 as permitted sender) client-ip=209.85.208.170; envelope-from=julio.r.santos.jr@gmail.com; helo=mail-lj1-f170.google.com;\"},{\"name\":\"Authentication-Results\",\"value\":\"amazonses.com; spf=pass (spfCheck: domain of _spf.google.com designates 209.85.208.170 as permitted sender) client-ip=209.85.208.170; envelope-from=julio.r.santos.jr@gmail.com; helo=mail-lj1-f170.google.com; dkim=pass header.i=@gmail.com; dmarc=pass header.from=gmail.com;\"},{\"name\":\"X-SES-RECEIPT\",\"value\":\"AEFBQUFBQUFBQUFFWHJDWHdQaHNHbVN4T00vd3dqSElkTUFYYVV2U2hmbFlQSFU5aVJKNjFZYXhoSWNFZ0pIbWZIZVd0MGpyVjhIV0dINmpGTDFGWVh1a0VwU1BZL0FzTUF1clVmMVlMYUcvNmg2LzgraTZzbHk5RUY1RUQvdENjZkR2U2xqL21SRjhlazhOZGJ3NzNvTytxa3VBVUJsSUNxVkNsTWlwZFlabHZoUk90cGY4Q3VvK0xEaWtCQjcyeHdBdUN0b2RBeGdvZVJ0bWVra1pOdmJWR0NZNTlQd1NSa25ITHREaTRoK096YTZhNFlSTGhzZGNoVk5qdjE0VTdSb290N1hxOXlkYWZUUXBac25TNWpwc29nSGlXbjRPeUcwU0pkaTJmZ1UxLytvRTdNMER1MEE9PQ==\"},{\"name\":\"X-SES-DKIM-SIGNATURE\",\"value\":\"a=rsa-sha256; q=dns/txt; b=XjPnwwPmrNgj7v0tvBBzqjltczO9IaaqW7EBgBLa/s+FoMXdYtaeOYx+Y2R9OArM+IO244Al5PJBKxJoXhUTSNdCAotc0OSpKlpkuZoZ/XbBvxQ7ZooZkU4sj6Bc3V82C8Nlivev/9O8Iy8KBf8L92sEzSgy6NZKoDLYo1XugYc=; c=relaxed/simple; s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1611967799; v=1; bh=kAVC1P+kz94sVflXq4lKE/nns35IXhTFSWoJLOj+VlM=; h=From:To:Cc:Bcc:Subject:Date:Message-ID:MIME-Version:Content-Type:X-SES-RECEIPT;\"},{\"name\":\"Received\",\"value\":\"by mail-lj1-f170.google.com with SMTP id f11so12531539ljm.8 for <doors@automation.everythingbiig.com>; Fri, 29 Jan 2021 16:49:59 -0800 (PST)\"},{\"name\":\"DKIM-Signature\",\"value\":\"v=1; a=rsa-sha256; c=relaxed/relaxed; d=gmail.com; s=20161025; h=mime-version:from:date:message-id:subject:to; bh=kAVC1P+kz94sVflXq4lKE/nns35IXhTFSWoJLOj+VlM=; b=TfN6RDByusSh6bQnuYGYHHvcr2e59Sif78woZ5WZNPnuC5E4h+GoMOU6ZWpJE3umL3LPx/a+4w3Imw95vXUSYpTdvFWp71lIHvHkVN5bhT5zCuA/B2EZnc5Uz0BFi/eEkEmY7KVknKP/lShPbluaOAdLGrqIE+XemTjlQ18P6KiHniEuf3rpGrXnzYdT4fo6QO4N2ZPQlIbWkv7Buunu+vKgLQgI/vr3uOLYscLIoIpICYuO879KXEKMISJ0SkV9ATXGQ1lfS82iqiazrZTSms+pTTBZ2RidlUua+8MCSUIJvkHbMbVhRRKXxc39RrSIGZ3XVLoyy8/TpqSJURpLWw==\"},{\"name\":\"X-Google-DKIM-Signature\",\"value\":\"v=1; a=rsa-sha256; c=relaxed/relaxed; d=1e100.net; s=20161025; h=x-gm-message-state:mime-version:from:date:message-id:subject:to; bh=kAVC1P+kz94sVflXq4lKE/nns35IXhTFSWoJLOj+VlM=; b=ZmyC/eiNbjIsdSEjvMqZ/ijPIhy4jeWyZhHk0P0DQZf+Qe0bD/V3eYa3Q0mQPTkNJM ykS16xBBss5fZ5rX0CuKAytJS+0aOOpLk+9Y5+k+7ADBchGpNYeK9gRTPmYqwEXlVLst AzW5tmHv+r5eH8qOyG9u/N1bc7D2dBLOe80z6bQzWGCvvYavMytbAAfVcZ0gFvDZlr8L AH+1lZ8HpseND4IjraPjTlCwgCtvl+0afUZyVaf1b6b7vcdpojxYPGYdl1JAso7Np8Kz ahgXsJBYI7gA7AD9Z42dkFmXcAWrgMSSe9/ZQ4End7Fd3rB+mUcSQ9gseu63N+t/h9G3 qx7A==\"},{\"name\":\"X-Gm-Message-State\",\"value\":\"AOAM532he3KeB9G6MJAo295Y3co/xBZLTvBInBgUpzmabzTkASTPs7JI CCpbintck3yWi2j0tQWmBA5CMpsfhT4RUD7uHGrrWVgphzQ=\"},{\"name\":\"X-Google-Smtp-Source\",\"value\":\"ABdhPJyXemuVYyqdAm6ICjyv1WgelmRLNMzWmQ1lXEk/Ia8t+5ECBWmLiyFSzMims+Offdvd2JSLe+6Ie4RaDNguQ4U=\"},{\"name\":\"X-Received\",\"value\":\"by 2002:a2e:8005:: with SMTP id j5mr3814771ljg.34.1611967797531; Fri, 29 Jan 2021 16:49:57 -0800 (PST)\"},{\"name\":\"MIME-Version\",\"value\":\"1.0\"},{\"name\":\"From\",\"value\":\"Julio Santos <julio.r.santos.jr@gmail.com>\"},{\"name\":\"Date\",\"value\":\"Fri, 29 Jan 2021 19:49:46 -0500\"},{\"name\":\"Message-ID\",\"value\":\"<CAJYkhH-tOKRbR97qqOWQuuQP+XhW0mxF4u2-XBe3FQRUK6WhUQ@mail.gmail.com>\"},{\"name\":\"Subject\",\"value\":\"JULIO SANTOS's System: The Basement Front Door was Opened at 8:07 pm\"},{\"name\":\"To\",\"value\":\"doors@automation.everythingbiig.com\"},{\"name\":\"Content-Type\",\"value\":\"multipart/alternative; boundary=\\\"000000000000f616ec05ba137f77\\\"\"}],\"commonHeaders\":{\"returnPath\":\"julio.r.santos.jr@gmail.com\",\"from\":[\"Julio Santos <julio.r.santos.jr@gmail.com>\"],\"date\":\"Fri, 29 Jan 2021 19:49:46 -0500\",\"to\":[\"doors@automation.everythingbiig.com\"],\"messageId\":\"<CAJYkhH-tOKRbR97qqOWQuuQP+XhW0mxF4u2-XBe3FQRUK6WhUQ@mail.gmail.com>\",\"subject\":\"Durrr\"}},\"receipt\":{\"timestamp\":\"2021-01-30T00:49:59.401Z\",\"processingTimeMillis\":403,\"recipients\":[\"doors@automation.everythingbiig.com\"],\"spamVerdict\":{\"status\":\"PASS\"},\"virusVerdict\":{\"status\":\"PASS\"},\"spfVerdict\":{\"status\":\"PASS\"},\"dkimVerdict\":{\"status\":\"PASS\"},\"dmarcVerdict\":{\"status\":\"PASS\"},\"action\":{\"type\":\"SNS\",\"topicArn\":\"arn:aws:sns:us-east-1:297473205123:adt-email-notifications\",\"encoding\":\"BASE64\"}},\"content\":\"UmV0dXJuLVBhdGg6IDxqdWxpby5yLnNhbnRvcy5qckBnbWFpbC5jb20+DQpSZWNlaXZlZDogZnJvbSBtYWlsLWxqMS1mMTcwLmdvb2dsZS5jb20gKG1haWwtbGoxLWYxNzAuZ29vZ2xlLmNvbSBbMjA5Ljg1LjIwOC4xNzBdKQ0KIGJ5IGluYm91bmQtc210cC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbSB3aXRoIFNNVFAgaWQgcmwyajcxczZwcWkybWM2NzJsaTM4NmoxM2Z0YjJyajFxN3VtdWs4MQ0KIGZvciBkb29yc0BhdXRvbWF0aW9uLmV2ZXJ5dGhpbmdiaWlnLmNvbTsNCiBTYXQsIDMwIEphbiAyMDIxIDAwOjQ5OjU5ICswMDAwIChVVEMpDQpYLVNFUy1TcGFtLVZlcmRpY3Q6IFBBU1MNClgtU0VTLVZpcnVzLVZlcmRpY3Q6IFBBU1MNClJlY2VpdmVkLVNQRjogcGFzcyAoc3BmQ2hlY2s6IGRvbWFpbiBvZiBfc3BmLmdvb2dsZS5jb20gZGVzaWduYXRlcyAyMDkuODUuMjA4LjE3MCBhcyBwZXJtaXR0ZWQgc2VuZGVyKSBjbGllbnQtaXA9MjA5Ljg1LjIwOC4xNzA7IGVudmVsb3BlLWZyb209anVsaW8uci5zYW50b3MuanJAZ21haWwuY29tOyBoZWxvPW1haWwtbGoxLWYxNzAuZ29vZ2xlLmNvbTsNCkF1dGhlbnRpY2F0aW9uLVJlc3VsdHM6IGFtYXpvbnNlcy5jb207DQogc3BmPXBhc3MgKHNwZkNoZWNrOiBkb21haW4gb2YgX3NwZi5nb29nbGUuY29tIGRlc2lnbmF0ZXMgMjA5Ljg1LjIwOC4xNzAgYXMgcGVybWl0dGVkIHNlbmRlcikgY2xpZW50LWlwPTIwOS44NS4yMDguMTcwOyBlbnZlbG9wZS1mcm9tPWp1bGlvLnIuc2FudG9zLmpyQGdtYWlsLmNvbTsgaGVsbz1tYWlsLWxqMS1mMTcwLmdvb2dsZS5jb207DQogZGtpbT1wYXNzIGhlYWRlci5pPUBnbWFpbC5jb207DQogZG1hcmM9cGFzcyBoZWFkZXIuZnJvbT1nbWFpbC5jb207DQpYLVNFUy1SRUNFSVBUOiBBRUZCUVVGQlFVRkJRVUZGV0hKRFdIZFFhSE5IYlZONFQwMHZkM2RxU0Vsa1RVRllZVlYyVTJobWJGbFFTRlU1YVZKS05qRlpZWGhvU1dORlowcEliV1pJWlZkME1HcHlWamhJVjBkSU5tcEdUREZHV1ZoMWEwVndVMUJaTDBGelRVRjFjbFZtTVZsTVlVY3ZObWcyTHpncmFUWnpiSGs1UlVZMVJVUXZkRU5qWmtSMlUyeHFMMjFTUmpobGF6aE9aR0ozTnpOdlR5dHhhM1ZCVlVKc1NVTnhWa05zVFdsd1pGbGFiSFpvVWs5MGNHWTRRM1Z2SzB4RWFXdENRamN5ZUhkQmRVTjBiMlJCZUdkdlpWSjBiV1ZyYTFwT2RtSldSME5aTlRsUWQxTlNhMjVJVEhSRWFUUm9LMDk2WVRaaE5GbFNUR2h6WkdOb1ZrNXFkakUwVlRkU2IyOTBOMWh4T1hsa1lXWlVVWEJhYzI1VE5XcHdjMjluU0dsWGJqUlBlVWN3VTBwa2FUSm1aMVV4THl0dlJUZE5NRVIxTUVFOVBRPT0NClgtU0VTLURLSU0tU0lHTkFUVVJFOiBhPXJzYS1zaGEyNTY7IHE9ZG5zL3R4dDsgYj1YalBud3dQbXJOZ2o3djB0dkJCenFqbHRjek85SWFhcVc3RUJnQkxhL3MrRm9NWGRZdGFlT1l4K1kyUjlPQXJNK0lPMjQ0QWw1UEpCS3hKb1hoVVRTTmRDQW90YzBPU3BLbHBrdVpvWi9YYkJ2eFE3Wm9vWmtVNHNqNkJjM1Y4MkM4TmxpdmV2LzlPOEl5OEtCZjhMOTJzRXpTZ3k2TlpLb0RMWW8xWHVnWWM9OyBjPXJlbGF4ZWQvc2ltcGxlOyBzPTIyNGk0eXhhNWR2N2MyeHozd29tdzZwZXVhc3Rlb25vOyBkPWFtYXpvbnNlcy5jb207IHQ9MTYxMTk2Nzc5OTsgdj0xOyBiaD1rQVZDMVAra3o5NHNWZmxYcTRsS0Uvbm5zMzVJWGhURlNXb0pMT2orVmxNPTsgaD1Gcm9tOlRvOkNjOkJjYzpTdWJqZWN0OkRhdGU6TWVzc2FnZS1JRDpNSU1FLVZlcnNpb246Q29udGVudC1UeXBlOlgtU0VTLVJFQ0VJUFQ7DQpSZWNlaXZlZDogYnkgbWFpbC1sajEtZjE3MC5nb29nbGUuY29tIHdpdGggU01UUCBpZCBmMTFzbzEyNTMxNTM5bGptLjgNCiAgICAgICAgZm9yIDxkb29yc0BhdXRvbWF0aW9uLmV2ZXJ5dGhpbmdiaWlnLmNvbT47IEZyaSwgMjkgSmFuIDIwMjEgMTY6NDk6NTkgLTA4MDAgKFBTVCkNCkRLSU0tU2lnbmF0dXJlOiB2PTE7IGE9cnNhLXNoYTI1NjsgYz1yZWxheGVkL3JlbGF4ZWQ7DQogICAgICAgIGQ9Z21haWwuY29tOyBzPTIwMTYxMDI1Ow0KICAgICAgICBoPW1pbWUtdmVyc2lvbjpmcm9tOmRhdGU6bWVzc2FnZS1pZDpzdWJqZWN0OnRvOw0KICAgICAgICBiaD1rQVZDMVAra3o5NHNWZmxYcTRsS0Uvbm5zMzVJWGhURlNXb0pMT2orVmxNPTsNCiAgICAgICAgYj1UZk42UkRCeXVzU2g2YlFudVlHWUhIdmNyMmU1OVNpZjc4d29aNVdaTlBudUM1RTRoK0dvTU9VNlpXcEpFM3VtTDMNCiAgICAgICAgIExQeC9hKzR3M0ltdzk1dlhVU1lwVGR2RldwNzFsSUh2SGtWTjViaFQ1ekN1QS9CMkVabmM1VXowQkZpL2VFa0VtWTdLDQogICAgICAgICBWa25LUC9sU2hQYmx1YU9BZExHcnFJRStYZW1UamxRMThQNktpSG5pRXVmM3JwR3JYbnpZZFQ0Zm82UU80TjJaUFFsSQ0KICAgICAgICAgYldrdjdCdXVudSt2S2dMUWdJL3ZyM3VPTFlzY0xJb0lwSUNZdU84NzlLWEVLTUlTSjBTa1Y5QVRYR1ExbGZTODJpcWkNCiAgICAgICAgIGF6clpUU21zK3BUVEJaMlJpZGxVdWErOE1DU1VJSnZrSGJNYlZoUlJLWHhjMzlSclNJR1ozWFZMb3l5OC9UcHFTSlVSDQogICAgICAgICBwTFd3PT0NClgtR29vZ2xlLURLSU0tU2lnbmF0dXJlOiB2PTE7IGE9cnNhLXNoYTI1NjsgYz1yZWxheGVkL3JlbGF4ZWQ7DQogICAgICAgIGQ9MWUxMDAubmV0OyBzPTIwMTYxMDI1Ow0KICAgICAgICBoPXgtZ20tbWVzc2FnZS1zdGF0ZTptaW1lLXZlcnNpb246ZnJvbTpkYXRlOm1lc3NhZ2UtaWQ6c3ViamVjdDp0bzsNCiAgICAgICAgYmg9a0FWQzFQK2t6OTRzVmZsWHE0bEtFL25uczM1SVhoVEZTV29KTE9qK1ZsTT07DQogICAgICAgIGI9Wm15Qy9laU5iaklzZFNFanZNcVovaWpQSWh5NGplV3laaEhrMFAwRFFaZitRZTBiRC9WM2VZYTNRMG1RUFRrTkpNDQogICAgICAgICB5a1MxNnhCQnNzNWZaNXJYMEN1S0F5dEpTKzBhT09wTGsrOVk1K2srN0FEQmNoR3BOWWVLOWdSVFBtWXF3RVhsVkxzdA0KICAgICAgICAgQXpXNXRtSHYrcjVlSDhxT3lHOXUvTjFiYzdEMmRCTE9lODB6NmJReldHQ3Z2WWF2TXl0YkFBZlZjWjBnRnZEWmxyOEwNCiAgICAgICAgIEFIKzFsWjhIcHNlTkQ0SWpyYVBqVGxDd2dDdHZsKzBhZlVaeVZhZjFiNmI3dmNkcG9qeFlQR1lkbDFKQXNvN05wOEt6DQogICAgICAgICBhaGdYc0pCWUk3Z0E3QUQ5WjQyZGtGbVhjQVdyZ01TU2U5L1pRNEVuZDdGZDNyQittVWNTUTlnc2V1NjNOK3QvaDlHMw0KICAgICAgICAgcXg3QT09DQpYLUdtLU1lc3NhZ2UtU3RhdGU6IEFPQU01MzJoZTNLZUI5RzZNSkFvMjk1WTNjby94QlpMVHZCSW5CZ1Vwem1hYnpUa0FTVFBzN0pJDQoJQ0NwYmludGNrM3lXaTJqMHRRV21CQTVDTXBzZmhUNFJVRDd1SEdycldWZ3BoelE9DQpYLUdvb2dsZS1TbXRwLVNvdXJjZTogQUJkaFBKeVhlbXVWWXlxZEFtNklDanl2MVdnZWxtUkxOTXpXbVExbFhFay9JYTh0KzVFQ0JXbUxpeUZTek1pbXMrT2ZmZHZkMkpTTGUrNkllNFJhRE5ndVE0VT0NClgtUmVjZWl2ZWQ6IGJ5IDIwMDI6YTJlOjgwMDU6OiB3aXRoIFNNVFAgaWQgajVtcjM4MTQ3NzFsamcuMzQuMTYxMTk2Nzc5NzUzMTsNCiBGcmksIDI5IEphbiAyMDIxIDE2OjQ5OjU3IC0wODAwIChQU1QpDQpNSU1FLVZlcnNpb246IDEuMA0KRnJvbTogSnVsaW8gU2FudG9zIDxqdWxpby5yLnNhbnRvcy5qckBnbWFpbC5jb20+DQpEYXRlOiBGcmksIDI5IEphbiAyMDIxIDE5OjQ5OjQ2IC0wNTAwDQpNZXNzYWdlLUlEOiA8Q0FKWWtoSC10T0tSYlI5N3FxT1dRdXVRUCtYaFcwbXhGNHUyLVhCZTNGUVJVSzZXaFVRQG1haWwuZ21haWwuY29tPg0KU3ViamVjdDogRHVycnINClRvOiBkb29yc0BhdXRvbWF0aW9uLmV2ZXJ5dGhpbmdiaWlnLmNvbQ0KQ29udGVudC1UeXBlOiBtdWx0aXBhcnQvYWx0ZXJuYXRpdmU7IGJvdW5kYXJ5PSIwMDAwMDAwMDAwMDBmNjE2ZWMwNWJhMTM3Zjc3Ig0KDQotLTAwMDAwMDAwMDAwMGY2MTZlYzA1YmExMzdmNzcNCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbjsgY2hhcnNldD0iVVRGLTgiDQoNCg0KDQotLTAwMDAwMDAwMDAwMGY2MTZlYzA1YmExMzdmNzcNCkNvbnRlbnQtVHlwZTogdGV4dC9odG1sOyBjaGFyc2V0PSJVVEYtOCINCg0KPGRpdiBkaXI9Imx0ciI+PGJyPjwvZGl2Pg0KDQotLTAwMDAwMDAwMDAwMGY2MTZlYzA1YmExMzdmNzctLQ0K\"}",
                "Timestamp": "2021-01-30T00:49:59.809Z",
                "SignatureVersion": "1",
                "Signature": "rRxmphRaFw2ZBzcr5gvKz7KPN6VmmxGlAPPAnQ5TR7mqZbd/HNaEtTMootrq0f0MNihXAor+C2253GPnq9m9nMMccOxBZkBD2dcWnsFhFL9iPe086mqWwKCtlOv5DEv7oPIRW1T6PGTttAUnq4/rSsv9jFncdficwpV5ieJ1oKBBGrzzaDrbuwbm8vEeFa4fwXVkWEcVRPCd2CWF66b4rLSu9VFs7gMu4kaTCCkzNWRkaiFVnNLd4jhSqVe52noE/RrV83qkXIXM+iOBNz5c2oN998oYeXyCiVccWHyrs2Apj4NJY7pbNVrjUlhhvsoDD+F0H42e9WGBMOAZcqVxIg==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:297473205123:adt-email-notifications:6ae6707c-f1f1-4712-a5de-ac8e951b751a",
                "MessageAttributes": {}
            }
            }
        ]
    }

def test_lambda_handler(apigw_event):
    with patch('integrations.notifications.requests') as req_mock:
        resp_mock = MagicMock()
        resp_mock.status_code = 200
        req_mock.get.return_value = resp_mock
        ret = notifications.lambda_handler(apigw_event, "")
        req_mock.get.assert_called_with("https://cloud.hubitat.com/api/UUID_NOT_CONFIGURED/apps/9/devices/139/on?access_token=ACCESS_TOKEN_NOT_CONFIGURED")
