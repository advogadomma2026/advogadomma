# Publicar o site no GitHub Pages (grátis)

Hospedagem atual: **GitHub Pages** (conta `migueldeandradeadv@gmail.com`).
Substitui a Vercel, que passou a exigir pagamento. O GitHub Pages é gratuito
para contas pessoais, não pede cartão de crédito e já inclui HTTPS.

O site é 100% HTML, CSS e Java puro (sem framework, sem build, sem banco de
dados), que é exatamente o que o GitHub Pages serve. Nada precisou ser
reescrito.

---

> ## Estado em 05/10/2026
>
> - [x] Conta criada: **`advogadomma2026`** (`migueldeandradeadv@gmail.com`)
> - [x] Repositório: <https://github.com/advogadomma2026/advogadomma> (público)
> - [x] Código enviado (`main`), GitHub Pages publicado
> - [x] `xtitoxv` (CriaSiteVH) adicionado como **colaborador**
> - [x] Domínio customizado `www.advogadomma.com.br` cadastrado no Pages
> - [ ] **Pendente:** trocar os registros DNS no registro.br (seção 4)
> - [ ] **Pendente:** remover os domínios do projeto na Vercel (seção 6)

## 1. Criar a conta e o repositório (uma vez) — concluído

1. Criar a conta em <https://github.com/join> com o e-mail
   `migueldeandradeadv@gmail.com` (o GitHub manda um código de confirmação
   para o e-mail — precisa abrir a caixa "GitHub" e confirmar).
2. Criar o repositório: <https://github.com/new>
   - **Owner:** a conta do cliente
   - **Nome do repositório:** `advogadomma` (sem espaços, sem acento)
   - **Visibilidade:** **Public**. No plano gratuito (GitHub Free) o GitHub
     Pages só publica a partir de repositório **público** — em repositório
     privado ele pede assinatura. Isso não é problema aqui: o conteúdo do site
     é público por definição, e o único arquivo do repositório que o cliente
     precisa proteger (credenciais) nunca entra nele.
   - **Não** marque "Add a README" — o repositório precisa ficar vazio.

## 2. Subir o código — concluído

Na pasta `siteadvmma`, com o Git instalado:

```bash
git init -b main
git add .
git commit -m "Site Advocacia MMA"
git remote add origin https://github.com/advogadomma2026/advogadomma.git
git push -u origin main
```

> O arquivo `CNAME` já está na raiz com `www.advogadomma.com.br`, e o
> `.nojekyll` também. **Não apague nenhum dos dois.**

## 3. Ligar o GitHub Pages ao repositório — concluído

1. No repositório: **Settings → Pages**.
2. Em **Build and deployment → Source**, escolher **Deploy from a branch**.
3. Branch: `main`, pasta: `/ (root)`. Salvar.
4. O endereço de teste é `https://advogadomma2026.github.io/advogadomma/`
   (redireciona para o domínio customizado assim que o DNS for trocado).

## 4. Apontar o domínio (registro.br) — PENDENTE

O domínio é do cliente e **nada precisa ser transferido**: só muda para onde
ele aponta. Hoje os registros ainda apontam para a Vercel
(`www` → `0bc0940bfd554ae4.vercel-dns-017.com`, apex → `216.198.79.1` /
`64.29.17.1`). No painel do registro.br → *Meus Domínios* →
`advogadomma.com.br` → *DNS* → *Editar Zona*:

| Tipo   | Nome (host)        | Valor                            |
|--------|--------------------|----------------------------------|
| ALIAS  | vazio / raiz (`@`) | `advogadomma2026.github.io`      |
| CNAME  | `www`              | `advogadomma2026.github.io`      |

Observações:

- O painel do registro.br chama "ALIAS" de **ALIAS** ou **ANAME** (depende da
  versão da tela). É o registro que faz o apontamento do domínio sem `www`
  direto para o GitHub Pages.
- Se o registro.br **não** oferecer ALIAS/ANAME, use os IPs do GitHub Pages
  em 5 registros `A` na raiz:
  `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- O `CNAME` de `www` aponta **sem o nome do repositório**
  (`advogadomma2026.github.io`, e não `advogadomma2026.github.io/advogadomma`).
- Depois de salvar, pode levar de 5 minutos a algumas horas para propagar. O
  GitHub emite o certificado HTTPS automaticamente em até 1 hora. Enquanto o
  certificado não sai, o site responde em `http` — não é erro.
- Enquanto o DNS não propagar, o GitHub mostra um aviso de "Domain is not
  verified". Ignore e volte em algumas horas.

## 5. Servir também o endereço sem `www`

Como o `CNAME` já declara `www.advogadomma.com.br`, o GitHub redireciona o
domínio sem `www` para o com `www`. Se o cliente preferir que
`advogadomma.com.br` (sem www) responda diretamente, adicione no repositório um
arquivo `CNAME` com **duas linhas**:

```
www.advogadomma.com.br
advogadomma.com.br
```

## 5. Ajustar a permissão do colaborador

Em repositório **público** o GitHub **não permite** conceder `Admin` nem
`Maintain` — a API responde `Cannot assign ... permission of admin`. O máximo
disponível é **Write**. Consequências:

- `xtitoxv` consegue enviar commits, criar branches e tags (publicar o site). ✔
- Mudar **Settings → Pages**, domínio customizado,Secrets e excluir o
  repositório continua sendo só do dono (`advogadomma2026`). ✘

Se for preciso dar controle total no futuro, o caminho é deixar o repositório
privado (exige plano pago) ou usar uma organização com o plano correto.

## 6. Desligar a Vercel (depois que o site novo estiver no ar)

1. No painel da Vercel do cliente: **Settings → Domains**, remover
   `advogadomma.com.br` e `www.advogadomma.com.br` do projeto.
2. Cancelar/pausar a assinatura do time, se houver.
3. Conferir no <https://www.whois.com.br/> que o domínio continua registrado no
   nome do cliente — a Vercel nunca foi o registrador, apenas o hospedeiro.

Não remova o domínio da Vercel **antes** de o site novo responder: enquanto os
dois existirem, a Vercel avisa que o domínio está em uso em outro serviço.

---

## 7. Publicar alterações depois

```bash
python build.py      # só se editou build.py
git add .
git commit -m "descrição da alteração"
git push
```

O GitHub Pages publica em 1–2 minutos. Não há build no servidor: o que está no
repositório é o que vai ao ar.

Para editar texto simples, dá para alterar o HTML direto no GitHub
(typings: botão pencil em cima do arquivo → *Commit changes*) — mas a forma
correta é editar os dados no bloco `SITE` / listas do `build.py` e rodar
`python build.py`, senão a próxima geração sobrescreve a edição.

---

## 8. Limites do plano gratuito (para saber)

| Recurso | Limite |
|---|---|
| Banda por mês | 100 GB |
| Tamanho do repositório | 1 GB (o site usa ~2,7 MB) |
| Build no servidor | Jekyll (padrão) — desativado pelo `.nojekyll` |
| Domínio próprio | ilimitado, HTTPS automático |
| Prazo de propagação | 1–2 min |

O site não passa perto de nenhum desses limites.

---

## Alternativa: Cloudflare Pages

Se um dia o GitHub enrolar ou faltar alguma configuração (cache de assets,
redirecionamentos, `404` sob controle), a **Cloudflare Pages** também é
grátis e sem cartão: em *Workers & Pages → Create → Pages → Connect to Git*,
apontar para o mesmo repositório, build em branco (*None*), output `/`. Como
a Cloudflare também hospeda o DNS, dá para trocar os registros sem sair de lá.
