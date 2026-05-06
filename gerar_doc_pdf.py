from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus.tableofcontents import TableOfContents
import os

class MyDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
            elif style == 'Heading3':
                self.notify('TOCEntry', (2, text, self.page))

filepath = "Documentacao_Monitoramento_PC.pdf"
doc = MyDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=3*cm, topMargin=3*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

# ABNT basic styles
styles.add(ParagraphStyle(name='ABNT_Normal', fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, leading=18, spaceAfter=12)) # 1.5 line spacing (~18pt leading)
styles.add(ParagraphStyle(name='ABNT_Center', fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name='ABNT_Heading1', fontName='Helvetica-Bold', fontSize=12, spaceAfter=12, spaceBefore=12))
styles.add(ParagraphStyle(name='ABNT_Heading2', fontName='Helvetica-Bold', fontSize=12, spaceAfter=12, spaceBefore=12))
styles.add(ParagraphStyle(name='ABNT_List', fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, leading=18, leftIndent=20))

# Redefining Heading styles for TOC interception
styles['Heading1'].fontName = 'Helvetica-Bold'
styles['Heading1'].fontSize = 12
styles['Heading1'].spaceBefore = 12
styles['Heading1'].spaceAfter = 12

styles['Heading2'].fontName = 'Helvetica-Bold'
styles['Heading2'].fontSize = 12
styles['Heading2'].spaceBefore = 12
styles['Heading2'].spaceAfter = 12

styles['Heading3'].fontName = 'Helvetica-Bold'
styles['Heading3'].fontSize = 12
styles['Heading3'].spaceBefore = 12
styles['Heading3'].spaceAfter = 12

story = []

story.append(Paragraph("DOCUMENTAÇÃO DO PROTÓTIPO: MONITORAMENTO DE PC", styles['ABNT_Center']))
story.append(Spacer(1, 24))

toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(fontName='Helvetica-Bold', fontSize=12, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    ParagraphStyle(fontName='Helvetica', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=16),
    ParagraphStyle(fontName='Helvetica', fontSize=12, name='TOCHeading3', leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=16),
]
story.append(Paragraph("SUMÁRIO", styles['ABNT_Center']))
story.append(Spacer(1, 12))
story.append(toc)
story.append(PageBreak())

story.append(Paragraph("1 PROBLEMA", styles['Heading1']))
story.append(Paragraph("Atualmente, muitos usuários não possuem ferramentas simples e acessíveis para acompanhar o desempenho do computador. Isso dificulta a identificação de problemas como uso excessivo de CPU, consumo elevado de memória RAM e sobrecarga do sistema, podendo causar lentidão, travamentos e perda de produtividade.", styles['ABNT_Normal']))

story.append(Paragraph("2 OBJETIVO", styles['Heading1']))
story.append(Paragraph("Desenvolver uma aplicação capaz de monitorar os principais recursos do computador, como CPU, memória RAM e disco, apresentando informações claras ao usuário e gerando alertas em situações críticas.", styles['ABNT_Normal']))

story.append(Paragraph("3 JUSTIFICATIVA", styles['Heading1']))
story.append(Paragraph("A criação deste sistema é importante para auxiliar na manutenção preventiva e na otimização do desempenho dos computadores. Além disso, o projeto contribui para o desenvolvimento de habilidades práticas em programação, análise de dados e sistemas computacionais.", styles['ABNT_Normal']))

story.append(Paragraph("4 DESCRIÇÃO DO PROJETO", styles['Heading1']))
story.append(Paragraph("O sistema será desenvolvido em Python, utilizando bibliotecas especializadas em monitoramento, como psutil. A aplicação poderá apresentar uma interface simples, exibindo dados atualizados em tempo real, como porcentagem de uso da CPU, memória e armazenamento.", styles['ABNT_Normal']))

story.append(Paragraph("5 FUNCIONALIDADES", styles['Heading1']))
story.append(Paragraph("• Monitoramento de CPU em tempo real", styles['ABNT_List']))
story.append(Paragraph("• Monitoramento de memória RAM", styles['ABNT_List']))
story.append(Paragraph("• Monitoramento de disco", styles['ABNT_List']))
story.append(Paragraph("• Exibição de informações atualizadas continuamente", styles['ABNT_List']))
story.append(Paragraph("• Geração de alertas em caso de uso elevado", styles['ABNT_List']))
story.append(Spacer(1, 12))

