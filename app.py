import os

from flask import Flask, request, abort

from query import Query
from constants import DATA_DIR

app = Flask(__name__)


@app.route("/perform_query/", methods=['GET', 'POST'])
def perform_query():
    file_name = os.path.join(DATA_DIR, request.args.get('file_name', 'apache_logs.txt'))
    if not os.path.isfile(file_name):
        abort(400)

    cmd1 = request.args.get('cmd1')
    value1 = request.args.get('value1')

    cmd2 = request.args.get('cmd2')
    value2 = request.args.get('value2')

    result = Query(file_name, cmd1, value1, cmd2, value2).implement_request()
    return app.response_class(result, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)