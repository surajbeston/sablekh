from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitorSerializer, LibrarySerializer, FileSerializer, LikeSerializer, LibraryGroupSerializer, FavouriteLibraryGroupSerializer, FavouriteLibrarySerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.exceptions import ParseError 
from rest_framework.parsers import FileUploadParser
from .models import Library, File, DownloadLot, Like, Visitor, Tag, PwResetToken, LibraryGroup, FavouriteLibrary, FavouriteLibraryGroup
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
import math
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
                library.searchable = request.data["searchable"]
            except KeyError:
                pass 
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
        if data["size"] > 52000:
            return Response({"error": "file size larger than 50MB"}, status = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
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

class LibraryGroupView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = Visitor.objects.get(email = request.user.email)
        data["user"] = user.hid
        data["link_str"] = title_to_link(data["title"], punctuation)
        hash_str = data["title"] + data["description"] + str(datetime.now())
        hashed = hashlib.sha224(hash_str.encode())
        data["hid"] = hashed.hexdigest()
        libraries = data["libraries"].split(",")
        del data["libraries"]
        serializer = LibraryGroupSerializer(data = data)
        if serializer.is_valid():
            library_group = serializer.save()
            for library in libraries:
                try:
                    library_obj = Library.objects.get(hid = library)
                except Library.DoesNotExist:
                    return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)
                library_group.libraries.add(library_obj)
            library_group.save()
            library_group.no_libraries = len(library_group.libraries.all())
            library_group.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_303_SEE_OTHER)

    def put(self, request):
        data = request.data
        try:
            library_group = LibraryGroup.objects.get(hid = data["hid"])
        except LibraryGroup.DoesNotExist:
            return Response({"error":"library group not found"}, status = status.HTTP_404_NOT_FOUND)
        if library_group.user.email != request.user.email:
            return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
        library_group.title, library_group.description, library_group.tags = data["title"], data["description"], data["tags"]
        for library in data["libraries"].split(","):
            try:
                library_obj = Library.objects.get(hid = library)
            except Library.DoesNotExist:
                return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)
            library_group.libraries.add(library_obj)
        library_group.save()
        library_group.no_libraries = len(library_group.libraries.all())
        library_group.save()
        serializer = LibraryGroupSerializer(library_group)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def delete(self, request):
        data = request.data
        try:
            library_group = LibraryGroup.objects.get(hid = data["hid"])
        except LibraryGroup.DoesNotExist:
            return Response({"error":"library group not found"}, status = status.HTTP_404_NOT_FOUND)
        if library_group.user.email != request.user.email:
            return Response({"error": "not authorized"}, status = status.HTTP_401_UNAUTHORIZED)
        serializer = LibraryGroupSerializer(library_group)
        data_to_send = serializer.data
        library_group.delete()
        data_to_send["deleted"] = True
        return Response(data_to_send, status = status.HTTP_200_OK)

class FavouriteLibraryView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            page = request.data["page"]
        except KeyError:
            page = 1
        user = Visitor.objects.get(email=request.user.email)
        all_favourites = FavouriteLibrary.objects.filter(user = user)[(page-1)*10:page*10]
        total_page = math.ceil(len(all_favourites)/10)
        data = []
        for favourite in all_favourites:
            library_serializer = LibrarySerializer(favourite.library)
            favourite_serializer = FavouriteLibrarySerializer(favourite)
            each = favourite_serializer.data
            likes_objs = Like.objects.filter(library = favourite.library)
            downloads = DownloadLot.objects.filter(library = favourite.library)
            each["library"], each["likes"], each["downloads"] = library_serializer.data, len(likes_objs), len(downloads)
            data.append(each)
        response = {"data": data,"page": page,"total_page": total_page, "number": len(data)}
        return Response(response, status = status.HTTP_200_OK)

    def put(self, request):
        data = request.data 
        try:
            library = Library.objects.get(hid = data["hid"])
        except Library.DoesNotExist:
            return Response({"error":"library group not found"}, status = status.HTTP_404_NOT_FOUND)
        user = Visitor.objects.get(email=request.user.email)
        all_favourites = FavouriteLibrary.objects.filter(user = user)
        all_favourite_libraries = [favourite.library for favourite in all_favourites]
        if library not in all_favourite_libraries:
            favourite = FavouriteLibrary(user = user, library= library)
            favourite.save()
        else:
            favourite = FavouriteLibrary.objects.get(user = user, library = library)
        serializer = FavouriteLibrarySerializer(favourite)
        data = serializer.data
        data["created"] = True
        return Response(data, status = status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        try:
            library = Library.objects.get(hid = data["hid"])
        except Library.DoesNotExist:
            return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)
        user = Visitor.objects.get(email=request.user.email)
        try:
            favourite = FavouriteLibrary.objects.get(user = user, library = library)
        except FavouriteLibrary.DoesNotExist:
            return Response({"error": "favourite library not found"}, status = status.HTTP_404_NOT_FOUND)
        serializer = FavouriteLibrarySerializer(favourite)
        data = serializer.data
        favourite.delete()
        data["deleted"] = True
        return Response(data, status = status.HTTP_200_OK)

