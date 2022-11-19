import os

from flask import Flask, render_template, jsonify

from flask import url_for
from flask import request

# <script type="text/javascript" {{ url_for('static', filename='app.js')}}></script>
from flaskr.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/' , methods=['GET', 'POST'])
    def hello2():
    #    videoID = ""
    #    videoID = remove_song()
        if request.method == 'POST':
            print("POSTED")
            list1 = database_to_list()
            return(list1)

        print(database_to_list())
    #    videoID = "0Bmhjf0rKe8"
        list1 = database_to_list()
        return render_template('settings.html', data=list1)

    # a simple page that says hello
    @app.route('/del' , methods=['GET', 'POST'])
    def admin_how_to_delet():
        del_all()
        return "<p> yourmom </p>"

    @app.route('/sr' , methods=['GET', 'POST'])
    def sr():
        if request.method == 'POST':
            print("POSTED")
            add_song(request.json['data'])
            print("requested")
            print(request.json)
            return("success")

    @app.route('/skip' , methods=['GET', 'POST'])
    def skip():
        if request.method == 'GET':
            remove_song()
            return("success")


    @app.route('/test' , methods=['GET', 'POST'])
    def test():
        list3 = ["kok" , "bok" , "xol" , 420 , "KMFLnlg883I"]
        add_song(list3)
        return("koksimus")



    @app.route('/hello' , methods=['GET', 'POST'])
    def hello():
        if request.method == 'POST':
            print("Postad")
            videoID = remove_song()
            list1 = database_to_list()
            return jsonify({"data": [list1 , videoID]})


        url_for('static', filename='style.css')
        #return "<p>your mom fat and gae</p>"
        dict1 = make_entry("♂ Leave The Gachimuchi On ♂" , "Duyui" , "xalhs" , 420 )
        dict2 = make_entry("♂ it's so it's so it's so ♂" , "kev" , "yourmom" , 360 )
        list4 = ["♂ it's so it's so it's so ♂" , "kev" , "yourmom" , 360 , "xeM4JK0bX5s" ]
        list3 = ["♂ Leave The Gachimuchi On ♂" , "Duyui" , "xalhs" , 420 , "BH726JXRok0"]
        add_song(list3)
        add_song(list4)
        list1=[dict1, dict2]
    #    list1 = queue.Queue(maxsize=1000)
    #    list1.put(dict1)
    #    list1.put(dict2)#[dict1 , dict2]

    #    remove_song()
    #    remove_song()
    #    if request.method == 'POST':
    #        print("GAE"*50)
    #        list1.pop(0)
            #return "I hate you"
        sitecode = generate_sitecode(list1 , "0Bmhjf0rKe8")
        return sitecode

    from . import db
    db.init_app(app)

    return app

def list_to_string(list1):
    temp = "list1 = list1 + ["
    for item in list1:
        temp += """
        + '{title: """ + item['title'] + """, uploader: """ + item['uploader'] + """, user:""" + item['user'] + """, length: """ + str(item['length']) + """},'
        """
    temp += "]"
    return temp

def generate_sitecode(list1 , videoID):

    tablehead = """<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">title</th>
      <th scope="col">uploader</th>
      <th scope="col">requested by</th>
      <th scope="col">length</th>
    </tr>
  </thead>
  <tbody>
    """
    tableend = """</tbody>
</table>"""
    tablemid = ""
    for i,item in enumerate(list1):
        tablemid += """<tr>
          <th scope="row">""" + str(i+1) + """</th>
          <td>""" +item["title"] +"""</td>
          <td>""" + item["uploader"] +"""</td>
          <td>""" + item["user"] +"""</td>
          <td>""" + str(item["length"]) +"""</td>
        </tr>
        """
    table = tablehead + tablemid + tableend

    #<iframe width="560" height="315" src="https://www.youtube.com/embed/vnesoY1s8Sc" title="YouTube video player"
