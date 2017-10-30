import sys

import os

sys.path.append(os.path.realpath('..'))

import mimetypes
from bson.objectid import ObjectId
import gridfs

from util.mongo_util import get_conn
from web.config import logger
from web.config import upload_dir

conn = get_conn()
gfs = gridfs.GridFS(conn)


def store_fs(file):
    fullname = None
    if file:
        try:
            filename = file.filename
            fullname = os.path.join(upload_dir, filename)
            file.save(fullname)
        except Exception as e:
            logger.debug('----store_fs----' + str(e))
    return fullname


def store_gridfs(file):
    obj = None
    if file:
        try:
            filename = file.filename
            extension = filename.split('.')[-1]
            content_type = mimetypes.types_map['.' + extension]
            oid = gfs.put(file, filename=filename, content_type=content_type)
            logger.debug('----oid----' + str(oid))
            obj = {
                'filename': filename,
                'content_type': content_type,
                'id': str(oid)
            }
        except Exception as e:
            logger.debug('----store_gridfs----' + str(e))
    return obj


def read_gridfs(id):
    file = None
    if id and ObjectId.is_valid(id):
        try:
            file = gfs.get(ObjectId(id))
        except Exception as e:
            logger.debug('----read_gridfs----' + str(e))
    return file


def delete_gridfs(id):
    result = None
    if id and ObjectId.is_valid(id):
        try:
            gfs.delete(ObjectId(id))
            result = True
        except Exception as e:
            logger.debug('----delete_gridfs----' + str(e))
            result = False
    return result