class FavouriteLibraryGroupView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            page = request.data["page"]
        except KeyError:
            page = 1
        user = Visitor.objects.get(email=request.user.email)
        all_favourites = FavouriteLibraryGroup.objects.filter(user = user)[(page-1)*10:page*10]
        total_page = math.ceil(len(all_favourites)/10)
        data = []
        for favourite in all_favourites:
            library_serializer = LibraryGroupSerializer(favourite.library_group)
            favourite_serializer = FavouriteLibraryGroupSerializer(favourite)
            each = favourite_serializer.data
            each["library_group"] = library_serializer.data
            data.append(each)
        response = {"data": data,"page": page,"total_page": total_page, "number": len(data)}
        return Response(response, status = status.HTTP_200_OK)

    def put(self, request):
        data = request.data 
        try:
            library_group = LibraryGroup.objects.get(hid = data["hid"])
        except LibraryGroup.DoesNotExist:
            return Response({"error":"library not found"}, status = status.HTTP_404_NOT_FOUND)
        user = Visitor.objects.get(email=request.user.email)
        all_favourites = FavouriteLibraryGroup.objects.filter(user = user)
        all_favourite_library_groups = [favourite.library_group for favourite in all_favourites]
        if library_group not in all_favourite_library_groups:
            favourite = FavouriteLibraryGroup(user = user, library_group= library_group)
            favourite.save()
        else:
            favourite = FavouriteLibraryGroup.objects.get(user = user, library_group = library_group)
        serializer = FavouriteLibraryGroupSerializer(favourite)
        data = serializer.data
        data["created"] = True
        return Response(data, status = status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        try:
            library_group = LibraryGroup.objects.get(hid = data["hid"])
        except LibraryGroup.DoesNotExist:
            return Response({"error":"library group not found"}, status = status.HTTP_404_NOT_FOUND)
        user = Visitor.objects.get(email=request.user.email)
        try:
            favourite = FavouriteLibraryGroup.objects.get(user = user, library_group = library_group)
        except FavouriteLibraryGroup.DoesNotExist:
            return Response({"error": "favourite library group not found"}, status = status.HTTP_404_NOT_FOUND)
        serializer = FavouriteLibraryGroupSerializer(favourite)
        data = serializer.data
        favourite.delete()
        data["deleted"] = True
        return Response(data, status = status.HTTP_200_OK)


@api_view(['GET', 'POST']) 
def get_library(request):
    hid = request.data["hid"]
    try:
        library = Library.objects.get(hid = hid)
        serializer = LibrarySerializer(library)
        data = serializer.data
        files = File.objects.filter(library = library)
        if len(files) > 0:
            serializers = [FileSerializer(file) for file in files]
            files_data = [serializer.data for serializer in serializers]
            data["files"] = files_data
        else:
            data["files"] = []
        likes_objs = Like.objects.filter(library = library)
        downloads = DownloadLot.objects.filter(library = library)
        data["likes"], data["downloads"], data["username"] = len(likes_objs), len(downloads), library.user.username
        return Response(data, status = status.HTTP_200_OK) 
    except Library.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def all_libraries(request):
    try:
        page = int(request.data["page"])
        if page < 1:
            return Response({"error": "invalid page number"}, status = status.HTTP_303_SEE_OTHER)
    except KeyError:
        page = 1
    try:
        visitor = Visitor.objects.get(email = request.user.email)
        libraries = Library.objects.filter(user = visitor, finished = True)
        pages = math.ceil(len(libraries)/10)
        libraries = libraries[(page-1)*10:page*10]
        # filtered_libraries = [library for library in libraries if library.finished]
        if len(libraries) == 0:
            return Response({"error":"no library found"}, status = status.HTTP_404_NOT_FOUND)
        serializers = [LibrarySerializer(library) for library in libraries]
        _libraries = [serializer.data for serializer in serializers]
        for data in _libraries:
            likes_objs = Like.objects.filter(library = data["hid"])
            downloads = DownloadLot.objects.filter(library = data["hid"])
            data["likes"], data["downloads"] = len(likes_objs), len(downloads)
        to_send = {"data": _libraries, "page": page, "total_pages": pages, "number": len(_libraries)}
        return Response(to_send, status = status.HTTP_200_OK)
    except Visitor.DoesNotExist:
        return Response({"error":"not found"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def all_library_groups(request):
    try:
        page = int(request.data["page"])
        if page < 1:
            return Response({"error": "invalid page number"}, status = status.HTTP_303_SEE_OTHER)
    except KeyError:
        page = 1
    visitor = Visitor.objects.get(email = request.user.email)
    library_groups = LibraryGroup.objects.filter(user = visitor)
    pages = math.ceil(len(library_groups)/10)
    library_groups = library_groups[(page-1)*10:page*10]
    if len(library_groups) == 0:
            return Response({"error":"no library group found"}, status = status.HTTP_404_NOT_FOUND)
    serializers = [LibraryGroupSerializer(library_group) for library_group in library_groups]
    data = [serializer.data for serializer in serializers]
    for group in data:
        libraries = []
        for library in group["libraries"]:
            try:
                library_obj = Library.objects.get(hid = library)
                serializer = LibrarySerializer(library_obj)
                library_data = serializer.data
                likes_objs = Like.objects.filter(library = library_data["hid"])
                downloads = DownloadLot.objects.filter(library = library_data["hid"])
                library_data["likes"], library_data["downloads"] = len(likes_objs), len(downloads)
                libraries.append(library_data)
            except Library.DoesNotExist:
                pass
        group["libraries"] = libraries
    to_send = {"data": data, "page": page, "total_pages": pages, "number": len(data)}
    return Response(to_send, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def get_library_group(request):
    data = request.data
    try:
        library_group = LibraryGroup.objects.get(link_str = data["link_str"])
    except LibraryGroup.DoesNotExist:
        return Response({"error": "no library group found"}, status = status.HTTP_404_NOT_FOUND)
    serializer = LibraryGroupSerializer(library_group)
    data = serializer.data
    libraries = []
    for library in data["libraries"]:
        try:
            library_obj = Library.objects.get(hid = library)
            serializer = LibrarySerializer(library_obj)
            library_data = serializer.data 
            likes_objs = Like.objects.filter(library = library_data["hid"])
            downloads = DownloadLot.objects.filter(library = library_data["hid"])
            library_data["likes"], library_data["downloads"] = len(likes_objs), len(downloads)
            libraries.append(library_data)
        except Library.DoesNotExist:
            pass 
    data["libraries"] = libraries
    return Response(data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def check_favourite_library(request):
    data = request.data
    try:
        library = Library.objects.get(hid = data["hid"])
    except Library.DoesNotExist:
        return Response({"error": "library does not exists"}, status = status.HTTP_404_NOT_FOUND)
    try:
        user = Visitor.objects.get(email = request.user.email)
        favourite = FavouriteLibrary.objects.get(user = user, library=library)
        serializer = LibrarySerializer(favourite.library)
        data = serializer.data
        data["exists"] = True
    except FavouriteLibrary.DoesNotExist:
        data = {"exists": False}
    return Response(data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def check_favourite_library_group(request):
    data = request.data
    try:
        library_group = LibraryGroup.objects.get(hid = data["hid"])
    except LibraryGroup.DoesNotExist:
        return Response({"error": "library group does not exists"}, status = status.HTTP_404_NOT_FOUND)
    try:
        user = Visitor.objects.get(email = request.user.email)
        favourite = FavouriteLibraryGroup.objects.get(user = user, library_group=library_group)
        serializer = LibraryGroupSerializer(favourite.library_group)
        data = serializer.data
        data["exists"] = True
    except FavouriteLibraryGroup.DoesNotExist:
        data = {"exists": False}
    return Response(data, status = status.HTTP_200_OK)


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
    try:
        page = request.data["page"]
    except KeyError:
        page = 1
    if query is not None and query != "":
        title_parser = QueryParser("title", schema=ix.schema)
        descri_parser = QueryParser("description", schema=ix.schema)
        tags_parser = QueryParser("tags", schema = ix.schema)
        try:
            title_qry = title_parser.parse(query)
            descri_qry = descri_parser.parse(query)
            tags_qry = tags_parser.parse(query)
        except:
            return Response([])
        searcher = ix.searcher()
        results = searcher.search(title_qry)
        descrip_results = searcher.search(descri_qry)
        tags_results = searcher.search(tags_qry)
        results.upgrade_and_extend(descrip_results)
        results.upgrade_and_extend(tags_results)
    if results.has_exact_length():
        len_results = len(results)
    else:
        len_results = results.estimated_length()
    total_page = math.ceil(len_results/10)
    results = results[(page-1)*10:page*10]
    data = []
    hids = []
    for result in results:
        if result["hid"] not in hids:
            try:
                library = Library.objects.get(hid = result["hid"])
                serializer = LibrarySerializer(library)
                library_data = serializer.data
                likes_objs = Like.objects.filter(library = library)
                downloads = DownloadLot.objects.filter(library = library)
                library_data["likes"], library_data["downloads"] = len(likes_objs), len(downloads)
                data.append(library_data)
                hids.append(result["hid"])
            except Library.DoesNotExist:
                pass
    response = {"data": data, "page": page, "total_page": total_page, "number": len(data)}
    return Response(response, status = status.HTTP_200_OK)

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
        data = serializer.data
        files = File.objects.filter(library = library)
        if len(files) > 0:
            serializers = [FileSerializer(file) for file in files]
            files_data = [serializer.data for serializer in serializers]
            data["files"] = files_data
        else:
            data["files"] = []
        likes_objs = Like.objects.filter(library = library)
        downloads = DownloadLot.objects.filter(library = library)
        data["likes"], data["downloads"], data["username"] = len(likes_objs), len(downloads), library.user.username
        return Response(data, status = status.HTTP_200_OK)
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
