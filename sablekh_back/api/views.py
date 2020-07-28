from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitorSerializer, LibrarySerializer, FileSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from .models import Library, File, DownloadLot, DownloadLot, Like, Visitor
import hashlib
from datetime import datetime
import mimetypes
from string import ascii_letters, digits, punctuation
import zipfile 
import random  
import binascii
from .misc import filter_text
from os import system

from django.conf import settings
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from .models import WHOOSH_SCHEMA

class UserView(APIView):
    def post(self, request):
        data = request.data        
        hash_str = data["username"] + str(datetime.now())
        hashed = hashlib.sha224(hash_str.encode())
        data["hid"] = hashed.hexdigest()
        serializer = VisitorSerializer(data = data)
        if serializer.is_valid():
            obj = serializer.save()
        else:
            return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER) 
        return Response(request.data)

    def get(self, request):
        try:
            user = Visitor.objects.get(username = request.user.username)
            serializer = VisitorSerializer(user)
            data = serializer.data
            return Response(data, status = status.HTTP_302_FOUND)
        except Visitor.DoesNotExist:
            return Response({"error": "not found"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        hid = request.data["hid"]
        try:
            user = Visitor.objects.get(username = request.user.username)
            if user.hid != hid:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
            serializer = VisitorSerializer(user)
            data = serializer.data
            user.delete()
            return Response(data, status = status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "not found"}, status = status.HTTP_404_NOT_FOUND)

class LibraryView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        hash_str = data["title"] + data["description"] + str(datetime.now())
        hashed = hashlib.sha224(hash_str.encode())
        data["hid"] = hashed.hexdigest()
        visitor = Visitor.objects.get(username = request.user.username)
        data["user"] = visitor.hid
        serializer = LibrarySerializer(data =data)
        if serializer.is_valid():
            print (serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER)
    
    def patch(self, request):
        hid = request.data["hid"]
        try:
            library = Library.objects.get(hid = hid)
            library.title = request.data["title"]
            library.description = request.data["description"]
            library.save()
            serializer = LibrarySerializer(library)
            data = serializer.data
            data["deleted"] = False
            return Response(data, status = status.HTTP_200_OK)
        except Library.DoesNotExist:
            return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        hid = request.data["hid"]
        try:
            library = Library.objects.get(username = request.user.username)
            if library.hid != hid:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
            serializer = LibrarySerializer(library)
            data = serializer.data
            data["deleted"] = True
            library.delete()
            return Response(data, status = status.HTTP_200_OK)
        except Library.DoesNotExist:
            return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)

class FileView(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if '_file' not in request.data:
            raise ParseError("Empty content")
        data = request.data
        try:
            library = Library.objects.get(hid = data["library"])
            if library.user.username != request.user.username:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
            if library.no_files >= 10:
                return Response({"error": "library limit of 10 files reached"}, status = status.HTTP_403_FORBIDDEN)
        except Library.DoesNotExist:
            return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)
        data["size"] = data["_file"].size // 1024
        if data["size"] > 31000:
            return Response({"error": "file size larger than 30MB"}, status = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        data["title"] = data["_file"].name
        hash_str = data["title"] + str(datetime.now())
        hashed = hashlib.sha224(hash_str.encode())
        data["hid"] = hashed.hexdigest()
        serializer = FileSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            library.no_files += 1
            library.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER)

    def delete(self, request):
        try:
            file = File.objects.get(hid = request.data["hid"])
            if file.library.user.username == request.user.username:
                serializer = FileSerializer(file)
                data = serializer.data 
                file.delete() 
                system("rm "+file._file.name)
                data["deleted"] = True
                return Response(data, status = status.HTTP_200_OK)
            else:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
        except File.DoesNotExist:
            return Response({"error":"file not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_library(request):
    hid = request.data["hid"]
    try:
        library = Library.objects.get(hid = hid)
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status = status.HTTP_302_FOUND)
    except Library.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_libraries(request):
    try:
        visitor = Visitor.objects.get(username = request.user.username)
        print (visitor)
        libraries = Library.objects.filter(user = visitor)
        print (libraries) 
        serialiers = [LibrarySerializer(library) for library in libraries]
        data = [serializer.data for serializer in serialiers]
        return Response(data, status = status.HTTP_200_OK)
    except Visitor.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_files(request):
    library = Library.objects.get(hid = request.data["hid"])
    if library.user != request.user:
        return Response({"error": "library does not belong to user"}, status = status.HTTP_401_UNAUTHORIZED)
    files = File.objects.filter(library = request.data["hid"])
    if len(files) > 0:
        serializers = [FileSerializer(file) for file in files]
        data = [serializer.data for serializer in serializers]
        # data = [del each["_file"] for each in data_raw]
        return Response(data, status = status.HTTP_302_FOUND)
    return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def download_files(request):
    hids = request.data["hids"].split(",")
    library_hid = request.data["library"]
    try:
        library = Library.objects.get(hid = library_hid)
    except Library.DoesNotExist:
        return Response({"error": "no library with following hid - "+library_hid}, status = status.HTTP_404_NOT_FOUND)
    filenames = []
    for hid in hids:
        try:    
            file_obj = File.objects.get(hid = hid)
        except File.DoesNotExist:
            return Response({"error": "no file with following hid - "+hid}, status = status.HTTP_404_NOT_FOUND)
        if file_obj.library == library:
            filenames.append(file_obj._file.name)
        else:
            return Response({"error": "file and library does not match"}, status = status.HTTP_401_UNAUTHORIZED)
    library = file_obj.library
    filenames.sort()
    try:
        download_lot = DownloadLot.objects.get(files = filenames)
        return Response({"filename": download_lot.zip_name, "by": "found"})
    except DownloadLot.DoesNotExist:
        library_name = filter_text(library.title[:20], punctuation)
        zip_name =  library_name + str(binascii.crc32(str(hids).encode()))+ ".zip"
        jungle_zip = zipfile.ZipFile('downloadable/'+zip_name, 'w')
        for filename in filenames:
            system("cp "+ filename + " .")
            filename = filename.split("/")[1]
            jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
            system("rm "+filename)
        jungle_zip.close()
        if request.user.is_authenticated:
            visitor = Visitor.objects.get(username = request.user.username)
            down_obj = DownloadLot(zip_name = zip_name, visitor = visitor, library = library, files = filenames)
        else:
            down_obj = DownloadLot(zip_name = zip_name, library = library, files = filenames)
        down_obj.save()
        return Response({"filename": "http://localhost/downloadable/"+zip_name, "by": "created"}, status = status.HTTP_201_CREATED)

@api_view(['GET'])
def search(request):
    ix = open_dir("index")
    query = request.data["query"]
    if query is not None and query != "":
        title_parser = QueryParser("title", schema=ix.schema)
        descri_parser = QueryParser("description", schema=ix.schema)
        try:
            title_qry = title_parser.parse(query)
            descri_qry = descri_parser.parse(query)
        except:
            return Response([])
        searcher = ix.searcher()
        results = searcher.search(title_qry, limit = 20)
        descrip_results = searcher.search(descri_qry, limit = 20)
        results.upgrade_and_extend(descrip_results)
    return Response([ dict(result) for result in results])