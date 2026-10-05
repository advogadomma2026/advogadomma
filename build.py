# -*- coding: utf-8 -*-
"""
Gerador de páginas estáticas — Advocacia e Consultoria Jurídica MMA
Uso:  python build.py
Saída: index.html, areas.html, sobre.html, contato.html, privacidade.html,
       404.html, CNAME, .nojekyll, sitemap.xml, robots.txt, site.webmanifest
"""
import json
import os
import html
import datetime
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
DST = ROOT

# ---------------------------------------------------------------------------
# DADOS DO ESCRITÓRIO
# ---------------------------------------------------------------------------
SITE = {
    "nome": "Advocacia e Consultoria Jurídica MMA",
    "dominio": "www.advogadomma.com.br",
    "advogado": "Miguel Martinho Coelho de Andrade",
    "oab": "OAB/BA 92318",
    "oab_num": "92318",
    "telefone": "(71) 99726-0142",
    "telefone_link": "+5571997260142",
    "whatsapp": "https://wa.me/5571997260142",
    "email": "migueldeandradeadv@gmail.com",
    "endereco": "Rua Ladeira da Saúde, nº 262 — Saúde",
    "cidade": "Salvador/BA — CEP 40040-640",
    "maps": "https://www.google.com/maps/search/?api=1&query=Rua+Ladeira+da+Sa%C3%BAde%2C+262%2C+Salvador%2C+BA",
    "horario": [("Segunda a Sexta", "08h30 às 18h"), ("Sábado", "08h30 às 12h")],
    "sigilo": "Sigilo profissional garantido pelo Estatuto da Advocacia (art. 7º, II, do Estatuto da OAB).",
    "credito": {
        "rotulo": "Desenvolvido por",
        "nome": "CriaSiteVH",
        "url": "https://www.criasitevh.com.br",
        "logo": "assets/img/criasitevh.jpg",
        "logo_w": 27,
        "logo_h": 20,
    },
}

# ---------------------------------------------------------------------------
# ÁREAS DO DIREITO — ordem alfabética
# ---------------------------------------------------------------------------
AREAS = [
    {
        "slug": "administrativo",
        "icone": "building",
        "titulo": "Direito Administrativo",
        "desc": "Atuação diante da Administração Pública direta e indireta, analisando a legalidade de atos administrativos, licitações e contratos públicos.",
        "destaques": [
            "Licitações e contratos públicos (Lei 14.133/2021)",
            "Servidores públicos: punições, estabilidade e aposentadoria",
            "Multas, autarquias e empresas públicas",
            "Ações contra o Estado e entidades",
            "Improbidade administrativa",
        ],
    },
    {
        "slug": "ambiental",
        "icone": "leaf",
        "titulo": "Direito Ambiental",
        "desc": "Defesa em processos administrativos ambientais e ações civis públicas, com foco em regularização de atividades e responsabilização por dano ambiental.",
        "destaques": [
            "Autuação e multa ambiental (IBAMA, INEMA, Coema)",
            "Licenciamento ambiental e estudo de impacto",
            "Áreas de proteção, APPs e unidades de conservação",
            "Ações civis públicas ambientais",
            "Reparação de danos ambientais",
        ],
    },
    {
        "slug": "civil",
        "icone": "doc",
        "titulo": "Direito Civil",
        "desc": "Atuação em relações entre particulares e também contra empresas e órgãos públicos: revisão de contratos, cobrança, indenizações e responsabilidade civil.",
        "destaques": [
            "Contratos: revisão, cobrança e rescisão",
            "Indenizações por dano moral e material",
            "Responsabilidade civil e caso fortuito ou força maior",
            "Direito Imobiliário e usucapião",
            "Família: pensão alimentícia, guarda e partilha",
        ],
    },
    {
        "slug": "constitucional",
        "icone": "landmark",
        "titulo": "Direito Constitucional",
        "desc": "Defesa dos direitos e garantias fundamentais e análise da constitucionalidade de leis e atos normativos, com atuação nos remédios constitucionais e nos tribunais superiores.",
        "destaques": [
            "Direitos e garantias fundamentais (art. 5º da CF)",
            "Controle de constitucionalidade de leis e atos normativos",
            "Remédios constitucionais: mandado de segurança, habeas data e habeas corpus",
            "Ações diretas de inconstitucionalidade (ADI, ADPF e ADC)",
            "Recursos extraordinários e atuação no STF",
        ],
    },
    {
        "slug": "consumidor",
        "icone": "bag",
        "titulo": "Direito do Consumidor",
        "desc": "Aplicação integral do Código de Defesa do Consumidor (Lei 8.078/1990) em reclamações administrativas e ações judiciais.",
        "destaques": [
            "Produtos e serviços defeituosos",
            "Publicidade enganosa e práticas abusivas",
            "Correção monetária, juros e atualização de valores",
            "Reclamações no Procon e no consumidor.gov.br",
            "Responsabilidade por vício e por fato do produto",
        ],
    },
    {
        "slug": "eca",
        "icone": "heart",
        "titulo": "Direito da Criança e do Adolescente (ECA)",
        "desc": "Atuação na defesa dos direitos de crianças e adolescentes, com prioridade absoluta, conforme o Estatuto da Criança e do Adolescente.",
        "destaques": [
            "Adoção e famílias de acolhimento",
            "Conselho Tutelar e medidas de proteção",
            "Acolhimento institucional e familiar",
            "Direito à educação, saúde, lazer e convivência",
            "Sigilo do adolescente infrator (art. 109 do ECA)",
        ],
    },
    {
        "slug": "direitos-humanos",
        "icone": "shield",
        "titulo": "Direitos Humanos",
        "desc": "Defesa de direitos e garantias, com atuação nos sistemas de responsabilização do Estado e de seus agentes.",
        "destaques": [
            "Proteção e reforço dos direitos e garantias",
            "Responsabilidade internacional do Estado",
            "Recursos em âmbito internacional e regional",
            "Execução de decisões estrangeiras",
            "Casos de discriminação e intolerância",
        ],
    },
    {
        "slug": "eleitoral",
        "icone": "ballot",
        "titulo": "Direito Eleitoral",
        "desc": "Atuação na Justiça Eleitoral em todas as fases do processo eleitoral, incluindo contagens, impugnações e investigação criminal eleitoral.",
        "destaques": [
            "Condições de inelegibilidade",
            "Contabilidade de campanha e prestação de contas",
            "Impugnação de votos e da urna eletrônica",
            "Investigação criminal eleitoral",
            "Recursos especiais no TSE",
        ],
    },
    {
        "slug": "empresarial",
        "icone": "briefcase",
        "titulo": "Direito Empresarial",
        "desc": "Consultoria jurídica preventiva e contenciosa para empresas, com foco em segurança contratual e governança.",
        "destaques": [
            "Constituição, alteração e extinção de sociedades",
            "Contratos societários e de parceria",
            "Compliance e programas de integridade",
            "Fusões, aquisições e due diligence",
            "Responsabilidade de sócios e administradores",
        ],
    },
    {
        "slug": "financeiro",
        "icone": "banknote",
        "titulo": "Direito Financeiro",
        "desc": "Análise e defesa em matérias ligadas ao orçamento público, dívida pública, crédito, mercados de capitais e setor financeiro regulado.",
        "destaques": [
            "Controle da dívida pública e do orçamento",
            "Sistema financeiro e regulação do Banco Central",
            "Recuperação e reestruturação de créditos",
            "Responsabilidade de instituições financeiras",
            "Produtos e serviços de crédito",
        ],
    },
    {
        "slug": "internacional",
        "icone": "globe",
        "titulo": "Direito Internacional",
        "desc": "Atuação em questões de caráter transnacional, com apoio na análise de tratados, costumes internacionais e jurisdição estrangeira.",
        "destaques": [
            "Comércio exterior e contratos internacionais",
            "Investimentos estrangeiros e tratados bilaterais",
            "Cobrança e recuperação de créditos no exterior",
            "Extraterritorialidade da lei brasileira",
            "Mediação e arbitragem internacional",
        ],
    },
    {
        "slug": "penal",
        "icone": "gavel",
        "titulo": "Direito Penal",
        "desc": "Defesa técnica completa em inquérito e processo criminal, com acompanhamento em todas as instâncias da Justiça Criminal.",
        "destaques": [
            "Audiência de custódia e liberdade provisória",
            "Habeas corpus nas instâncias",
            "Crimes econômicos e crimes empresariais",
            "Tribunal do Júri",
            "Acordo de não persecução penal (ANPP)",
        ],
    },
    {
        "slug": "previdenciario",
        "icone": "umbrella",
        "titulo": "Direito Previdenciário",
        "desc": "Revisão e defesa de benefícios de segurados e pensionados do Regime Geral de Previdência Social e dos Regimes Próprios.",
        "destaques": [
            "Aposentadoria por idade, tempo de contribuição e incapacidade",
            "Pensão por morte, invalidez e revisão",
            "Revisão de benefícios concedidos",
            "Cálculo de benefícios e revisões de cálculo",
            "Contribuições e recolhimentos",
        ],
    },
    {
        "slug": "trabalho",
        "icone": "helmet",
        "titulo": "Direito do Trabalho",
        "desc": "Atuação na Justiça do Trabalho e em negociações administrativas, em favor de trabalhadores e de empresas.",
        "destaques": [
            "Verbas rescisórias e rescisão contratual",
            "Assédio moral e assédio sexual",
            "Acidentes de trabalho e doenças ocupacionais",
            "FGTS, férias, 13º e horas extras",
            "Negociações coletivas e dissídios",
        ],
    },
    {
        "slug": "tributario",
        "icone": "receipt",
        "titulo": "Direito Tributário",
        "desc": "Consultoria e contencioso tributário, com análise de legalidade de tributos, lançamentos, obrigação de pagar e prescrição.",
        "destaques": [
            "Lançamento, auto de infração e cobrança",
            "Obrigações principais e acessórias",
            "IPTU, IPVA, ITBI e taxas municipais",
            "IRPF, IRPJ e planejamento sucessório tributário",
            "Planejamento tributário lícito e defesa em cobrança",
        ],
    },
]

