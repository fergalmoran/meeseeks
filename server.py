import os
from flask import Flask, request, Response
from livereload import Server

from servers.plex import PlexHook

app = Flask(__name__, instance_relative_config=False,
            static_url_path='/', static_folder='views')
app.config.update(
    DEBUG=True,
    PLEX_HOST='',
    PLEX_API_KEY=''
)
app.config.from_pyfile('settings.cfg')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/recommend_movie/', methods=['POST'])
def recommend_movie():
    try:
        content = request.json
        if 'movie_name' in content and content['movie_name'] != '':
            plex = PlexHook(app.config['PLEX_HOST'], app.config['PLEX_API_KEY'])
            results = plex.find_movie(content['movie_name'])
            for r in results:
                location = r.locations[0]
                source_dir = os.path.dirname(location)
                target_dir = \
                    os.path.join(app.config['LINK_DIR'], r.title)
                if not os.path.isfile(target_dir):
                    os.symlink(source_dir, target_dir)

            plex.update_library()

            return Response('Succesfully added item', 200)
        return Response('movie-name key not present', 400)
    except Exception as ex:
        print(ex)
        return Response(ex, 500)


if __name__ == '__main__':
    print('Using {} and {}'.format(app.config['PLEX_HOST'],
                                   app.config['PLEX_API_KEY']))
    server = Server(app.wsgi_app)
    # server.watch
    server.serve(host='0.0.0.0')
