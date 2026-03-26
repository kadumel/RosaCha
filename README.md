# Rosa Chá - Site Institucional em Django

Projeto institucional para a marca **Rosa Chá**, com foco em posicionamento premium, delicadeza visual e captação de orçamento.

## Stack

- Python 3
- Django 5
- Django Templates
- CSS customizado
- SQLite (desenvolvimento)

## Estrutura principal

- `rosacha_project/` - configuração do projeto Django
- `core/` - app principal com páginas institucionais e formulário de contato
- `templates/` - templates base, includes e páginas
- `static/` - CSS e JS
- `media/` - preparado para mídias futuras

## Funcionalidades implementadas

- Páginas: Home, Sobre, Serviços, Galeria e Contato
- Design system com paleta premium da marca
- Layout responsivo para desktop e mobile
- SEO básico com `title` e `meta description` dinâmicos
- Formulário funcional de contato com validação
- Persistência de leads no banco via model `Lead`
- Django Admin configurado para visualizar mensagens
- Includes reutilizáveis (`header`, `footer`, `cta`)

## Como rodar localmente

1. Criar ambiente virtual:
   - macOS/Linux: `python3 -m venv .venv`
2. Ativar ambiente virtual:
   - macOS/Linux: `source .venv/bin/activate`
3. Instalar dependências:
   - `pip install -r requirements.txt`
4. Aplicar migrações:
   - `python manage.py migrate`
5. Criar usuário admin (opcional):
   - `python manage.py createsuperuser`
6. Iniciar servidor:
   - `python manage.py runserver`
7. Acessar:
   - Site: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

## Observações

- O layout da galeria está pronto para receber imagens reais (formatos horizontal, vertical e destaque).
- Links de WhatsApp/Instagram estão como placeholders e podem ser atualizados facilmente nos templates.
