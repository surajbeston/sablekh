from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitorSerializer, LibrarySerializer, FileSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.exceptions import ParseError 
from rest_framework.parsers import FileUploadParser
from .models import Library, File, DownloadLot, Like, Visitor, Tag, PwResetToken
import hashlib
from datetime import datetime
import mimetypes
from string import ascii_letters, digits, punctuation
import zipfile 
import random  
import binascii
from .misc import filter_text, title_to_link
from subprocess import Popen
import django
from django.shortcuts import redirect

from django.conf import settings
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from .models import WHOOSH_SCHEMA

import requests
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from dateutil import tz 
from bs4 import BeautifulSoup

from .thumbnail import generate_thumbnail

from django.contrib.sessions.backends.db import SessionStore

def home(request):
    return redirect("https://sablekh.com")

class UserView(APIView):
    def post(self, request):
        data = request.data
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
            return Response(data, status = status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "not found"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        hid = request.data["hid"]
        try:
            user = Visitor.objects.get(email = request.user.email)
            serializer = VisitorSerializer(user)
            data = serializer.data
            return Response(data, status = status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "not found"}, status = status.HTTP_404_NOT_FOUND)

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
            try:
                library.finished = request.data["finished"]
                files = File.objects.filter(library = library)
                for file in files:
                    thumbnail_file = generate_thumbnail(file._file.name)
                    if thumbnail_file:
                        library.thumbnail = "https://api.sablekh.com/" + thumbnail_file
                        break 
            except KeyError:
                pass    
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
                Popen("rm "+file._file.name, shell = True).wait()
                data["deleted"] = True 
                return Response(data, status = status.HTTP_200_OK)
            else:
                return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
        except File.DoesNotExist:
            return Response({"error":"file not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST']) 
def get_library(request):
    hid = request.data["hid"] 
    try:
        library = Library.objects.get(hid = hid)
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Library.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def all_libraries(request):
    try:
        visitor = Visitor.objects.get(email = request.user.email)
        libraries = Library.objects.filter(user = visitor)
        filtered_libraries = [library for library in libraries if library.finished]
        if len(filtered_libraries) == 0:
            return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)
        serialiers = [LibrarySerializer(library) for library in filtered_libraries]
        data = [serializer.data for serializer in serialiers]
        return Response(data, status = status.HTTP_200_OK)
    except Visitor.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def all_files(request):
    library = Library.objects.get(hid = request.data["hid"])
    files = File.objects.filter(library = request.data["hid"])
    if len(files) > 0:
        serializers = [FileSerializer(file) for file in files]
        data = [serializer.data for serializer in serializers]
        # data = [del each["_file"] for each in data_raw]
        return Response(data, status = status.HTTP_200_OK)
    return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
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
    if (len(filenames) == 1):
        zip_name = filenames[0]
        if request.user.is_authenticated:
            visitor = Visitor.objects.get(email = request.user.email)
            down_obj = DownloadLot(zip_name = zip_name, visitor = visitor, library = library, files = filenames)
        else:
            down_obj = DownloadLot(zip_name = zip_name, library = library, files = filenames)
        down_obj.save()
        return Response({"filename": "https://api.sablekh.com/single-download/"+zip_name.split("/")[1], "by": "created"}, status = status.HTTP_201_CREATED)
    filenames.sort()
    download_lot = DownloadLot.objects.filter(files = filenames)
    if len(download_lot) > 0:
        zip_name = download_lot[0].zip_name
        if request.user.is_authenticated:
            visitor = Visitor.objects.get(email = request.user.email)
            down_obj = DownloadLot(zip_name = zip_name, visitor = visitor, library = library, files = filenames)
        else:
            down_obj = DownloadLot(zip_name = zip_name, library = library, files = filenames)
        down_obj.save()
        return Response({"filename": "https://api.sablekh.com/download/"+zip_name, "by": "found"})
    else:
        library_name = filter_text(library.title[:20], punctuation)
        zip_name =  library_name + str(binascii.crc32(str(hids).encode()))+ ".zip"
        jungle_zip = zipfile.ZipFile('downloadable/'+zip_name, 'w')
        for filename in filenames:
            Popen("cp "+ filename + " .", shell = True).wait()
            filename = filename.split("/")[1]
            jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
            Popen("rm "+filename, shell= True).wait() 
        jungle_zip.close()
        if request.user.is_authenticated:
            visitor = Visitor.objects.get(email = request.user.email)
            down_obj = DownloadLot(zip_name = zip_name, visitor = visitor, library = library, files = filenames)
        else:
            down_obj = DownloadLot(zip_name = zip_name, library = library, files = filenames)
        down_obj.save()
        return Response({"filename": "https://api.sablekh.com/download/"+zip_name, "by": "created"}, status = status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
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
            if obj.tags == None:
                obj_tags = []
            else:
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
            pass 
    if max_tag_score > 0:
        whoosh_per_tag = max_whoosh_score/max_tag_score
    else:
        whoosh_per_tag = 0
    tuple_data = [(whoosh_score+tag_score*whoosh_per_tag, LibrarySerializer(result_obj)) for whoosh_score, tag_score, result_obj in result_objs]
    tuple_data.sort(key = lambda x: x[0], reverse = True) 
    response = [serializer.data for score, serializer in tuple_data]
    new_response = []
    for data in response:
        if data not in new_response:
            new_response.append(data)
    return Response(new_response, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def auth_token(request):
    email, password = request.data["email"], request.data["password"]
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
    return Response({"error": "authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def change_link(request):
    hid = request.data["hid"]
    link_str = request.data["link_str"]
    if len(link_str) < 3:
        return Response({"error": "small link size"}, status = status.HTTP_403_FORBIDDEN)
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

@api_view(['GET', 'POST'])
def string_to_library(request):
    link_str = request.data["link_str"]
    try:
        library = Library.objects.get(link_str = link_str)
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Library.DoesNotExist:
        return Response({"error": "library not found"}, status = status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def send_password_key(request):
    email = request.data["email"]
    try:
        visitor = Visitor.objects.get(email = email)
    except Visitor.DoesNotExist:
        return Response({"error":"email not found"}, status = status.HTTP_404_NOT_FOUND)

    token = ''.join([random.choice(digits+ascii_letters) for _ in range(150)])    
    token_obj = PwResetToken(token = token, user = visitor) 
    token_obj.save()
    link = "https://sablekh.com/reset-password/"+token
    file = open("password_reset.html") 
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    soup.select("#token_link")[0]["href"] = link 
    response = requests.post(
        "https://api.mailgun.net/v3/sablekh.com/messages",
        auth=("api", "f746c538cfc2aa48e43c3ae39bddb827-f7d0b107-ca20f738"),
        data={"from": "Sablekh <noreply@sablekh.com>",
              "to": [email],
              "subject": "Password Reset",
              "text": "Hi, {} please click on the link below to reset password".format(visitor.username),
              "html": str(soup)})
    if response.status_code == 200:
        return Response({"message": "email sent"}, status =status.HTTP_200_OK)
    else:
        return Response({"error": "error sending email"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def reset_password(request):
    token = request.data["token"]
    _type = request.data["type"] 
    try:
        token_obj = PwResetToken.objects.get(token = token)
    except PwResetToken.DoesNotExist:
        return Response({"error": "invalid token"}, status = status.HTTP_404_NOT_FOUND)
    user = token_obj.user 
    if datetime.now(tz = tz.UTC) - token_obj.datetime > timedelta(days = 1) or token_obj.is_used:
        return Response({"error": "token expired", "email": user.email}, status = status.HTTP_403_FORBIDDEN)
    if _type == "test":
        return Response({"message": "token valid", "email": user.email}, status = status.HTTP_200_OK)
    elif _type == "action-change":
        password = request.data["password"]
        user.password = make_password(password)
        user.save() 
        token_obj = False
        token_obj.save()
        return Response({"message": "password reset", "email": user.email}, status= status.HTTP_205_RESET_CONTENT)
    else:
        return Response({"error": "invalid type", "email": user.email}, status = status.HTTP_303_SEE_OTHER)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def like(request):
    data = request.data
    visitor = Visitor.objects.get(email = request.user.email)
    data["user"] = visitor.hid
    serializer = LikeSerializer(data = data)
    if serializer.is_valid():
        obj = serializer.save()
        data["message"] = "like registered"
        return Response(data, status = status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def check_like(request):
    user = Visitor.objects.get(email = request.user.email)
    try:
        like_obj = Like.objects.get(user = user, library = request.data["library"])
        return Response({"library": request.data["library"], "liked": True}, status = status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({"library": request.data["library"],"liked": False}, status = status.HTTP_200_OK)   

@api_view(['GET', 'POST'])
def all_likes(request):
    likes_objs = Like.objects.filter(library = request.data["library"])
    return Response({"library": request.data["library"] ,"likes": len(likes_objs)}, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def all_downloads(request):
    downloads = DownloadLot.objects.filter(library = request.data["library"])
    return Response({"library": request.data["library"], "downloads" : len(downloads)}, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_tags(request):
    tags = Tag.objects.all()
    return Response({"tags":[tag.title for tag in tags]}, status = status.HTTP_200_OK)