# ---------------------------------------------------------------------------
# DERIVADOS DE AREAS — nunca escreva o número de áreas à mão
# ---------------------------------------------------------------------------
N_AREAS = len(AREAS)

# Nomes curtos usados nas meta descriptions.
NOMES_META = {
    "eca": "ECA",
    "direitos-humanos": "direitos humanos",
    "previdenciario": "previdenciário",
}


def areas_nomes_meta():
    nomes = [NOMES_META.get(a["slug"], a["slug"].replace("-", " ")) for a in AREAS]
    return ", ".join(nomes[:-1]) + " e " + nomes[-1]


SITE["descricao_meta"] = (
    f"Advocacia e Consultoria Jurídica MMA — atuação em {N_AREAS} áreas do Direito em Salvador/BA "
    "e atendimento remoto. Consulta inicial gratuita, sigilosa e feita diretamente pelo advogado."
)

SERVICOS = [
    {
        "icone": "chat",
        "titulo": "Consulta inicial",
        "desc": "Primeira conversa para entender o seu caso, tirar dúvidas e definir os próximos passos. Sem custo e sem compromisso de contratação.",
        "meta": ["30 a 60 minutos", "Primeira orientação"],
    },
    {
        "icone": "doc",
        "titulo": "Parecer jurídico",
        "desc": "Análise técnica da situação, com conclusão fundamentada, riscos, custos estimados e todas as alternativas de atuação.",
        "meta": ["Prazo combinado", "Documento enviado por e-mail"],
    },
    {
        "icone": "shield",
        "titulo": "Acompanhamento processual",
        "desc": "Representação completa em processos administrativos e judiciais, com relatórios periódicos sobre o andamento.",
        "meta": ["Todas as instâncias", "Relatórios regulares"],
    },
    {
        "icone": "building",
        "titulo": "Assessoria preventiva",
        "desc": "Consultoria contínua para pessoas e empresas: revisão de contratos, adequação legal e prevenção de litígios.",
        "meta": ["Recorrencial ou pontual", "Plano sob medida"],
    },
]

PASSOS = [
    ("01", "Fale conosco", "Envie sua dúvida pelo WhatsApp com o máximo de detalhes possível."),
    ("02", "Análise inicial", "Avaliamos o caso e identificamos os pontos jurídicos relevantes."),
    ("03", "Proposta", "Você recebe a estratégia, os prazos e os valores antes de decidir."),
    ("04", "Atuação", "Se autorizar, iniciamos o acompanhamento e reportamos cada evolução."),
]

DIFERENCIAIS = [
    ("Atendimento direto do advogado", "Você fala com quem vai defender o seu caso, sem cadeia de atendimento."),
    ("Sigilo absoluto", "Todas as informações são tratadas em sigilo, conforme o Estatuto da OAB."),
    ("Clareza antes da contratação", "Escopo, valores e prazos alinhados antes de qualquer assinatura."),
    ("Comunicação constante", "Relatórios objetivos sobre cada movimentação do processo."),
    ("Preço transparente", "Condições apresentadas por escrito, sem custos ocultos."),
    ("Atuação híbrida", "Presencial em Salvador/BA e atendimento remoto a todo o Brasil."),
]

