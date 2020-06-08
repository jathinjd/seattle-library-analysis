# importing all the required libraries and funtions
import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import mysql.connector as mariadb

# Assigning the application to variable app
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# This is the default route. We use get and post methods
@app.route("/", methods=["GET", "POST"])
# function defined in the default route is queries
def queries():
    # The line below gets fetches and displays the html page titled index.html
    render_template("index.html")
    # The html page has text boxes to get inputs from user
    if request.method == 'POST':
        # Extracting the required inputs from the form
        booksnumber = request.form.get("booksnumber")
        authorsnumber = request.form.get("authorsnumber")
        # These if else statement check which api call to make based on user inputs
        if booksnumber != "":
            return redirect(url_for('api_mostcheckedout', topn=booksnumber))

        elif authorsnumber != "":

            return redirect(url_for('api_topauthors', atopn=authorsnumber))
        else:
            return redirect(url_for('api_nocheckouts'))

    return render_template("index.html")


# api for the first query. topn is a variable passed to this.
@app.route('/mostchekedout/<topn>', methods=['GET'])
def api_mostcheckedout(topn):
    # query_parameters = request.args

    # number = query_parameters.get(topn)
    # This is the sql query that we are going to pass to the database
    query = ("SELECT a.BibNumber, b.Title, COUNT(a.BibNumber) "
             "FROM SDL_Checkouts a, SDL_Inventory b "
             "WHERE a.BibNumber = b.BibNum "
             "GROUP BY a.BibNumber ORDER BY COUNT(a.BibNumber) DESC "
             "LIMIT ")
    query = query + str(topn) + ";"
    # The lines below take care of connecting to the required database
    connection = mariadb.connect(host='54.81.212.188',
                                 database='SeattleDataLibrary',
                                 user='harmitjasani@tamu.edu',
                                 password='ADB_ProjectRoxX')
    cursor = connection.cursor()
    # This line executes the query and the lines below convert them into json
    cursor.execute(query)
    results = json.dumps(cursor.fetchall())

    results_json = json.loads(results)
    # The following block of code displays the query results in the form of an html page
    results_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Group 1: ISTM 622-601</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
    </head>
    <body>
    <div class="container">
    <table class="table table-striped"><br>
    <h2>Business Question 1 - Most checked out books</h2>
    <tr><td><b>BibNumber</b></td><td><b>Title</b></td><td><b>Count of Checkouts</b></td></tr>
    """
    for i in results_json:
        results_html = results_html + "<tr>" \
                                      "<td>" + str(i[0]) + "</td>" \
                                                           "<td>" + str(i[1]) + "</td>" \
                                                                                "<td>" + str(i[2]) + "</td>" \
                                                                                                     "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


# The explanation is similar to as in the above query. The only changes are for the sql query
@app.route('/nochekouts', methods=['GET'])
def api_nocheckouts():
    query = "SELECT TITLE FROM SDL_Inventory " \
            "WHERE BibNum NOT IN (SELECT DISTINCT a.BibNumber FROM SDL_Checkouts a) " \
            "AND TRIM(TITLE)<>'';"
    connection = mariadb.connect(host='54.81.212.188',
                                 database='SeattleDataLibrary',
                                 user='harmitjasani@tamu.edu',
                                 password='ADB_ProjectRoxX')
    cursor = connection.cursor()
    cursor.execute(query)
    results = json.dumps(cursor.fetchall())

    results_json = json.loads(results)

    results_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Group 1: ISTM 622-601</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
        </head>
        <body>
        <div class="container">
        <table class="table table-striped"><br>
        <h2>Business Question 2 - Books that have not been checked out</h2>
        <tr><td><b>Title</b></td></tr>
        """

    for i in results_json:
        results_html = results_html + "<tr>" \
                                      "<td>" + str(i[0]) + "</td>" \
                                                           "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


# The explanation is similar to as in the first query. The only changes are for the sql query
@app.route('/trendingauthors/<atopn>', methods=['GET'])
def api_topauthors(atopn):
    query_parameters = request.args

    number = query_parameters.get('Top n Authors')
    query = "SELECT b.Author, COUNT(b.Author)" \
            " FROM sample_demo a, SDL_Inventory b" \
            " WHERE a.CheckoutMonth BETWEEN (MONTH(CURDATE())- 2) AND (MONTH(CURDATE())+1)" \
            " AND a.CheckoutYear = CONVERT(YEAR(CURDATE()), CHAR)" \
            " AND a.BibNumber = b.BibNum" \
            " AND TRIM(b.Author)<>''" \
            " GROUP BY b.Author" \
            " ORDER BY COUNT(b.Author) DESC" \
            " LIMIT "

    query = query + str(atopn) + ";"
    connection = mariadb.connect(host='54.81.212.188',
                                 database='SeattleDataLibrary',
                                 user='harmitjasani@tamu.edu',
                                 password='ADB_ProjectRoxX')
    cursor = connection.cursor()
    cursor.execute(query)
    results = json.dumps(cursor.fetchall())

    results_json = json.loads(results)

    results_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Group 1: ISTM 622-601</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
            </head>
            <body>
            <div class="container">
            <table class="table table-striped"><br>
            <h2>Business Question 3 - Popular Authors</h2>
            <tr><td><b>Author</b></td><td><b>Count of checked out books</b></td></tr>
            """

    for i in results_json:
        results_html = results_html + "<tr>" \
                                      "<td>" + str(i[0]) + "</td>" \
                                                           "<td>" + str(i[1]) + "</td>" \
                                                                                "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


app.run()


