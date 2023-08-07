from django.shortcuts import render,redirect
from django.http import HttpResponse,response
import pymongo
import re
import base64
from pymongo.errors import ConnectionFailure
import requests
import datetime
from django.contrib.sessions.backends.cached_db import SessionStore

class Library:
    def __init__(self):
        self.signupError = False
        self.idError = False
        self.signup = False
        self.login = False
        self.passError = False
        self.logoutOpt = False
        self.signOpt = True
        self.home = True
        self.passSetError = False
        self.issueBook = False
        self.navIssueBook = True
        self.bookSubmit = False
        self.submitBookOpt = True
        self.backHome = False
        self.showBookOpt = True
        self.showIssueBook = False
        self.result = []
        try:
            self.connection = pymongo.MongoClient('mongodb://127.0.0.1:27017')
            self.db = self.connection['Library']
            self.collection = self.db['Admin']
            self.collection2 = self.db['Issued_Books']
            self.response = requests.get('https://www.googleapis.com/books/v1/volumes?q=harry+potter&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.response2 = requests.get('https://www.googleapis.com/books/v1/volumes?q=marvel&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.response3 = requests.get('https://www.googleapis.com/books/v1/volumes?q=pirates&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.response4 = requests.get('https://www.googleapis.com/books/v1/volumes?q=struggle+for+indian+independence&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.response5 = requests.get('https://www.googleapis.com/books/v1/volumes?q=netaji+shubhash+chandra+bose&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.response6 = requests.get('https://www.googleapis.com/books/v1/volumes?q=history&key=AIzaSyCtjHzRLoGmxEthulnfYNOqXSnx8_QevzQ')
            self.api1 = self.response.json()
            self.api2 = self.response2.json()
            self.api3 = self.response3.json()
            self.api4 = self.response4.json()
            self.api5 = self.response5.json()
            self.api6 = self.response6.json()
        except ConnectionFailure:
            print("Could not connect to server")

    # logout url
    def logout(self,request):
            self.login = False
            self.signup = False
            self.issueBook = False
            self.logoutOpt = False
            self.backHome = False
            self.showIssueBook = False
            self.showBookOpt = True
            self.signOpt = True
            self.navIssueBook = True
            self.home = True
            request.session.flush()
            return redirect('/?=returnHome')

    # Home page
    def returnHome(self,request):
        if request.session.has_key('user') and request.session.has_key('password'):
            self.login = False
            self.signup = False
            self.issueBook = False
            self.bookSubmit = False
            self.signOpt = False
            self.backHome = False
            self.showIssueBook = False
            self.logoutOpt = True
            self.showBookOpt = True
            self.submitBookOpt = True
            self.navIssueBook = True
            self.home = True
            return redirect('/?=returnHome')
        else:
            self.login = False
            self.signup = False
            self.backHome = False
            self.issueBook = False
            self.bookSubmit = False
            self.logoutOpt = False
            self.showIssueBook = False
            self.showBookOpt = True
            self.signOpt = True
            self.submitBookOpt = True
            self.navIssueBook = True
            self.home = True
            return redirect('/?=returnHome')
    def homes(self,request):
        return render(request, 'main.html',{
            'signup': self.signup,
            'signupError': self.signupError,
            'idError': self.idError,
            'passError': self.passError,
            'logoutOpt': self.logoutOpt,
            'signOpt': self.signOpt,
            'home': self.home,
            'login': self.login,
            'books1': self.api1,
            'books2': self.api2,
            'books3': self.api3,
            'books4': self.api4,
            'books5': self.api5,
            'books6': self.api6,
            'passSetError': self.passSetError,
            'issueBook': self.issueBook,
            'navIssueBook': self.navIssueBook,
            'bookSubmit': self.bookSubmit,
            'submitBookOpt': self.submitBookOpt,
            'backHome': self.backHome,
            'showBookOpt': self.showBookOpt,
            'showIssueBook': self.showIssueBook,
            'result': self.result
        })

    # Signup page
    def signed(self,request):
        self.home = False
        self.login = False
        self.issueBook = False
        self.signOpt = False
        self.signup = True
        return redirect('/?=signup')

    def sign(self,request):
        if request.method == "POST":
            self.reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
            self.matchRe = re.compile(self.reg)
            self.name = request.POST.get('name')
            self.mobile = request.POST.get('mobile')
            self.email = request.POST.get('email')
            self.password = request.POST.get('password')
            self.resultPass = re.search(self.matchRe, self.password)
            self.passwordEncoded = base64.b64encode(self.password.encode('utf-8'))
            self.data = ({
                'Name': self.name,
                'Mobile_no': self.mobile,
                'Email_id': self.email,
                'Password': self.passwordEncoded
            })
            self.query = {
                "Email_id":self.email
            }
            try:
                self.result = [0]
                for self.x in self.collection.find(self.query):
                    self.result[0] = self.x
                if self.resultPass and self.result[0] == 0 and self.name != "" and self.mobile != "" and self.email != "" and self.password != "":
                    self.passSetError = False
                    self.signupError = False
                    self.idError = False
                    try:
                        self.collection.insert_many([self.data])
                        self.signOpt = False
                        self.logoutOpt = True
                        return redirect("/login?=success")
                    except:
                        print('Insertion in the database is not completed.')
                        return redirect('/?=serverErrFail')
                elif self.result[0] != 0:
                    self.signupError = False
                    self.passSetError = False
                    self.idError = True
                    return redirect("/?=idFoundFail")
                elif self.name == "" or self.mobile == "" or self.email == "" or self.password == "":
                    self.idError = False
                    self.signupError = True
                    return redirect("/?=notAllFillFail")
                else:
                    self.passSetError = True
                    return redirect('/?=passValidFailed')
            except:
                print("Data is not Fetched from the database.")
                return redirect("/?=serverFail")

    # Login page
    def loged(self,request):
        self.signup = False
        self.home = False
        self.issueBook = False
        self.signOpt = False
        self.login = True
        return redirect('/?=success')

    def signin(self,request):
        if request.method == "POST":
            self.email = request.POST.get('email')
            self.password = request.POST.get('password')
            self.query = {
                "Email_id":self.email,
            }
            try:
                self.result = [0]
                for self.x in self.collection.find(self.query):
                     self.result[0] = self.x
                if self.email != '' and self.password != "" and self.result[0] != 0:
                    self.signupError = False
                    self.idError = False
                    self.passwordDecoded = base64.b64decode(self.result[0]['Password']).decode('utf-8')
                    if self.passwordDecoded == self.password:
                        self.passError = False
                        self.logoutOpt = True
                        request.session['user'] = self.email
                        request.session['password'] = self.passwordDecoded
                        return redirect('/returnHome?=success')
                    else:
                        self.passError = True
                        return redirect('/?=passwordFailed')
                elif self.email == '' or self.password == "":
                    self.idError = False
                    self.signupError = True
                    return redirect('/?=idNotFound')
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect('/?=entryNotFull')
            except:
                print("Data is not fetched from the database.")
                return redirect('/?=serverFail')

    # Issue Book page
    def issuedBook(self,request):
        if request.session.has_key('user') and request.session.has_key('password'):
            self.home = False
            self.login = False
            self.signup = False
            self.navIssueBook = False
            self.showIssueBook = False
            self.backHome = True
            self.issueBook = True
            self.showBookOpt = True
            return redirect('/?=issueBook')
        else:
            return redirect('/returnHome?=signinFailed')

    def issuedDetails(self,request):
        try:
            if request.method == 'POST':
                self.search = None
                for i in self.api1['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                for i in self.api2['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                for i in self.api3['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                for i in self.api4['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                for i in self.api5['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                for i in self.api6['items']:
                    if i['volumeInfo']['title'] == request.POST.get('bookName'):
                        self.search = i['volumeInfo']['imageLinks']['thumbnail']
                self.data = {
                    'Student_Name': request.POST.get('studentName'),
                    'Mobile_no': request.POST.get('mobile'),
                    'Library_id': request.POST.get('libraryId'),
                    'Book_Name': request.POST.get('bookName'),
                    'Issue_Date': request.POST.get('date'),
                    'Url': self.search
                }
                self.query = {
                    'Library_id': request.POST.get('libraryId'),
                    'Book_Name': request.POST.get('bookName')
                }
                if request.POST.get('studentName') == '' or request.POST.get('mobile') == '' or request.POST.get('libraryId') == '' or request.POST.get('bookName') == '' or request.POST.get('date') == '':
                    self.idError = Fals_
                    self.signupError = True
                    return redirect('/?=detailsError')
                else:
                    self.signupError = False
                    self.result = None
                    for self.i in self.collection2.find(self.query):
                        self.result = self.i
                    if self.result.get('Submit-Date') != None or self.result == None:
                        self.idError = False
                        self.collection2.insert_many([self.data])
                        return redirect('/?=issueSuccess')
                    else:
                        self.idError = True
                        return redirect('/?=notIssue')

        except:
            print("Some error occured")
            return redirect("/?=errOccured")

    def submitBook(self, request):
        if request.session.has_key('user') and request.session.has_key('password'):
            self.home = False
            self.login = False
            self.signup = False
            self.showIssueBook = False
            self.issueBook = False
            self.submitBookOpt = False
            self.backHome = True
            self.bookSubmit = True
            self.showBookOpt = True
            self.navIssueBook = True
            return redirect('/?=submitBook')
        else:
            return redirect('/returnHome?=signinFailed')

    def submitBookDetails(self, request):
        try:
            if request.method == 'POST':
                self.data = {'$set':{
                    'Submit_Date': request.POST.get('date'),
                }}
                self.query = {
                    'Library_id': request.POST.get('libraryId'),
                    'Book_Name': request.POST.get('bookName')
                }
            if request.POST.get('studentName') == '' or request.POST.get('mobile') == '' or request.POST.get('libraryId') == '' or request.POST.get('bookName') == '' or request.POST.get('date') == '':
                self.idError = False
                self.signupError = True
                return redirect('/?=detailsError')
            else:
                self.signupError = False
                self.result = None
                for self.i in self.collection2.find(self.query):
                    self.result = self.i
                if self.result == None:
                    self.idError = True
                    return redirect('/?=notSubmited')
                else:
                    self.idError = False
                    self.collection2.update_one(self.query,self.data)
                    return redirect('/?=submitSuccessfully')
        except:
            print('There is some error in submit book')
            return redirect('/returnHome?=error')

    def issueBookShow(self, request):
        if request.session.has_key('user') and request.session.has_key('password'):
            self.home = False
            self.login = False
            self.signup = False
            self.navIssueBook = True
            self.issueBook = False
            self.showBookOpt = False
            self.submitBookOpt = True
            self.backHome = True
            self.showIssueBook = True
            self.logoutOpt = True
            self.result.clear()
            for i in self.collection2.find():
                self.result.append(i)
            return redirect('/?=submitBook')
        else:
            return redirect('/?=signinFailed')