FAQ = [
    (
        "A primeira consulta tem custo?",
        "A conversa inicial é gratuita e serve para entender o caso e avaliar a viabilidade da atuação. "
        "O atendimento é sigiloso e não gera qualquer compromisso de contratação.",
    ),
    (
        "Quais documentos devo levar?",
        "Reúna o que tiver relação com o caso: contratos, notas fiscais, e-mails, prints de conversas, "
        "documentos pessoais, decisões e intimações. Quanto mais completo o material, mais precisa é a orientação.",
    ),
    (
        "Em quanto tempo recebo resposta?",
        "Mensagens recebidas em horário comercial costumam ser respondidas no mesmo dia útil. "
        "Prazos processuais específicos são informados logo na análise inicial.",
    ),
    (
        "Como funciona o sigilo do escritório?",
        "O sigilo é uma obrigação legal, prevista no art. 7º, II, do Estatuto da OAB. "
        "Nenhuma informação do cliente é compartilhada com terceiros sem autorização expressa.",
    ),
    (
        "Como são definidos os honorários?",
        "Dependendo do caso, o advogado pode trabalhar com honorários únicos, por hora ou por resultado. "
        "A proposta é sempre apresentada por escrito, com escopo e valores claros, antes do início da atuação.",
    ),
    (
        "Vocês atendem pessoas de outras cidades?",
        "Sim. Além do atendimento presencial em Salvador/BA, o escritório realiza atendimento por "
        "videoconferência e troca de documentos por e-mail, mantendo todos os trâmites válidos e formais.",
    ),
    (
        "O que o WhatsApp resolve e o que precisa de outro canal?",
        "O WhatsApp é o canal mais rápido para primeiro contato e orientação inicial. "
        "Documentos e petições são enviados por e-mail ou em atendimento reservado, para garantir a integridade dos arquivos.",
    ),
    (
        "Posso enviar documentos por aqui?",
        "Pode, mas evite anexar arquivos com dados sensíveis de terceiros. Quando se sentir seguro, "
        "escreva: “Autorizo o envio dos documentos anexados”. Os arquivos são tratados com reserva.",
    ),
]

# ---------------------------------------------------------------------------
# ÍCONES (SVG inline, traçado)
# ---------------------------------------------------------------------------
ICONS = {
    "building": '<path d="M3 21h18"/><path d="M5 21V8a2 2 0 0 1 2-2h2M5 21h14"/><path d="M9 21v-4h6v4"/><path d="M9 6V4h6a2 2 0 0 1 2 2v4h2a2 2 0 0 1 2 2v9"/><path d="M10 10h.01M14 10h.01M10 14h.01M14 14h.01"/>',
    "leaf": '<path d="M20 4c0 8-5 15-13 15H4a1 1 0 0 1-1-1C3 10 9 4 20 4Z"/><path d="M4 20 15 9"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
    "landmark": '<path d="M3 21h18"/><path d="M5 21V10M10 21V10M14 21V10M19 21V10"/><path d="M2.5 10 12 3.5 21.5 10Z"/>',
    "bag": '<path d="M6 8h12l1 12.5a1 1 0 0 1-1 1.1H6a1 1 0 0 1-1-1.1Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "heart": '<path d="M12 20.5 4.6 13.2A4.9 4.9 0 0 1 11.5 6.3l.5.5.5-.5a4.9 4.9 0 0 1 6.9 6.9Z"/>',
    "shield": '<path d="M12 3l7.5 3v5.4c0 5-3.4 8.6-7.5 10.6-4.1-2-7.5-5.6-7.5-10.6V6Z"/><path d="m9.2 12.2 2 2 3.6-3.9"/>',
    "ballot": '<rect x="4" y="9" width="16" height="11.5" rx="1.6"/><path d="M8 9V7a4 4 0 0 1 8 0v2"/><path d="M9.6 14.6l1.6 1.6 3.2-3.4"/>',
    "briefcase": '<rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5"/><path d="M3 12.5h18"/>',
    "banknote": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6.5 12h.01M17.5 12h.01"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3.2 9.5h17.6M3.2 14.5h17.6"/><path d="M12 3c2.6 2.6 3.9 5.7 3.9 9S14.6 18.4 12 21c-2.6-2.6-3.9-5.7-3.9-9S9.4 5.6 12 3Z"/>',
    "gavel": '<path d="M4 21h8"/><path d="m11 14-3.5-3.5L14 4l3.5 3.5Z"/><path d="m13 5 6 6"/><path d="M16.5 8.5 20 12"/><path d="m18 10 4 4-2.5 2.5-4-4Z"/>',
    "umbrella": '<path d="M12 4a8 8 0 0 1 8 8H4a8 8 0 0 1 8-8Z"/><path d="M12 12v6.2a2.2 2.2 0 0 0 4.4 0"/>',
    "helmet": '<path d="M4 16.5a8 8 0 0 1 16 0"/><path d="M9.2 9V16.5M14.8 9v7.5"/><path d="M2.5 16.5h19a1 1 0 0 1 1 1V19h-21v-1.5a1 1 0 0 1 1-1Z"/>',
    "receipt": '<path d="M6 3h12v18l-2.4-1.6-2.4 1.6-2.4-1.6-2.4 1.6L6 21Z"/><path d="M14.5 8 9.5 16"/><circle cx="10" cy="9.6" r="1"/><circle cx="14" cy="14.4" r="1"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.9A8 8 0 1 1 21 12Z"/><path d="M9 11h6M9 14h4"/>',
    "phone": '<path d="M6.5 3h3l1.5 4.5-2 1.4a12 12 0 0 0 6.1 6.1l1.4-2 4.5 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.2 2 2 0 0 1 6.5 3Z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.2 2"/>',
    "arrow": '<path d="M5 12h13"/><path d="m12.5 5.5 6.5 6.5-6.5 6.5"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "spark": '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
    "wa": '<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/><path d="M9.1 8.4c.2-.4.4-.4.6-.4h.5c.2 0 .4 0 .6.4l.7 1.7c.1.3 0 .5-.1.7l-.4.5c-.1.2-.3.4-.1.7a6 6 0 0 0 2.6 2.3c.3.2.5.1.7-.1l.5-.6c.2-.2.4-.3.7-.2l1.6.8c.3.1.4.3.4.5v.5c0 .4-.3.8-.7.9-1 .4-2.2.2-3.4-.4a9.4 9.4 0 0 1-4-4.3c-.5-1.3-.5-2.6 0-3.5Z" fill="currentColor" stroke="none"/>',
    "shield2": '<path d="M12 3l7.5 3v5.4c0 5-3.4 8.6-7.5 10.6-4.1-2-7.5-5.6-7.5-10.6V6Z"/><path d="M12 8v4.2"/><path d="M12 15.8h.01"/>',
}


def icon(name, cls="ico", size=22):
    body = ICONS.get(name, ICONS["doc"])
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{body}</svg>'
    )


E = html.escape


def wa_link(msg):
    return SITE["whatsapp"] + "?text=" + urllib.parse.quote(msg)


def wa_area(a):
    return wa_link(f"Olá! Vim pelo site da {SITE['nome']} e gostaria de falar sobre a área de {a['titulo']}.")


def wa_geral(assunto="orientação inicial"):
    return wa_link(f"Olá! Vim pelo site da {SITE['nome']} e gostaria de uma {assunto}.")


YEAR = datetime.date.today().year


def asset(path, base=""):
    """Cache-busting: a Vercel serve /assets com immutable por 1 ano, entao o
    caminho precisa mudar quando o arquivo muda senao o visitante ve a versao antiga.
    base="/" fixa a raiz do site (usado na 404 do GitHub Pages)."""
    ts = int(os.path.getmtime(os.path.join(ROOT, path)))
    return f"{base}{path}?v={ts}"


HOURS_LI = "".join(
    f'<li><span>{E(d)}</span><strong>{E(h)}</strong></li>' for d, h in SITE["horario"]
)

