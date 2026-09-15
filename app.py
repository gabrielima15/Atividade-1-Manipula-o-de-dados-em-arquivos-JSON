from flask import Flask, request
from repository.daoInstituicoes import *


app = Flask(__name__)


def main(arg=[]):
    app.run(debug=True)


@app.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsino = listar()
    print("Entrou na requisição")
    coEntidade = request.args.get("co_entidade")
    print(f'Valor do co_entidade do request: {coEntidade}')
    print(f'Itens da lista de instituições:{len(insituicoesEnsino)}')
    if coEntidade is not None:
        insituicoesEnsinoReponse = [
            insituicaoEnsino.toDict() for insituicaoEnsino in insituicoesEnsino if insituicaoEnsino.co_entidade == coEntidade]
    else:
        insituicoesEnsinoReponse = [
            insituicaoEnsino.toDict() for insituicaoEnsino in insituicoesEnsino]

    return insituicoesEnsinoReponse, 200

@app.get("/instituicoesensino/<int:id_escolhido>")
def getByIdInstituicoesEnsino(id_escolhido):
    print("dentro da função")
    instituicaoSelecionada = buscarPeloId(id_escolhido)
    print("passei pela variavel selecionada")

    if id_escolhido is not None:
        instituicaoResponde = [
            dadoInstituicao.toDict() for dadoInstituicao in instituicaoSelecionada
            if str(dadoInstituicao.id) == str(id_escolhido)
           ]   
        return instituicaoResponde,200
    
    
@app.post("/instituicoesensino")
def postCriarInstituicaoEnsino():
    pegar_dado_requisicao = request.get_json()
    
    enviar_dados = adicionarNovoDado(pegar_dado_requisicao)
    
    return enviar_dados, 201
    
@app.put("/instituicoesensino/<int:id_atualizadar>")
def putAtualizarInstituicaoEnsino(id_atualizadar):
    
    dados_novos = request.get_json()
    sucesso = atualizarDados(id_atualizadar, dados_novos)
    if not sucesso:
        return {"erro": "Instituição não encontrada para atualização"}, 404
        
    return{"mensagem": "Instituição atualizada com sucesso!"}, 200

@app.delete("/instituicoesensino/<int:id_deletar>")
def deleteInstituicoes(id_deletar):
    removerInstituicao = deletarDado(id_deletar)
    
    if not removerInstituicao:
        return {"erro":"instituição não existe."},400
    
    return {"mensagem":"instituição removida"}
    
    

if __name__ == '__main__':
    main()