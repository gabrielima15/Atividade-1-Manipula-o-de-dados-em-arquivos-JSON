from helpers.file.json import read,write
from models.instituicaoensino import InstituicaoEnsino,DadosInstituicaoEnsino

def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


def buscarPeloId(id_atualizadar):
    # ler o arquivo.
    dataset = read("instituicoes.json")
    # criar uma lista com os dados selecionados da Instituicao com id igual ao selecionado.
    instituicaoEscolhida = [
        InstituicaoEnsino(row["id"],row["co_entidade"],row["no_entidade"],row["qt_mat_bas"])
        for row in dataset if str(row["id"]) == str(id_atualizadar)]
    
    return instituicaoEscolhida


def atualizarDados(id_dado, dados_novos):
    #ler o arquivo.
    dataset = read("instituicoes.json")
    instituicao_atualizada = False
    # percorre a lista do objeto instituicao com id igual e troca os dados antigos pelo atual.
    for row in dataset:
        if str(row["id"]) == str(id_dado):
            row["co_entidade"] = dados_novos.get("co_entidade", row["co_entidade"])
            row["no_entidade"] = dados_novos.get("no_entidade", row["no_entidade"])
            row["qt_mat_bas"]  = dados_novos.get("qt_mat_bas", row["qt_mat_bas"])
            
            instituicao_atualizada = True
            break  
    # verifica se a instituição existe.
    if not instituicao_atualizada:
        return False
    
    salvar_dados = write('instituicoes.json',dataset)
    return True

    
def deletarDado(id):
    # ler o arquivo.json
    dataset = read("instituicoes.json")
    instituicao_selecionada = False
    # pegar a quantidade de dados existente na instituição.json
    tamanho_original = len(dataset)
    # criar uma nova lista com as instituições com um id direfente ao escolhido.
    instituicoes_diferentes = [row for row in dataset if str(row["id"]) != str(id)]
    # verificar o tamanho da lista atual com o da anterior.
    if len(instituicoes_diferentes) == tamanho_original:
        instituicao_selecionada = False
        return instituicao_selecionada
    # salvar na instituicoes.json
    write("instituicoes.json",instituicoes_diferentes)
    return True

def adicionarNovoDado(dados_novos):
    # ler o arquivo.json
    dataset = read("instituicoes.json")
    # criar um novo id
    if dataset:
        proximo_id = max(int(row["id"])for row in dataset) + 1
    else:
        proximo_id = 1
     
    # definir as novas informações da instituição e caso não digitar nada será definida
    # como padrão String("") e int(0).   
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
    # salvar na variavel no dicionario.
    salvar_dado = nova_instituicao.toDict()
    # escrever na instituicoes.json
    dataset.append(salvar_dado)
    write("instituicoes.json", dataset)
    
    return salvar_dado
