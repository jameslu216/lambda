import json
import traceback
import logging
import datetime

def handler(event, context, ex):
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    
    err = {
        "customError":"AWSLambda",
        "timestamp": str(datetime.datetime.now()),
        "logLevel": logging.getLevelName(logging.ERROR),
        "type": type(ex).__name__,
        "message": str(ex),
        "traceback": traceback.format_exc(),
        "context": str(context),
        "event": event
    }
    
    print(json.dumps(err))
    return ex
    