# ---------------------------------------------------------------------------
# STRUCTURED DATA
# ---------------------------------------------------------------------------
ORG_JSON = {
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": SITE["nome"],
    "url": f"https://{SITE['dominio']}/",
    "logo": f"https://{SITE['dominio']}/assets/img/logo-mma-3x.png",
    "image": f"https://{SITE['dominio']}/assets/img/logo-mma-3x.png",
    "description": SITE["descricao_meta"],
    "founder": {"@type": "Person", "name": SITE["advogado"], "jobTitle": "Advogado"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": SITE["endereco"],
        "addressLocality": "Salvador",
        "addressRegion": "BA",
        "postalCode": "40040-640",
        "addressCountry": "BR",
    },
    "telephone": SITE["telefone"],
    "email": SITE["email"],
    "areaServed": "BR",
    "priceRange": "Sob consulta",
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:30",
            "closes": "18:00",
        },
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": "Saturday",
            "opens": "08:30",
            "closes": "12:00",
        },
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Áreas de atuação",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": a["titulo"]}} for a in AREAS
        ],
    },
}

# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------
NAV_ITENS = [
    ("inicio", "Início"),
    ("areas", "Áreas de Atuação"),
    ("sobre", "Quem Somos"),
    ("servicos", "Consultoria"),
    ("faq", "Dúvidas"),
    ("contato", "Contato"),
]


def header(pagina="index", ativo="", base=""):
    """base="/" nas paginas servidas a partir da raiz (404 do GitHub Pages),
    onde o endereco solicitado pode ter varios niveis e os caminhos relativos
    resolveriam errado."""
    links = []
    for chave, label in NAV_ITENS:
        href = "#" + chave if pagina == "index" else f"{base}index.html#{chave}"
        cls = "nav__link is-active" if chave == ativo else "nav__link"
        links.append(f'        <a class="{cls}" href="{href}">{label}</a>')
    return f"""
<header class="site-header" id="siteHeader">
  <div class="container site-header__inner">
    <a class="brand" href="{base}index.html" aria-label="{E(SITE['nome'])} — início">
      <span class="brand__mark"><img src="{base}assets/img/logo-mma-3x.png" width="181" height="180" alt="Logomarca MMA"></span>
      <span class="brand__text">
        <strong>Advocacia e Consultoria Jurídica MMA</strong>
        <span>{E(SITE['advogado'])} · {E(SITE['oab'])}</span>
      </span>
    </a>
    <nav class="nav" id="mainNav" aria-label="Navegação principal">
{chr(10).join(links)}
      <a class="btn btn--wa btn--block nav__cta" href="{wa_geral()}" target="_blank" rel="noopener">
        {icon('wa', 'ico ico--wa', 18)} Falar no WhatsApp
      </a>
    </nav>
    <button class="nav-toggle" id="navToggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="mainNav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="nav-backdrop" id="navBackdrop" hidden></div>
"""


