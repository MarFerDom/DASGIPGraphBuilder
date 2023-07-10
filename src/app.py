from flask import Flask, render_template, request, send_file, redirect, make_response, jsonify, send_from_directory
from flask_dropzone import Dropzone
from src import DASGIP_loader, conf, handler, simple_json_db
    
DB = simple_json_db.SimpleJSONDB()
    
PAGE_TITLE = "Eppendorf DASGIP Graph Builder"
_DRAG_DROP_TEXT_ = "(or) Drag and Drop files here."
_VALID_TYPES_ = ['jpeg', 'png', 'jpg', 'gif']
_VAR_COLS_ = 3

app = Flask(__name__)
dropzone = Dropzone(app)

def get_handler(filename: str):
    return handler.Handler(DB.get_content(filename), filename=filename)

@app.route("/")
def index():
    '''
       Main page - displays the drag and drop text for file.
    '''

    if len(DB.get_files()) == 0:
        # If no files are available, redirect to upload page.
        return redirect("/upload", 302)
    else:
        # Load any file to get variables and sources.
        # kept it like this for easy changing when different file contents.
        files = DB.get_files()
        local_handler = get_handler(files[0])
        sources = local_handler.sources
        vars = local_handler.get_variables(sources[0])
        
        # Organize the variables as lines with at most _VAR_COLS_ variables per line.
        lines = [[vars[j*_VAR_COLS_ + i] for i in range(min(len(vars),_VAR_COLS_))
                  if j*_VAR_COLS_ + i < len(vars)]
                  for j in range(len(vars)//_VAR_COLS_ +1)]
        
        # Clear config from nulls
        config = DB.config.copy()
        for key in ('min_map', 'max_map'):
            config[key] = {k:v for k,v in config.get(key, {'': None}).items()
                           if v is not None}

        # Create main page
        response = make_response(render_template("./main_page.html",
                                                 **vars_main,
                                                 files=files,
                                                 **config,
                                                 sources=sources,
                                                 lines=lines)) 
        return response
    
@app.get("/"+conf.API_CONFIG)
def show_config():
    # Check persistant configuration.
    return jsonify(DB.config)

@app.route("/"+conf.API_CONFIG, methods=["POST", "OPTIONS"])
def set_config():
    if request.method == "OPTIONS":
        response = options_response()
    else:
        data = request.json
        # Create the configuration parameters
        cols = []
        min_map = {}
        max_map = {}
        color_map = {}
        for key in data:
            color, min_val, max_val = data[key]
            color_map.update({key: color})
            min_map.update({key: None} if min_val == '' else {key: int(min_val)})
            max_map.update({key: None} if max_val == '' else {key: int(max_val)})
            cols.append(key)
        
        options = {
            "color_map":color_map,
            "min_map":min_map,
            "max_map":max_map,
            "cols": cols
            }
        # Update persistant configuration
        DB.config = options
        DB.commit()
    response = make_response("ok")
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.get("/"+conf.API_UPLOAD)
def upload_get():
    '''
       Uploads the file content and redirects to the selection page.
    '''

    return render_template("./upload.html", **vars_upload)

@app.post("/"+conf.API_UPLOAD)
def upload():
    '''
       Uploads the file content and redirects to the selection page.
    '''

    for file in request.files.getlist('file'):
        filename = ''.join( (c for c in file.filename.split('\\')[-1] \
                             if c.isalnum() or c in ' -_.'))
        # Decode content, remove \r if inserted and break into blocks per vessel
        data_blocks = DASGIP_loader.data_block_loader(
            content=file.read().decode("utf-8").replace("\r",''))
        # Update database with data blocks for each file
        DB.update_content(filename, data_blocks)
    
    DB.commit()
    return redirect("/", 302)

@app.route("/"+conf.API_GRAPH, methods=["POST", "OPTIONS"])
def graph_maker():
    if request.method == "OPTIONS":
        response = options_response()
    else:
        options = DB.config.copy()
        cols = options.pop("cols")
        data = request.json
        if data["files"] == [] or data["sources"] == []:
            response = jsonify({"paths":["test.png"]})
        else:
            files_created = []

            for file in data["files"]:
                local_handler = get_handler(file)
                local_handler.add_option(data=options)
                for source in data["sources"]:
                    files_created.append(
                        local_handler.make_graph(source,local_handler.filter_cols(source, cols))
                        )
            response = jsonify({"paths":files_created})
        response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route("/"+conf.API_LIST_FILES)
def list_files():
    return ';\n'.join(DB.get_files())

@app.get("/"+conf.API_IMGS)
def list_imgs():
    return DB.get_imgs

@app.route("/"+conf.API_IMGS+"<filename>")
def get_img(filename: str):
    filename = filename.split("/")[-1]
    if filename.split('.')[-1] not in _VALID_TYPES_:
        return conf._ERROR_IMG_
    return send_from_directory("../", conf.__IMG_DIR__+filename, mimetype='image/png')

with app.app_context():
    _UPLOAD_PATH_ = conf.API_URL+conf.API_UPLOAD

    vars_upload = {
        "PAGE_TITLE": PAGE_TITLE,
        "_DRAG_DROP_TEXT_": _DRAG_DROP_TEXT_,
        "_UPLOAD_PATH_": _UPLOAD_PATH_
    }

    vars_main = {
        "PAGE_TITLE": PAGE_TITLE,
        "_CONFIG_PATH_": conf.API_URL+conf.API_CONFIG,
        "_UPLOAD_PATH_": _UPLOAD_PATH_,
        "_IMAGES_PATH_": conf.API_URL+conf.API_IMGS,
        "_GRAPH_PATH_": conf.API_URL+conf.API_GRAPH
    }


def options_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == "__main__":
    app.run(debug=False, port=conf.API_PORT)