story.append(Paragraph("6 RESULTADOS ESPERADOS", styles['Heading1']))
story.append(Paragraph("Espera-se que o sistema seja leve, eficiente e de fácil utilização, permitindo ao usuário identificar problemas rapidamente e melhorar o desempenho do computador.", styles['ABNT_Normal']))

story.append(Paragraph("7 VISÃO GERAL", styles['Heading1']))
story.append(Paragraph("Este prototipo eh um Super Dashboard desenvolvido em Streamlit, projetado para monitorar os recursos do sistema. Ele consolida a visualizacao de dados historicos em CSV, leitura de metricas ao vivo, gestao de processos e simulacoes para games.", styles['ABNT_Normal']))

story.append(Paragraph("8 ARQUITETURA E MÓDULOS PRINCIPAIS", styles['Heading1']))

story.append(Paragraph("8.1 Dashboard Principal (app.py)", styles['Heading2']))
story.append(Paragraph("O arquivo central utiliza Streamlit para gerar a interface interativa e ferramentas como Pandas e Matplotlib para analise de dados, alem de psutil para metricas em tempo real.", styles['ABNT_Normal']))
story.append(Paragraph("<b>Paginas do Menu Lateral:</b>", styles['ABNT_Normal']))
story.append(Paragraph("• <b>Dashboard Historico</b>: Visualizacao baseada em datasets (CSV) apresentando KPIs, graficos de uso da CPU vs RAM e distribuicao de temperatura.", styles['ABNT_List']))
story.append(Paragraph("• <b>Monitor em Tempo Real</b>: Captura ao vivo metricas de CPU, Memoria e Disco com exibicao de barras de progresso e emissao de alertas.", styles['ABNT_List']))
story.append(Paragraph("• <b>Gestao & Otimizador</b>: Exibe o Top 10 processos que mais consomem recursos do computador, com a funcionalidade de encerramento de tarefas pesadas pelo usuario.", styles['ABNT_List']))
story.append(Paragraph("• <b>Modo Gamer</b>: Detecta a execucao de jogos populares no sistema e realiza estimativas de impacto de performance e taxa de quadros (FPS).", styles['ABNT_List']))
story.append(Paragraph("• <b>Modo HUD</b>: Uma exibicao minimalista voltada para telas secundarias, com numeros contrastantes sendo atualizados continuamente.", styles['ABNT_List']))
story.append(Spacer(1, 12))

story.append(Paragraph("8.2 Ferramentas Utilizadas", styles['Heading2']))
story.append(Paragraph("A nova arquitetura removeu dependencias como Flask e SQLite em favor de um ecossistema mais performatico para analise de dados e visualizacao rapida.", styles['ABNT_Normal']))
story.append(Paragraph("<b>Tecnologias de Destaque:</b>", styles['ABNT_Normal']))
story.append(Paragraph("• <b>Streamlit</b>: Cria a interface inteira em Python de forma simples e rapida.", styles['ABNT_List']))
story.append(Paragraph("• <b>psutil</b>: Captura informacoes internas do hardware com maxima precisao.", styles['ABNT_List']))
story.append(Paragraph("• <b>Pandas & Matplotlib</b>: Manipulam e plotam dados brutos transformando-os em informacoes visuais legiveis.", styles['ABNT_List']))

story.append(Spacer(1, 12))

story.append(Paragraph("9 IMPACTO SOCIAL", styles['Heading1']))
story.append(Paragraph("Este projeto possui um significativo impacto tecnologico na sociedade ao democratizar o acesso ao monitoramento de hardware. Tradicionalmente, ferramentas avancadas de diagnostico de computadores sao complexas ou voltadas apenas para profissionais de TI. Ao disponibilizar um 'Super Dashboard' intuitivo, gratuito e automatizado, o projeto permite que usuarios comuns identifiquem gargalos de desempenho, realizem manutencoes preventivas e evitem a obsolescencia precoce de seus equipamentos.", styles['ABNT_Normal']))
story.append(Paragraph("Alem disso, a ferramenta contribui para a sustentabilidade: ao ajudar os usuarios a fecharem processos desnecessarios e otimizarem a maquina, ha uma reducao no consumo de energia eletrica e no desgaste dos componentes fisicos, o que mitiga a geracao de lixo eletronico (e-waste). Dessa forma, a tecnologia promove uma relacao mais consciente, produtiva e duradoura entre as pessoas e seus computadores pessoais no dia a dia.", styles['ABNT_Normal']))

doc.multiBuild(story)
print(f"PDF gerado com sucesso em: {os.path.abspath(filepath)}")
