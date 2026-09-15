from flask import Flask, request
from models.instituicaoensino import InstituicaoEnsino,DadosInstituicaoEnsino
from helpers.file.json import read,write


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


def buscarPeloId(id_atualizadar):
    dataset = read("instituicoes.json")
    
    instituicaoEscolhida = [
        InstituicaoEnsino(row["id"],row["co_entidade"],row["no_entidade"],row["qt_mat_bas"])
        for row in dataset if str(row["id"]) == str(id_atualizadar)]
    
    return instituicaoEscolhida


def atualizarDados(id_dado, dados_novos):
    dataset = read("instituicoes.json")
    instituicao_atualizada = False
    
    for row in dataset:
        if str(row["id"]) == str(id_dado):
            row["co_entidade"] = dados_novos.get("co_entidade", row["co_entidade"])
            row["no_entidade"] = dados_novos.get("no_entidade", row["no_entidade"])
            row["qt_mat_bas"]  = dados_novos.get("qt_mat_bas", row["qt_mat_bas"])
            
            instituicao_atualizada = True
            break  
            
    if not instituicao_atualizada:
        return False
    
    salvar_dados = write('instituicoes.json',dataset)
    return True

    
def deletarDado(id):
    dataset = read("instituicoes.json")
    instituicao_selecionada = False
    tamanho_original = len(dataset)
    
    instituicoes_diferentes = [row for row in dataset if str(row["id"]) != str(id)]
    
    if len(instituicoes_diferentes) == tamanho_original:
        instituicao_selecionada = False
        return instituicao_selecionada
    
    write("instituicoes.json",instituicoes_diferentes)
    return True

def adicionarNovoDado(dados_novos):
    dataset = read("instituicoes.json")
    
    if dataset:
        proximo_id = max(int(row["id"])for row in dataset) + 1
    else:
        proximo_id = 1
        
    nova_instituicao = DadosInstituicaoEnsino(
       id=str(proximo_id),
        no_entidade=dados_novos.get("no_entidade", ""),
        co_entidade=dados_novos.get("co_entidade", 0),
        no_uf=dados_novos.get("no_uf", ""),
        sg_uf=dados_novos.get("sg_uf", ""),
        co_uf=dados_novos.get("co_uf", 0),
        no_municipio=dados_novos.get("no_municipio", ""),
        co_municipio=dados_novos.get("co_municipio", 0),
        nu_ano_censo=dados_novos.get("nu_ano_censo", 2026),
        qt_mat_bas=dados_novos.get("qt_mat_bas", 0),
        qt_mat_inf=dados_novos.get("qt_mat_inf", 0),
        qt_mat_fund=dados_novos.get("qt_mat_fund", 0),
        qt_mat_med=dados_novos.get("qt_mat_med", 0),
        qt_mat_prof=dados_novos.get("qt_mat_prof", 0),
        qt_mat_eja=dados_novos.get("qt_mat_eja", 0),
        qt_mat_esp=dados_novos.get("qt_mat_esp", 0)
        )
    
    # 4. Transforma o objeto de volta para dicionário usando o seu método toDict()
    salvar_dado = nova_instituicao.toDict()
    
    # 5. Adiciona à lista existente e sobrescreve o arquivo JSON
    dataset.append(salvar_dado)
    write("instituicoes.json", dataset)
    
    # Retorna o dicionário para a rota responder ao cliente
    return salvar_dado

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