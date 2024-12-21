import io  # Certifique-se de importar o módulo 'io'
import base64  # Importando base64 para codificar as imagens
from flask import Flask, render_template, Response
from analises import municipios_alagoas, gerar_linha, gerar_pizza, meis_municipio, idh_municipio
import pandas as pd

def create_app():
    # Inicializa a aplicação Flask
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/home')
    def home():
        return render_template('introduction.html')

    @app.route('/pesquisa_analises_municipios')
    def pesquisa_analise_municipio():
        return render_template('pesquisa_analises_municipios.html', municipios=municipios_alagoas)

    @app.route('/sobrenos')
    def abtus():
        return render_template('sobrenos.html')

    @app.route('/pesquisa_analises_municipios/<municipio>')
    def show_municipio(municipio):
        meismunicipio = meis_municipio[meis_municipio['no_mun'] == municipio]['valor'].to_list()
        anosmei = meis_municipio[meis_municipio['no_mun'] == municipio]['ano'].tolist()
        idhsmunicipio = idh_municipio[(idh_municipio['no_mun'] == municipio) & (idh_municipio['idh_categoria'] == 'Total')]['valor'].to_list()
        anosidh = idh_municipio[(idh_municipio['no_mun'] == municipio) & (idh_municipio['idh_categoria'] == 'Total')]['ano'].tolist()

        # Gerando os gráficos como imagens em base64
        grafico_linha_meis = gerar_linha(anosmei, [meismunicipio], titulo=f"MEIs por ano em {municipio}", cores=['darkred', '#9467bd'], xlabel='Ano', ylabel='MEIs')
        grafico_linha_idhs = gerar_linha(anosidh, [idhsmunicipio], titulo=f"IDHs por década em {municipio}", cores=['lightgreen', '#9467bd'], xlabel='Ano', ylabel='IDH')
        
        # Retorna o template com os gráficos codificados em base64
        return render_template('municipio_analise_templete.html', municipio=municipio, linha_meis=grafico_linha_meis, linha_idhs=grafico_linha_idhs)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
