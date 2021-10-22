from flask import Flask, request
books = []
app = Flask(__name__)


@app.route('/')
def hello():
    q = request.args.get('q')
    print(q)
    return {"message": "Hello!"}, 201


@app.route('/book', methods=['POST', 'GET', 'PUT', 'DELETE'])
def book():
    try:
        if request.method == 'POST':
            body = request.get_json()
            try:
                if len(books) > 0:
                    for i, book in enumerate(books):
                        if str(book['title']).lower() == str(body['title']).lower():
                            return {"message": "Duplicate Title Book", "body": None}, 400
                books.append(body)
                return {"message": "Book already add to database", "body": body}, 201
            except Exception as e:
                return {"message": "Exception: " + e, "body": None}, 404
        elif request.method == 'GET':
            return {"books": books}, 200
        elif request.method == 'PUT':
            body = request.get_json()
            for i, book in enumerate(books):
                if book['id'] == body['id']:
                    books[i] = body
            return {"message": "Book has been replace", "body": body}, 200
        elif request.method == 'DELETE':
            deleteId = request.args.get('id')
            for i, book in enumerate(books):
                if int(book['id']) == int(deleteId):
                    books.pop(i)
            return {"message": "Book is deleted"}, 200
    except Exception as e:
        print(e)
# app.run()
