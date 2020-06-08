# importing all the required libraries and funtions
import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import pprint

#import MongoClient
from pymongo import MongoClient
client=MongoClient("mongodb+srv://admuser:7VuVnlAZEYAWYwvP@admistm622-pmipm.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['testdb']
records = db['myData']

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
@app.route('/mostcheckedout/<topn>', methods=['GET'])
def api_mostcheckedout(topn):
    checkout_counts = records.aggregate(
        [{"$group": {"_id": "$Title", "num_checkouts": {"$sum": 1}}}, {"$sort": {"num_checkouts": -1}}, {"$limit": int(topn)}])
    results_json = checkout_counts
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
    <tr><td><b>Title</b></td><td><b>Count of Checkouts</b></td></tr>
    """
    for i in results_json:
        results_html = results_html + "<tr>" \
                                      "<td>" + str(i['_id']) + "</td>" \
                                                           "<td>" + str(i['num_checkouts']) + "</td>" \
                                                                                                    "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


# The explanation is similar to as in the above query. The only changes are for the sql query
@app.route('/nocheckouts', methods=['GET'])
def api_nocheckouts():
    unchecked_books = records.find({"Status": "N/A"})
    results_json = unchecked_books

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
                                      "<td>" + str(i['Title']) + "</td>" \
                                                           "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


# The explanation is similar to as in the first query. The only changes are for the sql query
@app.route('/trendingauthors/<atopn>', methods=['GET'])
def api_topauthors(atopn):
    author_sales = records.aggregate(
        [{"$group": {"_id": "$Author", "num_author_sold": {"$sum": 1}}}, {"$sort": {"num_author_sold": -1}}, {"$skip":2},
         {"$limit": int(atopn)}])
    results_json = author_sales

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
                                      "<td>" + str(i['_id']) + "</td>" \
                                                           "<td>" + str(i['num_author_sold']) + "</td>" \
                                                                                "</tr>"

    results_html = results_html + "</div>" \
                                  "</table>" \
                                  "</body>" \
                                  "</html>"

    return results_html


app.run()