#    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

    print(videoID + "kkeeeek")
    print(type(videoID))
    sitecode = """

    <div id="player"></div>

<script src="http://www.youtube.com/player_api"></script>

<script>
    var list1 = []
    """ + list_to_string(list1) + """
    var videoID = """ + videoID + """

    // create youtube player
    var player;
    function onYouTubePlayerAPIReady() {
        player = new YT.Player('player', {
          height: '390',
          width: '640',
          videoId: videoID,
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
    }

    // autoplay video
    function onPlayerReady(event) {
        event.target.playVideo();
    }

    // when video ends
    var done = false;
      function onPlayerStateChange(event) {
      if(event.data === 0) {
            alert('done');
            fetch("http://127.0.0.1:5000", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                    first_name: "yourmom",
                    last_name: "nword",
                    age: "fgt"
                })
            })
            .then(response)

        }
    //    if (event.data == YT.PlayerState.PLAYING && !done) {
    //      setTimeout(stopVideo, 2000);
    //      done = true;
    //    }
      }
      function stopVideo() {
        player.stopVideo();
      }
      var i = 0,
        arrLen = list1.length - 1
        str = "";
        str = str + '<table class="table table-striped">'
      +'<thead>'
        + '<tr>'
         + '<th scope="col">#</th>'
        +  '<th scope="col">title</th>'
        +  '<th scope="col">uploader</th>'
        +  '<th scope="col">requested by</th>'
        +  '<th scope="col">length</th>'
        + '</tr>'
      + '</thead>'
      + '<tbody>';
    for (;i <= arrLen; i++){
    str = str + '<tr>'
      + '<th scope="row">' + String(i+1) + '</th>'
      + '<td>' + list1[i].title + '</td>'
      <td>' + list1[i].uploader + '</td>
      <td>' + list1[i].user + '</td>
      <td>' + String(list1[i].length) + '</td>
    + '</tr>';
    };
    str = str + '</tbody>'
    +   '</table>';
    console.log(temp);
    $('#foo').html(str);


</script>

    <body>
    <p>your mom fat and gae</p>
    <p>your dad lesbian?</p>


    <div id = "foo"> </div>
    </body>
    """
    return sitecode

def add_song(list1):
    db = get_db()
    if db.execute(
            'SELECT id FROM songrequest WHERE video_id = ?', (list1[4],)
        ).fetchone() is not None:
        print("song already exists11")
        return "song already exists"

    db.execute('INSERT INTO songrequest (title, uploader, requester, length , video_id) VALUES(? , ? , ? , ? , ?) ' , (list1[0], list1[1], list1[2], list1[3] , list1[4]))
    db.commit()
    print("added song11")
    return "added song"

def generating_fake_list():
    list1 = []
    list1.append(makeentry("THE♂TIME♂WIZARD♂" , "DJ FGT" , "xalhs" , 178 , "aC48Cm1eWLY"))
    list1.append(makeentry("your mom song" , "DJ FGT" , "xalhs" , 177 , "vQHM2Q9OMa0"))
    list1.append(makeentry("Don't Doubt" , "DJ FGT" , "xalhs" , 226 , "CRCvq-l_unE"))

    return list1


def remove_song(N = 1):
    db = get_db()
#    if db.execute(
#            'SELECT id FROM songrequest WHERE video_id = ?', (list1[4],)
#        ).fetchone() is None:
#        print("song doesn't exist11")
#        return "song doesn't exist"
    videoID = db.execute('SELECT * FROM songrequest LIMIT ?' , (N,)).fetchall()[-1]['video_id']
#    print(db.execute('SELECT video_id FROM songrequest LIMIT ?' , (N,)).fetchall()[-1]['video_id'])
#    print(db.execute('SELECT * FROM songrequest LIMIT ?' , (N,)).fetchall()[-1]['video_id'])                    THESE 2 ARE DIFFERENT, WHY?

    db.execute('DELETE FROM songrequest WHERE video_id= ?' , (videoID , )).fetchall()
    db.commit()
    return(videoID)
    #print( videoID[0]['video_id'])

def del_all():
    db = get_db()
    videoID = db.execute('DELETE FROM songrequest').fetchall()

def database_to_list():
    db = get_db()
    pre_list = db.execute('SELECT * FROM songrequest').fetchall()
    list1 = []
    for item in pre_list:
        list1.append(make_entry(item["title"] , item["uploader"] , item["requester"] , item["length"] , item['video_id']))

    return(list1)

def make_entry(title, artist ,user ,length , videoID):
    return {"title" : title , "uploader": artist , "user": user , "length": length , "videoID": videoID}

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         print ("fuck you1")
#         return "I hate you"
#     else:
#         print ("I hate you1")
#         return 'fuck you'
