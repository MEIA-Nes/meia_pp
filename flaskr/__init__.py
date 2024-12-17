from flask import Flask, render_template
from analises import municipios_alagoas

def create_app():
    # Inicializa a aplicação Flask
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/home')
    def home():
        # Carregar e manipular os dados diretamente
        return render_template('introduction.html')

    @app.route('/pesquisa_analises_municipios')
    def pesquisa_analise_municipio():
        return render_template('pesquisa_analises_municipios.html', municipios=municipios_alagoas)

    @app.route('/sobrenos')
    def abtus():
        return render_template('sobrenos.html')

    @app.route('/pesquisa_analises_municipios/<municipio>')
    def show_municipio(municipio):
        return render_template('municipio_analise_templete.html', municipio=municipio) 
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)