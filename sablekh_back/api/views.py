from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitorSerializer, LibrarySerializer, FileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from .models import Library, File, DownloadLot, Like, Visitor, Tag
import hashlib
from datetime import datetime
import mimetypes
from string import ascii_letters, digits, punctuation
import zipfile 
import random  
import binascii
from .misc import filter_text, title_to_link
from os import system
import django

from django.conf import settings
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from .models import WHOOSH_SCHEMA

class UserView(APIView):
    def post(self, request):
        supposed_username = data["email"].split("@")[0] 
        while True:
            try:
                user = Visitor.objects.get(username = supposed_username) 
                supposed_username += random.choice(digits) 
            except Visitor.DoesNotExist:
                data["username"] = supposed_username 
                break 
        hash_str = data["username"] + str(datetime.now())
        hashed = hashlib.sha224(hash_str.encode())
        data["hid"] = hashed.hexdigest()
        serializer = VisitorSerializer(data = data)
        if serializer.is_valid():
            obj = serializer.save()
        else:
            return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER) 
        return Response(serializer.data, status = status.HTTP_200_OK)

    def get(self, request):
        try:
            user = Visitor.objects.get(email = request.user.email)
            serializer = VisitorSerializer(user)
            data = serializer.data
            return Response(data, status = status.HTTP_302_FOUND)
        except Visitor.DoesNotExist:
            return Response({"error": "not found"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        hid = request.data["hid"]
        try:
            user = Visitor.objects.get(email = request.user.email)
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
        visitor = Visitor.objects.get(email = request.user.email)
        data["user"] = visitor.hid
        serializer = LibrarySerializer(data =data)
        data["link_str"] = title_to_link(data["title"], punctuation)
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
            library.tags = request.data["tags"]
            library.save()
            serializer = LibrarySerializer(library) 
            data = serializer.data
            data["deleted"] = False
            return Response(data, status = status.HTTP_200_OK)
        except Library.DoesNotExist:
            return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        hid = request.data["hid"]
        print (hid)
        try:
            library = Library.objects.get(hid = hid)
            if library.user.email != request.user.email:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
            serializer = LibrarySerializer(library)
            data = serializer.data
            data["deleted"] = True
            library.delete()
            ix = open_dir("index")
            ix.delete_by_term("hid", data["hid"])
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
            if library.user.email != request.user.email:
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
            if file.library.user.email == request.user.email:
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
        visitor = Visitor.objects.get(email = request.user.email)
        libraries = Library.objects.filter(user = visitor)
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
    filenames = [    ]
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
            visitor = Visitor.objects.get(email = request.user.email)
            down_obj = DownloadLot(zip_name = zip_name, visitor = visitor, library = library, files = filenames)
        else:
            down_obj = DownloadLot(zip_name = zip_name, library = library, files = filenames)
        down_obj.save()
        return Response({"filename": "http://localhost/downloadable/"+zip_name, "by": "created"}, status = status.HTTP_201_CREATED)

@api_view(['GET'])
def search(request):
    ix = open_dir("index")
    query = request.data["query"]
    tags = request.data["tags"]
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
    result_objs = []
    max_whoosh_score  = 0
    max_tag_score = 0
    for result in results:
        try:
            obj = Library.objects.get(hid = result["hid"])
            tag_score = 0
            obj_tags = obj.tags
            for obj_tag in obj_tags:
                if obj_tag in tags:
                    tag_score += 1
            if tag_score > max_tag_score:
                max_tag_score = tag_score
            if result.score > max_whoosh_score:
                max_whoosh_score = result.score
            result_objs.append((result.score, tag_score, obj))
        except Library.DoesNotExist:
            print ("reached here")
            pass 
    if max_tag_score > 0:
        whoosh_per_tag = max_whoosh_score/max_tag_score
    else:
        whoosh_per_tag = 0 
    tuple_data = [(whoosh_score+tag_score*whoosh_per_tag, LibrarySerializer(result_obj)) for whoosh_score, tag_score, result_obj in result_objs]
    tuple_data.sort(key = lambda x: x[0], reverse = True) 
    return Response([serializer.data for score, serializer in tuple_data], status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def auth_token(request):
    email, password = request.data["email"], request.data["password"]
    print ("reahed here")
    if email is not None and password is not None:
        user = get_object_or_404(Visitor, email = email)
        auth_user = authenticate(username= user.username, password = password)
        if auth_user is not None:
            try:
                token = Token.objects.get(user = auth_user) 
                return Response({"token": token.key}, status = status.HTTP_200_OK) 
            except Token.DoesNotExist:
                hash_str = ''.join(random.sample(ascii_letters + digits + str(datetime.now()), 13))
                hashed = hashlib.sha256(hash_str.encode())
                token = Token(user = auth_user, key = hashed.hexdigest())
                token.save()
                return Response({"token": hashed.hexdigest()}, status = status.HTTP_200_OK)
    return Response({"error": "authentication failed"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def change_link(request):
    hid = request.data["hid"]
    link_str = request.data["link_str"]
    try:
        library = Library.objects.get(hid = hid)
        if library.user.email == request.user.email:
            library.link_str = filter_text(link_str, punctuation, "-")
            try:
                library.save()
            except django.db.utils.IntegrityError:
                return Response({"error": "link string already exists"}, status = status.HTTP_403_FORBIDDEN)
            serializer = LibrarySerializer(library)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"error": "user and library does not match"}, status = status.HTTP_401_UNAUTHORIZED)
    except Library.DoesNotExist:
        return Response({"error": "library not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def string_to_library(request):
    link_str = request.data["link_str"]
    try:
        library = Library.objects.get(link_str = link_str)
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Library.DoesNotExist:
        return Response({"error": "library not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tags(request):
    tags = Tag.objects.all()
    return Response([tag.title for tag in tags], status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def hawa(request):
    return Response({"hawa": "hawa"})