def footer(base=""):
    areas_links = "\n".join(
        f'          <li><a href="{base}areas.html#{a["slug"]}">{E(a["titulo"])}</a></li>' for a in AREAS
    )
    cr = SITE["credito"]
    credit = (
        f'      <p class="footer__credit">{E(cr["rotulo"])} '
        f'<a href="{E(cr["url"])}" target="_blank" rel="nofollow noopener">'
        f'<img src="{base}{E(cr["logo"])}" width="{cr["logo_w"]}" height="{cr["logo_h"]}" '
        f'alt="{E(cr["nome"])}" loading="lazy">'
        f'<span>{E(cr["nome"])}</span></a></p>'
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <span class="brand__mark brand__mark--lg"><img src="{base}assets/img/logo-mma-3x.png" width="181" height="180" alt="Logomarca MMA"></span>
        <h2>Advocacia e<br>Consultoria Jurídica MMA</h2>
        <p class="footer__name">{E(SITE['advogado'])}<br>Advogado — {E(SITE['oab'])}</p>
        <a class="btn btn--wa" href="{wa_geral()}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Agendar atendimento</a>
      </div>

      <div class="footer__col">
        <h3>Áreas de atuação</h3>
        <ul class="footer__list footer__list--areas">
{areas_links}
        </ul>
      </div>

      <div class="footer__col">
        <h3>Contato</h3>
        <ul class="footer__contact">
          <li>{icon('pin', 'ico ico--foot', 20)}<a href="{SITE['maps']}" target="_blank" rel="noopener">{E(SITE['endereco'])}<br>{E(SITE['cidade'])}</a></li>
          <li>{icon('phone', 'ico ico--foot', 20)}<a href="tel:{SITE['telefone_link']}">{E(SITE['telefone'])}</a></li>
          <li>{icon('mail', 'ico ico--foot', 20)}<a href="mailto:{SITE['email']}">{E(SITE['email'])}</a></li>
          <li>{icon('clock', 'ico ico--foot', 20)}<ul class="footer__hours">{HOURS_LI}</ul></li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom">
      <p>© {YEAR} {E(SITE['advogado'])} — {E(SITE['nome'])}. Todos os direitos reservados.</p>
      <p class="footer__note">Os conteúdos publicados neste site têm caráter informativo e não substituem a consultoria jurídica individual. {E(SITE['sigilo'])}</p>
      <p class="footer__links"><a href="{base}privacidade.html">Política de Privacidade</a><span>·</span><a href="{SITE['maps']}" target="_blank" rel="noopener">Como chegar</a></p>
{credit}
    </div>
  </div>
</footer>

<a class="float-wa" href="{wa_geral()}" target="_blank" rel="noopener" aria-label="Falar com o escritório no WhatsApp">
  <span class="float-wa__mark"><img src="{base}assets/img/logo-mma-3x.png" width="181" height="180" alt=""></span>
  <span class="float-wa__label">WhatsApp</span>
</a>
"""


def head(titulo, descricao, canonical, base=""):
    if canonical:
        url = f"https://{SITE['dominio']}/{canonical}"
        robots = "index, follow"
    else:
        url = f"https://{SITE['dominio']}/"
        robots = "noindex, follow"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta name="author" content="{E(SITE['advogado'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{E(SITE['nome'])}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://{SITE['dominio']}/assets/img/logo-mma-3x.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000F22">
<link rel="icon" href="{base}assets/img/favicon-32.png" sizes="32x32">
<link rel="icon" href="{base}assets/img/favicon.png" sizes="96x96">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('assets/css/styles.css', base)}">
<script type="application/ld+json">
{json.dumps(ORG_JSON, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
"""


def section_head(eyebrow, title, sub=None):
    subhtml = f'\n        <p class="section__sub">{sub}</p>' if sub else ""
    return f"""
      <div class="section__head">
        <span class="eyebrow">{eyebrow}</span>
        <h2 class="section__title">{title}</h2>{subhtml}
      </div>
"""


def cta_band():
    return f"""
    <section class="cta-band">
      <div class="container cta-band__inner">
        <div>
          <h2>Vamos conversar sobre o seu caso?</h2>
          <p>A primeira orientação é gratuita e sigilosa. Em poucos minutos você entende os caminhos possíveis.</p>
        </div>
        <a class="btn btn--gold btn--lg" href="{wa_geral('consulta inicial gratuita')}" target="_blank" rel="noopener">
          {icon('wa', 'ico ico--wa', 20)} Chamar no WhatsApp
        </a>
      </div>
    </section>
"""


# ---------------------------------------------------------------------------
# BLOCOS DE CONTEÚDO
# ---------------------------------------------------------------------------
def area_card(a, full=False):
    lista = ""
    if full:
        lista = '<ul class="area__list">' + "".join(
            f'<li>{icon("check", "ico ico--sm", 15)}{E(h)}</li>' for h in a["destaques"]
        ) + "</ul>"
    return f"""        <article class="area reveal" id="{a['slug']}">
          <span class="area__icon">{icon(a['icone'], 'ico', 24)}</span>
          <h3 class="area__title">{E(a['titulo'])}</h3>
          <p class="area__text">{E(a['desc'])}</p>
{lista}          <a class="area__link" href="{wa_area(a)}" target="_blank" rel="noopener">
            {icon('wa', 'ico ico--sm ico--wa', 16)} Falar sobre esta área
          </a>
        </article>
"""


def form_block():
    options = "\n".join(f'                <option value="{E(a["titulo"])}">{E(a["titulo"])}</option>' for a in AREAS)
    return f"""        <form class="form" id="contactForm" novalidate>
          <div class="form__row">
            <label class="field">
              <span>Nome completo *</span>
              <input type="text" name="nome" required autocomplete="name" placeholder="Como podemos chamar você?">
            </label>
            <label class="field">
              <span>Telefone / WhatsApp *</span>
              <input type="tel" name="telefone" required autocomplete="tel" placeholder="(71) 99999-9999">
            </label>
          </div>
          <label class="field">
            <span>E-mail *</span>
            <input type="email" name="email" required autocomplete="email" placeholder="seu@email.com">
          </label>
          <label class="field">
            <span>Área do Direito</span>
            <select name="area">
              <option value="">Selecione (opcional)</option>
{options}
              <option value="Não sei informar">Não sei informar</option>
            </select>
          </label>
          <label class="field">
            <span>Descreva seu caso *</span>
            <textarea name="mensagem" rows="5" required placeholder="Relate os fatos com o máximo de detalhes possível. Evite inserir dados sensíveis de terceiros."></textarea>
          </label>
          <p class="form__legal">Ao enviar, você autoriza o contato do escritório. O atendimento é sigiloso e nenhum dado é compartilhado com terceiros.</p>
          <div class="form__actions">
            <button class="btn btn--gold" type="submit">{icon('wa', 'ico ico--wa', 18)} Enviar pelo WhatsApp</button>
            <a class="btn btn--ghost-dark" href="mailto:{SITE['email']}">Enviar por e-mail</a>
          </div>
          <p class="form__status" id="formStatus" role="status" aria-live="polite"></p>
        </form>
"""


def faq_block():
    return "\n".join(
        f"""        <details class="faq__item reveal">
          <summary><span>{E(q)}</span>{icon('arrow', 'ico ico--faq', 20)}</summary>
          <div class="faq__answer"><p>{E(a)}</p></div>
        </details>"""
        for q, a in FAQ
    )


def hero():
    return f"""
<section class="hero" id="inicio">
  <div class="hero__bg"></div>
  <div class="hero__overlay"></div>
  <div class="container hero__inner">
    <div class="hero__content">
      <span class="eyebrow eyebrow--light">{E(SITE['oab'])} · Salvador/BA</span>
      <h1 class="hero__title">Advocacia e<br>Consultoria Jurídica <span class="gold">MMA</span></h1>
      <p class="hero__lead">
        Atuação firme, técnica e sigilosa em <strong>{N_AREAS} áreas do Direito</strong> para pessoas,
        empresas e servidores públicos. Análise clara do seu caso antes de qualquer decisão,
        sempre com o advogado responsável pelo atendimento.
      </p>
      <div class="hero__actions">
        <a class="btn btn--gold" href="{wa_geral('consulta inicial gratuita')}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Falar no WhatsApp</a>
        <a class="btn btn--ghost" href="areas.html">Conhecer as áreas de atuação</a>
      </div>
      <ul class="hero__chips">
        <li>{icon('check', 'ico ico--sm', 16)} Consulta inicial gratuita</li>
        <li>{icon('check', 'ico ico--sm', 16)} Sigilo absoluto</li>
        <li>{icon('check', 'ico ico--sm', 16)} Atendimento remoto</li>
      </ul>
    </div>

    <aside class="hero__card reveal">
      <div class="hero__card-head">
        <span class="brand__mark brand__mark--md"><img src="assets/img/logo-mma-3x.png" width="181" height="180" alt="Logomarca MMA"></span>
        <div>
          <strong>{E(SITE['advogado'])}</strong>
          <span>Advogado — {E(SITE['oab'])}</span>
        </div>
      </div>
      <p class="hero__card-quote">“O direito não pertence ao advogado: pertence a quem vive. Nosso trabalho é garantir que ele seja respeitado.”</p>
      <ul class="hero__card-list">
        <li>{icon('phone', 'ico ico--sm', 18)}<a href="tel:{SITE['telefone_link']}">{E(SITE['telefone'])}</a></li>
        <li>{icon('pin', 'ico ico--sm', 18)}<a href="{SITE['maps']}" target="_blank" rel="noopener">{E(SITE['endereco'])}<small>{E(SITE['cidade'])}</small></a></li>
        <li>{icon('mail', 'ico ico--sm', 18)}<a href="mailto:{SITE['email']}">{E(SITE['email'])}</a></li>
      </ul>
    </aside>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# PÁGINAS
# ---------------------------------------------------------------------------
def page_index():
    areas_grid = "\n".join(area_card(a) for a in AREAS)
    servicos = "\n".join(
        f"""        <article class="svc reveal">
          <span class="svc__icon">{icon(s['icone'], 'ico', 24)}</span>
          <h3>{E(s['titulo'])}</h3>
          <p>{E(s['desc'])}</p>
          <ul class="svc__meta">{''.join(f'<li>{E(m)}</li>' for m in s['meta'])}</ul>
        </article>"""
        for s in SERVICOS
    )
    passos = "\n".join(
        f"""          <li class="step reveal">
            <span class="step__num">{n}</span>
            <h3>{E(t)}</h3>
            <p>{E(d)}</p>
          </li>"""
        for n, t, d in PASSOS
    )
    diferenciais = "\n".join(
        f"""          <li class="diff reveal">{icon('spark', 'ico ico--sm', 18)}<span>{E(t)}<small>{E(d)}</small></span></li>"""
        for t, d in DIFERENCIAIS
    )

    return (
        head(
            f"{SITE['nome']} | {SITE['advogado']} — {SITE['oab']}",
            SITE["descricao_meta"],
            "",
        )
        + header("index", "inicio")
        + '<main id="conteudo">'
        + hero()
        + f"""
    <section class="strip">
      <div class="container strip__grid">
        <div class="strip__item reveal"><strong>{N_AREAS}</strong><span>Áreas do Direito</span></div>
        <div class="strip__item reveal"><strong>{E(SITE['oab_num'])}</strong><span>Inscrição na OAB/BA</span></div>
        <div class="strip__item reveal"><strong>100%</strong><span>Sigilo e confidencialidade</span></div>
        <div class="strip__item reveal"><strong>BA</strong><span>Salvador e atendimento remoto</span></div>
      </div>
    </section>

    <section class="section" id="sobre">
      <div class="container about__grid">
        <div class="about__media reveal">
          <img src="assets/img/escritorio.jpg" alt="Escritório de advocacia — {E(SITE['nome'])}" loading="lazy" width="800" height="600">
          <div class="about__badge">
            <span class="brand__mark brand__mark--sm"><img src="assets/img/logo-mma-3x.png" width="181" height="180" alt=""></span>
            <div><strong>{E(SITE['advogado'])}</strong><span>Advogado — {E(SITE['oab'])}</span></div>
          </div>
        </div>
        <div class="about__content reveal">
          <span class="eyebrow">Quem somos</span>
          <h2 class="section__title section__title--left">Advocacia e Consultoria Jurídica MMA</h2>
          <p class="lead">
            O escritório <strong>{E(SITE['nome'])}</strong> atua na defesa e na consultoria jurídica
            com uma proposta simples: entender o caso antes de agir, explicar com clareza cada
            alternativa e entregar um serviço justo, sigiloso e responsável.
          </p>
          <p>
            São <strong>{N_AREAS} áreas de atuação</strong>, do Direito Administrativo ao Tributário. Cada
            demanda é analisada individualmente e a estratégia é definida em conjunto com o cliente,
            com valores e prazos informados antes do início dos trabalhos.
          </p>
          <ul class="about__list">
            <li>{icon('check', 'ico ico--sm', 18)} Atendimento feito diretamente pelo advogado responsável</li>
            <li>{icon('check', 'ico ico--sm', 18)} Escopo, prazos e valores definidos antes da contratação</li>
            <li>{icon('check', 'ico ico--sm', 18)} {E(SITE['sigilo'])}</li>
            <li>{icon('check', 'ico ico--sm', 18)} Presencial em Salvador/BA e remoto para todo o Brasil</li>
          </ul>
          <div class="about__actions">
            <a class="btn btn--gold" href="{wa_geral()}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Falar com o advogado</a>
            <a class="btn btn--ghost-dark" href="sobre.html">Saiba mais</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" id="areas">
      <div class="container">
        {section_head("Especialidades", "Áreas de atuação do Direito",
                      f"Atuação em {N_AREAS} áreas, do Direito Administrativo ao Tributário. Escolha a sua necessidade e fale direto com o advogado pelo WhatsApp.")}
        <div class="areas-grid">
{areas_grid}
        </div>
        <div class="areas__cta reveal">
          <p>Não encontrou a sua necessidade ou o seu caso envolve mais de uma área?</p>
          <a class="btn btn--wa" href="{wa_geral('orientação sobre o meu caso')}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Descrever meu caso</a>
        </div>
      </div>
    </section>

    <section class="section" id="servicos">
      <div class="container">
        {section_head("Serviços", "Consultoria jurídica sob medida",
                      "Da primeira conversa à conclusão do trabalho, cada etapa é conduzida com estratégia, técnica e transparência.")}
        <div class="services-grid">
{servicos}
        </div>
        <div class="steps" id="como-funciona">
          <h3 class="steps__title">Como funciona o atendimento</h3>
          <ol class="steps__grid">
{passos}
          </ol>
        </div>
      </div>
    </section>

    <section class="section section--cream">
      <div class="container">
        {section_head("Diferenciais", "Por que o MMA")}
        <ul class="diffs">
{diferenciais}
        </ul>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="container container--narrow">
        {section_head("Dúvidas", "Perguntas frequentes", "As respostas mais comuns sobre o atendimento do escritório.")}
        <div class="faq">
{faq_block()}
        </div>
        <p class="faq__foot">Não encontrou sua dúvida?
          <a href="{wa_geral('uma dúvida sobre o atendimento')}" target="_blank" rel="noopener">Pergunte no WhatsApp {icon('arrow', 'ico ico--sm', 16)}</a>
        </p>
      </div>
    </section>
"""
        + cta_band()
        + f"""
    <section class="section section--dark" id="contato">
      <div class="container">
        {section_head("Contato", "Entre em contato", "Prefere presencial? Estamos em Salvador/BA. Para os demais estados, atendimento por videoconferência.")}
        <div class="contact-grid">
          <div class="contact-info reveal">
            <ul class="contact-list">
              <li>{icon('pin', 'ico ico--foot', 22)}<div><strong>Endereço</strong>
                <a href="{SITE['maps']}" target="_blank" rel="noopener">{E(SITE['endereco'])}<br>{E(SITE['cidade'])}</a>
                <a class="link-sm" href="{SITE['maps']}" target="_blank" rel="noopener">Ver no mapa {icon('arrow', 'ico ico--sm', 14)}</a>
              </div></li>
              <li>{icon('phone', 'ico ico--foot', 22)}<div><strong>Telefone / WhatsApp</strong>
                <a href="tel:{SITE['telefone_link']}">{E(SITE['telefone'])}</a></div></li>
              <li>{icon('mail', 'ico ico--foot', 22)}<div><strong>E-mail</strong>
                <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a></div></li>
              <li>{icon('clock', 'ico ico--foot', 22)}<div><strong>Horário de funcionamento</strong>
                <ul class="hours">{HOURS_LI}</ul></div></li>
            </ul>
            <div class="contact__img"><img src="assets/img/cidade.jpg" alt="Salvador, Bahia" loading="lazy" width="800" height="500"></div>
          </div>
          <div class="contact-form reveal">
            <h3 class="contact-form__title">Envie sua mensagem</h3>
            <p class="contact-form__lead">Preencha o formulário e o texto será aberto direto no WhatsApp do escritório para envio.</p>
{form_block()}
          </div>
        </div>
      </div>
    </section>
"""
        + "</main>"
        + footer()
        + f'<script src="{asset("assets/js/main.js")}" defer></script>\n</body>\n</html>\n'
    )


def page_areas():
    cards = "\n".join(area_card(a, full=True) for a in AREAS)
    pills = "\n".join(
        f'        <a class="pill" href="#{a["slug"]}">{E(a["titulo"].replace("Direito ", ""))}</a>'
        for a in AREAS
    )
    return (
        head(
            f"Áreas de Atuação | {SITE['nome']}",
            f"Atuação em {N_AREAS} áreas do Direito: {areas_nomes_meta()}.",
            "areas.html",
        )
        + header("areas", "areas")
        + f"""
    <main id="conteudo">
      <section class="page-hero">
        <div class="container">
          <span class="eyebrow eyebrow--light">Especialidades</span>
          <h1>Áreas de atuação</h1>
          <p>{N_AREAS} áreas do Direito, com análise individual de cada caso. Escolha a sua e fale direto com o
             advogado responsável pelo atendimento.</p>
        </div>
      </section>

      <section class="section section--dark">
        <div class="container">
          <nav class="pills" aria-label="Ir para uma área de atuação">
{pills}
          </nav>
          <div class="areas-grid areas-grid--full">
{cards}
          </div>
          <div class="areas__cta reveal">
            <p>Seu caso não se encaixa nessas áreas ou envolve mais de uma?</p>
            <a class="btn btn--wa" href="{wa_geral('orientação sobre o meu caso')}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Descrever meu caso</a>
          </div>
        </div>
      </section>
"""
        + cta_band()
        + "</main>"
        + footer()
        + f'<script src="{asset("assets/js/main.js")}" defer></script>\n</body>\n</html>\n'
    )


def page_sobre():
    difs_dark = "\n".join(
        f'          <li class="diff reveal">{icon("spark", "ico ico--sm", 18)}<span>{E(t)}<small>{E(d)}</small></span></li>'
        for t, d in DIFERENCIAIS
    )
    return (
        head(
            f"Quem Somos | {SITE['nome']}",
            f"Conheça {SITE['advogado']}, advogado {SITE['oab']}, e a proposta da Advocacia e Consultoria "
            f"Jurídica MMA: atendimento direto, sigilo absoluto e transparência.",
            "sobre.html",
        )
        + header("sobre", "sobre")
        + f"""
    <main id="conteudo">
      <section class="page-hero">
        <div class="container">
          <span class="eyebrow eyebrow--light">Quem somos</span>
          <h1>Advocacia e Consultoria Jurídica MMA</h1>
          <p>{E(SITE['advogado'])} — Advogado, {E(SITE['oab'])}</p>
        </div>
      </section>

      <section class="section">
        <div class="container about__grid">
          <div class="about__content reveal">
            <span class="eyebrow">O escritório</span>
            <h2 class="section__title section__title--left">Direito a serviço de quem precisa</h2>
            <p class="lead">
              A Advocacia e Consultoria Jurídica MMA nasceu para simplificar a relação entre advogado e
              cliente: informação clara, escopo definido e sigilo como regra.
            </p>
            <p>
              Atendemos pessoas físicas, empresas e servidores públicos nas {N_AREAS} áreas do Direito listadas
              neste site — da consulta inicial à execução da decisão, sempre com o advogado responsável
              presente no acompanhamento.
            </p>
            <ul class="about__list">
              <li>{icon('check', 'ico ico--sm', 18)} {E(SITE['sigilo'])}</li>
              <li>{icon('check', 'ico ico--sm', 18)} Valores e escopo apresentados por escrito</li>
              <li>{icon('check', 'ico ico--sm', 18)} Atendimento presencial e remoto</li>
              <li>{icon('check', 'ico ico--sm', 18)} Prazo de resposta combinado com o cliente</li>
            </ul>
            <div class="about__actions">
              <a class="btn btn--gold" href="{wa_geral()}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Falar no WhatsApp</a>
              <a class="btn btn--ghost-dark" href="areas.html">Ver as {N_AREAS} áreas</a>
            </div>
          </div>
          <div class="about__media reveal">
            <img src="assets/img/reuniao.jpg" alt="Atendimento jurídico no escritório" loading="lazy" width="800" height="600">
          </div>
        </div>
      </section>

      <section class="section section--dark">
        <div class="container">
          {section_head("Compromisso", "O que você pode esperar do MMA")}
          <ul class="diffs">
{difs_dark}
          </ul>
        </div>
      </section>
"""
        + cta_band()
        + "</main>"
        + footer()
        + f'<script src="{asset("assets/js/main.js")}" defer></script>\n</body>\n</html>\n'
    )


def page_contato():
    return (
        head(
            f"Contato | {SITE['nome']}",
            f"Fale com {SITE['advogado']} ({SITE['oab']}): WhatsApp {SITE['telefone']}, e-mail {SITE['email']} "
            f"e endereço em Salvador/BA. Atendimento sigiloso.",
            "contato.html",
        )
        + header("contato", "contato")
        + f"""
    <main id="conteudo">
      <section class="page-hero">
        <div class="container">
          <span class="eyebrow eyebrow--light">Contato</span>
          <h1>Fale com o advogado</h1>
          <p>Resposta em horário comercial, sempre de forma sigilosa. Escolha o canal que preferir.</p>
        </div>
      </section>

      <section class="section section--dark">
        <div class="container">
          <div class="contact-grid">
            <div class="contact-info reveal">
              <ul class="contact-list">
                <li>{icon('wa', 'ico ico--foot ico--wa', 22)}<div><strong>WhatsApp (canal preferencial)</strong>
                  <a href="{wa_geral()}" target="_blank" rel="noopener">{E(SITE['telefone'])}</a></div></li>
                <li>{icon('phone', 'ico ico--foot', 22)}<div><strong>Telefone</strong>
                  <a href="tel:{SITE['telefone_link']}">{E(SITE['telefone'])}</a></div></li>
                <li>{icon('mail', 'ico ico--foot', 22)}<div><strong>E-mail</strong>
                  <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a></div></li>
                <li>{icon('pin', 'ico ico--foot', 22)}<div><strong>Endereço</strong>
                  <a href="{SITE['maps']}" target="_blank" rel="noopener">{E(SITE['endereco'])}<br>{E(SITE['cidade'])}</a></div></li>
                <li>{icon('clock', 'ico ico--foot', 22)}<div><strong>Horário de funcionamento</strong>
                  <ul class="hours">{HOURS_LI}</ul></div></li>
              </ul>
            </div>
            <div class="contact-form reveal">
              <h3 class="contact-form__title">Envie sua mensagem</h3>
              <p class="contact-form__lead">O texto será aberto direto no WhatsApp do escritório.</p>
{form_block()}
            </div>
          </div>
        </div>
      </section>

      <section class="section section--cream">
        <div class="container about__grid">
          <div class="about__media reveal">
            <img src="assets/img/cidade.jpg" alt="Salvador, Bahia" loading="lazy" width="800" height="500">
          </div>
          <div class="about__content reveal">
            <span class="eyebrow">Onde estamos</span>
            <h2 class="section__title section__title--left">Salvador/BA e atendimento remoto</h2>
            <p class="lead">
              O escritório atende presencialmente em Salvador e, por videoconferência, clientes de todo
              o Brasil — com a mesma seriedade e o mesmo sigilo.
            </p>
            <p>
              Antes de qualquer atendimento presencial, confirme a disponibilidade de agenda pelo
              WhatsApp. Documentos podem ser enviados por e-mail para análise prévia.
            </p>
            <a class="btn btn--gold" href="{SITE['maps']}" target="_blank" rel="noopener">Abrir no Google Maps {icon('arrow', 'ico ico--sm', 18)}</a>
          </div>
        </div>
      </section>
"""
        + "</main>"
        + footer()
        + f'<script src="{asset("assets/js/main.js")}" defer></script>\n</body>\n</html>\n'
    )


def page_privacidade():
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    return (
        head(
            f"Política de Privacidade | {SITE['nome']}",
            "Como o escritório trata os dados pessoais coletados neste site, em conformidade com a Lei "
            "Geral de Proteção de Dados (Lei 13.709/2018).",
            "privacidade.html",
        )
        + header("privacidade")
        + f"""
    <main id="conteudo">
      <section class="page-hero">
        <div class="container">
          <span class="eyebrow eyebrow--light">Transparência</span>
          <h1>Política de Privacidade</h1>
          <p>Como os seus dados pessoais são tratados, em conformidade com a Lei nº 13.709/2018 (LGPD).</p>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow prose">
          <p class="prose__lead">Última atualização: {hoje}</p>

          <h2>1. Quem controla os dados</h2>
          <p><strong>{E(SITE['nome'])}</strong>, com sede em {E(SITE['endereco'])}, {E(SITE['cidade'])},
             é a controladora dos dados pessoais coletados neste site. Para assuntos de privacidade,
             escreva para <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a>.</p>

          <h2>2. Quais dados coletamos</h2>
          <p>Coletamos apenas os dados enviados voluntariamente: nome, telefone, e-mail e a descrição do
             caso informada nos formulários e mensagens. Não solicitamos dados de crianças e adolescentes
             nem de pessoas em situação de vulnerabilidade; havendo tal hipótese, aplicamos o Estatuto da
             Criança e do Adolescente.</p>

          <h2>3. Finalidades e bases legais</h2>
          <p>Os dados são tratados para (i) responder a solicitações e prestar consultoria jurídica;
             (ii) analisar o caso e apresentar proposta de honorários; e (iii) executar o serviço
             contratado, quando houver. As bases legais são o consentimento do titular, a execução de
             procedimentos preliminares a contrato, o cumprimento de obrigação legal ou regulatória e o
             legítimo interesse na organização do atendimento.</p>

          <h2>4. Sigilo profissional</h2>
          <p>{E(SITE['sigilo'])} Nenhuma informação é compartilhada com terceiros sem autorização
             expressa, salvo hipótese legal de requisição de autoridade competente.</p>

          <h2>5. Compartilhamento e transferência internacional</h2>
          <p>Não vendemos, alugamos nem cedemos dados a terceiros. Compartilhamentos ocorrem apenas com
             prestadores de serviço necessários (e-mail, agenda, armazenamento), sob obrigação de
             confidencialidade, ou por determinação legal.</p>

          <h2>6. Armazenamento e segurança</h2>
          <p>As informações são armazenadas em ambientes protegidos, com acesso restrito ao advogado
             responsável. Mensagens de WhatsApp utilizadas para atendimento não são compartilhadas nem
             usadas para fins publicitários.</p>

          <h2>7. Retenção</h2>
          <p>Dados de contatos que não resultaram em atendimento são mantidos pelo período necessário ao
             cumprimento de obrigações legais e ao prazo de prescrição das ações relacionadas. Dados
             relativos a processos são mantidos pelo prazo aplicável ao exercício da advocacia.</p>

          <h2>8. Direitos do titular</h2>
          <p>Nos termos da LGPD, o titular pode solicitar confirmação de tratamento, acesso, correção,
             anonimização ou bloqueio dos dados, revogar o consentimento e eliminar dados desnecessários.
             Para exercer qualquer direito, escreva para <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a>.</p>

          <h2>9. Cookies</h2>
          <p>Este site não utiliza cookies de publicidade nem de rastreamento de comportamento. Apenas
             recursos técnicos necessários ao funcionamento das páginas são carregados.</p>

          <h2>10. Alterações desta política</h2>
          <p>Esta política pode ser atualizada a qualquer tempo. A data da última atualização é sempre
             indicada no início desta página.</p>
        </div>
      </section>
"""
        + "</main>"
        + footer()
        + f'<script src="{asset("assets/js/main.js")}" defer></script>\n</body>\n</html>\n'
    )


# ---------------------------------------------------------------------------
# PÁGINA 404 (servida pelo GitHub Pages em qualquer endereço inexistente)
# ---------------------------------------------------------------------------
def page_404():
    return (
        head(
            f"Página não encontrada | {SITE['nome']}",
            "A página procurada não existe ou mudou de endereço. Use os atalhos abaixo para continuar.",
            "",
            base="/",
        )
        + header("404", "", base="/")
        + f"""
    <main id="conteudo">
      <section class="page-hero">
        <div class="container">
          <span class="eyebrow eyebrow--light">Erro 404</span>
          <h1>Página não encontrada</h1>
          <p>O endereço acessado não existe ou foi movido. Siga pelos atalhos abaixo para chegar ao conteúdo.</p>
        </div>
      </section>

      <section class="section">
        <div class="container about__actions reveal">
          <a class="btn btn--gold" href="/index.html">Ir para o início</a>
          <a class="btn btn--ghost-dark" href="/areas.html">Áreas de atuação</a>
          <a class="btn btn--wa" href="{wa_geral()}" target="_blank" rel="noopener">{icon('wa', 'ico ico--wa', 18)} Falar no WhatsApp</a>
        </div>
      </section>
    </main>
"""
        + cta_band()
        + footer(base="/")
        + f'<script src="{asset("assets/js/main.js", "/")}" defer></script>\n</body>\n</html>\n'
    )


# ---------------------------------------------------------------------------
# ARQUIVOS EXTRAS
# ---------------------------------------------------------------------------
def write_extra():
    manifest = {
        "name": SITE["nome"],
        "short_name": "MMA Advocacia",
        "description": SITE["descricao_meta"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000F22",
        "theme_color": "#000F22",
        "lang": "pt-BR",
        "icons": [
            {"src": "/assets/img/favicon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    with open(os.path.join(DST, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(os.path.join(DST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: https://{SITE['dominio']}/sitemap.xml\n")

    hoje = datetime.date.today().isoformat()
    paginas = [("", "1.0", "weekly"), ("areas.html", "0.9", "monthly"), ("sobre.html", "0.7", "monthly"),
               ("contato.html", "0.8", "monthly"), ("privacidade.html", "0.3", "yearly")]
    urls = "\n".join(
        f"  <url>\n    <loc>https://{SITE['dominio']}/{p}</loc>\n    <lastmod>{hoje}</lastmod>\n"
        f"    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for p, pr, c in paginas
    )
    with open(os.path.join(DST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"{urls}\n</urlset>\n")

    vercel = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {"source": "/assets/(.*)",
             "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}
        ],
    }
    with open(os.path.join(DST, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(vercel, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(os.path.join(DST, ".vercelignore"), "w", encoding="utf-8") as f:
        f.write("arq\nbuild.py\nREADME.md\nCONTINUACAO.md\nRETOMAR-DOMINIO.md\nocr*.ps1\nprep_ocr*.py\n"
                "dl_img.py\nmake_logo.py\ncheck_logo.py\n")

    # --- GitHub Pages ---
    with open(os.path.join(DST, "CNAME"), "w", encoding="utf-8") as f:
        f.write(SITE["dominio"] + "\n")

    open(os.path.join(DST, ".nojekyll"), "w", encoding="utf-8").close()


def main():
    outputs = {
        "index.html": page_index(),
        "areas.html": page_areas(),
        "sobre.html": page_sobre(),
        "contato.html": page_contato(),
        "privacidade.html": page_privacidade(),
        "404.html": page_404(),
    }
    for name, content in outputs.items():
        with open(os.path.join(DST, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  {name:22} {len(content):>8,} bytes")
    write_extra()
    print("OK")


if __name__ == "__main__":
    main()