from app import app
from db_setup import init_db, db_session
from forms import MusicSearchForm, AlbumForm
from flask import flash, render_template, request, redirect
from models import Album, Artist
from tables import Results
 
init_db()

def save_changes(album, form, new=False):
    """
    Salva as mudanças no banco de dados
    """
    # Obtém dados do formulário e os aloca para os atributos corretos
    # do objeto tabela SQLAlchemy
    artist = Artist()
    artist.name = form.artist.data
 
    album.artist = artist
    album.title = form.title.data
    album.release_date = form.release_date.data
    album.publisher = form.publisher.data
    album.media_type = form.media_type.data
 
    if new:
        # Adiciona o novo álbum ao banco de dados
        db_session.add(album)
 
    # Faz commit dos dados ao banco de dados
    db_session.commit()
  
@app.route('/', methods=['GET', 'POST'])
def index():
    qry = db_session.query(Album).all()
    for q in qry:
        print(q.title, q.artist)
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search, qry=qry)
 
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search_string:
        if search.data['select'] == 'Artist':
            qry = db_session.query(Album, Artist).filter(
                Artist.id==Album.artist_id).filter(
                    Artist.name.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'Album':
            qry = db_session.query(Album).filter(
                Album.title.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Publisher':
            qry = db_session.query(Album).filter(
                Album.publisher.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(Album)
            results = qry.all()
    else:
        qry = db_session.query(Album)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # Apresenta os resultados
        table = Results(results)
        table.border = True
        for result in results:
            print(result.title, result.artist)
        return render_template('results.html', table=table)
 
@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    """
    Adiciona um novo álbum
    """
    form = AlbumForm(request.form)
 
    if request.method == 'POST' and form.validate():
        # Salva o álbum
        album = Album()
        save_changes(album, form, new=True)
        flash('Album created successfully!')
        return redirect('/')
 
    return render_template('new_album.html', form=form)

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Album).filter(Album.id==id)
    album = qry.first()
 
    if album:
        form = AlbumForm(formdata=request.form, obj=album)
        if request.method == 'POST' and form.validate():
            # Salva as edições
            save_changes(album, form)
            flash('Album updated successfully!')
            return redirect('/')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """
    Deleta o item no banco de dados que corresponde ao id especificado na URL
    """
    qry = db_session.query(Album).filter(Album.id==id)
    album = qry.first()
 
    if album:
        form = AlbumForm(formdata=request.form, obj=album)
        if request.method == 'POST' and form.validate():
            # Deleta o item do banco de dados
            db_session.delete(album)
            db_session.commit()
 
            flash('Album deleted successfully!')
            return redirect('/')
        return render_template('delete_album.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
 
if __name__ == '__main__':
    app.run(debug=True)