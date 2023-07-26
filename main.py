import traceback

from extract import Extractor
from transform import ResponseObject
from load import LoadService

from config import conn



if __name__ == '__main__':
    for eachfile in Extractor().names:

        try:
            data = ResponseObject(eachfile)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e)
            for frame in tb.stack:
                print(f"File: {frame.filename}, Line: {frame.lineno}, Function: {frame.name}")
                if frame.locals:
                    print(f"Local variables: {frame.locals}")
            print(f"Exception: {str(e)}")

        try:
            LoadService(data, conn.cursor()).loads()
        except Exception as e:
            print(e)
            print(eachfile)