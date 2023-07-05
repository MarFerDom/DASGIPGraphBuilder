from flask import Flask, render_template, request, send_file, session, redirect, make_response, url_for, render_template_string, jsonify
from flask_session import Session
from markupsafe import escape
from flask_dropzone import Dropzone
from src import handler

PAGE_TITLE = "Eppendorf DASGIP Graph Builder"
_DRAG_DROP_TEXT_ = "(or) Drag and Drop files here."
_VALID_TYPES_ = ['jpeg', 'png', 'jpg', 'gif']

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

dropzone = Dropzone(app)
Session(app)

def get_handler(filename: str):
    return handler.Handler(session.get(filename).replace('\r',''), from_content=True)

@app.route("/")
def index():
    '''
       Main page - displays the drag and drop text for file.
    '''

    print(session.keys())
    return render_template("./index.html", **vars)

@app.route("/upload", methods=["POST"])
def upload():
    '''
       Uploads the file content and redirects to the selection page.
    '''

    file = request.files["file"]
    # If received file is not empty save in session.
    if file:
        filename = ''.join(
            (c for c in file.filename.split('\\')[-1] if c.isalnum() or c in ' -_.'))
        print(f'Got file {filename} with {len(filename) = }, {type(filename)}')
        session[filename] = file.read().decode('utf-8')
    else:
        # return to main page.
        return redirect("/", 302)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file.save("./working_file.csv")
    return render_template("./selection.html", **vars, FILE_NAME=filename,
                           sources=get_handler(filename).sources)

@app.route("/graph")
def graphs():
    print(session.keys())
    return '; '.join(session.keys())

@app.route("/graph/<filename>")
def graph(filename: str):
    print(f'filename is {filename}')
    source_list = "; ".join(get_handler(filename).sources)
    response = make_response(source_list)
    response.headers.add('Access-Control-Allow-Origin', '/upload')
    return response

@app.route("/graph/<filename>/vessel/<id>")
def get_vars(filename: str, id: str):
    #filename = list(session.keys())[0]
    print(f'filename is {filename}, id is {id}')
    response = make_response(jsonify(get_handler(filename).get_variables(id)))
    response.headers.add('Access-Control-Allow-Origin', '/upload')
    return response

@app.route("/graph/<filename>/vessel/<id>", methods=["POST"])
def get_graph(filename: str, id: str):
    data = request.json
    color_map = {k:v[0] for k,v in data.items()}
    min_map = {k:int(v[1]) for k,v in data.items() if v[1] != ''}
    max_map = {k:int(v[2]) for k,v in data.items() if v[2] != ''}
    local_handler = get_handler(filename)
    local_handler.add_option("color_map", color_map)
    local_handler.add_option("min_map", min_map)
    local_handler.add_option("max_map", max_map)
    cols = local_handler.filter_cols(id, list(data.keys()))
    return jsonify(local_handler.make_graph(id, cols))
    #return jsonify({'test':list(data.keys())})

@app.route("/file/<filename>")
def get_file(filename: str):
    filename = filename.split("/")[-1]
    if filename.split('.')[-1] not in _VALID_TYPES_:
        return "Invalid file type"
    return send_file("../"+filename, mimetype='image/png')

with app.app_context():
    _UPLOAD_PATH_ = "http://localhost/upload"

    vars = {
        "PAGE_TITLE": PAGE_TITLE,
        "_DRAG_DROP_TEXT_": _DRAG_DROP_TEXT_,
        "_UPLOAD_PATH_": _UPLOAD_PATH_
    }
if __name__ == "__main__":
    app.run(debug=True)
