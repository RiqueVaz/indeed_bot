# 🤖 Bot de Candidatura Automática - Indeed Brasil

Bot automatizado para se candidatar a vagas no Indeed Brasil usando Camoufox.

## 📋 Funcionalidades

- ✅ Busca automática de vagas no Indeed Brasil
- ✅ Candidaturas automáticas com preenchimento de formulários
- ✅ Suporte completo ao português brasileiro
- ✅ Modo stealth para evitar detecção
- ✅ Sistema de logs detalhado
- ✅ Configuração flexível via YAML

## 🚀 Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar o arquivo `config.yaml`:**
   - Edite a URL de busca com seus critérios
   - Configure o diretório de dados do usuário
   - Ajuste os parâmetros de busca

## ⚙️ Configuração

### config.yaml

```yaml
search:
  base_url: "https://br.indeed.com/jobs?q=SEU_CARGO&l=SUA_CIDADE&radius=25"
  start: 0
  end: 100

camoufox:
  user_data_dir: "user_data_dir"
  language: "br"
```

### Parâmetros de Busca

- **q**: Palavra-chave da vaga (ex: "Desenvolvedor Python")
- **l**: Localização (ex: "São Paulo, SP" ou "Remoto")
- **radius**: Raio de busca em km
- **start/end**: Intervalo de páginas para buscar

## 🎯 Como Usar

1. **Primeira execução:**
```bash
python indeed_bot.py
```

2. **Login manual:**
   - O bot abrirá a página de login do Indeed
   - Faça login manualmente
   - Feche o navegador e execute novamente

3. **Execução automática:**
   - O bot buscará vagas automaticamente
   - Se candidatará a todas as vagas "Indeed Apply"
   - Salvará logs de todas as ações

## 📊 Logs

Os logs são salvos em `indeed_apply.log` com:
- Timestamp de cada ação
- URLs das vagas processadas
- Status das candidaturas (sucesso/falha)
- Mensagens de erro detalhadas

## ⚠️ Considerações Importantes

- **Respeite os termos de uso** do Indeed
- **Use com moderação** para evitar bloqueios
- **Configure limites** de candidaturas por dia
- **Revise as vagas** antes de aplicar automaticamente
- **Mantenha seu perfil atualizado**

## 🔧 Solução de Problemas

### Erro de Login
- Verifique se fez login manualmente na primeira execução
- Limpe o diretório `user_data_dir` e tente novamente

### Cloudflare Protection
- Se aparecer proteção Cloudflare, clique manualmente
- O bot aguardará você resolver

### Vagas não encontradas
- Verifique se a URL de busca está correta
- Teste a busca manualmente no Indeed

## 📝 Exemplo de Uso

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar config.yaml com seus critérios
# 3. Executar o bot
python indeed_bot.py

# 4. Fazer login manual na primeira execução
# 5. Executar novamente para automação
python indeed_bot.py
```

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `indeed_apply.log`
2. Confirme se a configuração está correta
3. Teste a busca manualmente no Indeed

---

**⚠️ Aviso Legal**: Este software é fornecido "como está" sem garantias. O uso é de sua responsabilidade. Respeite os termos de uso do Indeed e use com moderação.