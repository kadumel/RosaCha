from pathlib import Path
import unicodedata

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LeadForm
from .models import CategoriaGaleria, EventoGaleria, ImagemGaleria


def normalize_text(value):
    normalized = unicodedata.normalize('NFKD', value.lower())
    return ''.join(ch for ch in normalized if ch.isalnum())


def get_icons_by_name():
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        return {}

    icons_dir = media_root / 'icones'
    if not icons_dir.exists():
        icons_dir = media_root / 'Icones'
    if not icons_dir.exists():
        return {}

    allowed_suffixes = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'}
    icons_map = {}

    for file_path in icons_dir.rglob('*'):
        if not file_path.is_file() or file_path.suffix.lower() not in allowed_suffixes:
            continue
        relative = file_path.relative_to(media_root).as_posix()
        key = normalize_text(file_path.stem)
        icons_map[key] = f'{settings.MEDIA_URL}{relative}'

    return icons_map


def find_icon_by_keywords(icons_map, keywords):
    for keyword in keywords:
        token = normalize_text(keyword)
        for icon_name, icon_url in icons_map.items():
            if token in icon_name:
                return icon_url
    return ''


def get_hero_carousel_images():
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        return []

    carousel_dir = media_root / 'carrossel'
    if not carousel_dir.exists():
        carousel_dir = media_root / 'Carrossel'
    if not carousel_dir.exists():
        return []

    allowed_suffixes = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    image_urls = []

    for file_path in carousel_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in allowed_suffixes:
            relative = file_path.relative_to(media_root).as_posix()
            image_urls.append(f'{settings.MEDIA_URL}{relative}')

    return sorted(image_urls)


def get_service_cards():
    images = get_hero_carousel_images()
    icons_map = get_icons_by_name()
    services = [
        {
            'titulo': 'Catering para eventos intimistas',
            'descricao': 'Planejamento e execução de serviço completo para encontros com atmosfera acolhedora e estética refinada.',
            'itens': [
                'Curadoria de menu conforme perfil do evento',
                'Apresentação harmoniosa de pratos e apoio de mesa',
                'Coordenação atenta ao fluxo da recepção',
            ],
            'cta': 'Solicitar proposta',
            'icon_keywords': ['catering', 'evento', 'mesa'],
        },
        {
            'titulo': 'Mesas temáticas e experiências especiais',
            'descricao': 'Composição visual com linguagem floral sutil para destacar aniversários, noivados, brunches e celebrações autorais.',
            'itens': [
                'Definição de conceito visual e paleta',
                'Seleção de peças decorativas e elementos de apoio',
                'Montagem fina com acabamento artesanal',
            ],
            'cta': 'Conversar sobre conceito',
            'icon_keywords': ['mesa', 'tematica', 'decoracao', 'floral'],
        },
        {
            'titulo': 'Chá da tarde e recepções elegantes',
            'descricao': 'Experiências delicadas para receber com charme, leveza e atenção aos detalhes de hospitalidade.',
            'itens': [
                'Cardápio equilibrado para ocasiões diurnas',
                'Montagem editorial de mesa e ilhas de apoio',
                'Ritmo de serviço confortável para convidados',
            ],
            'cta': 'Planejar recepção',
            'icon_keywords': ['cha', 'xicara', 'recepcao'],
        },
        {
            'titulo': 'Projetos personalizados',
            'descricao': 'Desenvolvimento sob consulta para propostas com necessidades específicas de atendimento, estética e operação.',
            'itens': [
                'Briefing estratégico e diagnóstico do evento',
                'Plano de execução por etapas',
                'Acompanhamento próximo até a entrega',
            ],
            'cta': 'Solicitar orçamento',
            'icon_keywords': ['projeto', 'personalizado', 'consultoria'],
        },
    ]

    # Troca intencional entre os serviços "Mesas temáticas" e "Chá da tarde"
    # para manter o alinhamento visual solicitado.
    image_order = [0, 2, 1, 3]
    for index, service in enumerate(services):
        image_index = image_order[index] if index < len(image_order) else index
        service['image_url'] = images[image_index] if image_index < len(images) else ''
        service['icon_url'] = find_icon_by_keywords(icons_map, service['icon_keywords'])

    return services


def get_home_features():
    icons_map = get_icons_by_name()
    features = [
        {
            'titulo': 'Curadoria estética',
            'descricao': 'Composição visual harmônica com identidade premium.',
            'icon_keywords': ['curadoria', 'estetica', 'paleta', 'design'],
        },
        {
            'titulo': 'Apresentação delicada',
            'descricao': 'Peças e finalizações que valorizam cada detalhe.',
            'icon_keywords': ['apresentacao', 'detalhe', 'delicada'],
        },
        {
            'titulo': 'Atendimento personalizado',
            'descricao': 'Escuta atenta para traduzir o estilo de cada cliente.',
            'icon_keywords': ['atendimento', 'cliente', 'suporte'],
        },
        {
            'titulo': 'Experiência acolhedora',
            'descricao': 'Hospitalidade elegante para receber com leveza.',
            'icon_keywords': ['acolhedora', 'hospitalidade', 'receber'],
        },
        {
            'titulo': 'Identidade autoral',
            'descricao': 'Projetos memoráveis, sem aparência genérica.',
            'icon_keywords': ['identidade', 'autoral', 'marca'],
        },
    ]

    for feature in features:
        feature['icon_url'] = find_icon_by_keywords(icons_map, feature['icon_keywords'])

    return features


def get_contact_header_image():
    icons_map = get_icons_by_name()
    return find_icon_by_keywords(icons_map, ['contato', 'atendimento'])


def get_home_gallery_images(limit=9):
    return (
        ImagemGaleria.objects.filter(ativo=True, evento__ativo=True, destaque_home=True)
        .select_related('evento')
        .order_by('ordem', '-criado_em')[:limit]
    )


def home(request):
    hero_images = get_hero_carousel_images()
    services = get_service_cards()
    return render(
        request,
        'core/home.html',
        {
            'page_title': 'Rosa Chá | Catering e Experiências Elegantes',
            'meta_description': (
                'Rosa Chá cria experiências de catering intimistas com '
                'delicadeza, sofisticação e apresentação artesanal.'
            ),
            'hero_images': hero_images,
            'services': services,
            'features': get_home_features(),
            'home_gallery_images': get_home_gallery_images(),
        },
    )


def sobre(request):
    return render(
        request,
        'core/sobre.html',
        {
            'page_title': 'Sobre | Rosa Chá',
            'meta_description': 'Conheça a história e o cuidado autoral por trás da Rosa Chá.',
        },
    )


def servicos(request):
    return render(
        request,
        'core/servicos.html',
        {
            'page_title': 'Serviços | Rosa Chá',
            'meta_description': 'Serviços de catering, mesas temáticas e experiências personalizadas.',
            'services': get_service_cards(),
            'servicos_header_image': find_icon_by_keywords(get_icons_by_name(), ['cha_da_tarde', 'cha', 'tarde']),
        },
    )


def galeria(request):
    categoria_slug = request.GET.get('categoria', '').strip()
    evento_slug = request.GET.get('evento', '').strip()
    gallery_header_image = find_icon_by_keywords(get_icons_by_name(), ['orcamento', 'orçamento'])
    categorias = CategoriaGaleria.objects.filter(ativo=True).order_by('nome')
    eventos = EventoGaleria.objects.filter(ativo=True).select_related('categoria').order_by('-data_evento', 'nome')
    imagens = ImagemGaleria.objects.filter(ativo=True, evento__ativo=True).select_related('evento')

    if categoria_slug:
        eventos = eventos.filter(categoria__slug=categoria_slug)
        imagens = imagens.filter(evento__categoria__slug=categoria_slug)

    if evento_slug:
        imagens = imagens.filter(evento__slug=evento_slug)

    return render(
        request,
        'core/galeria.html',
        {
            'page_title': 'Galeria | Rosa Chá',
            'meta_description': 'Portfólio visual com atmosferas delicadas para eventos memoráveis.',
            'categorias': categorias,
            'categoria_ativa': categoria_slug,
            'eventos': eventos,
            'evento_ativo': evento_slug,
            'galeria_imagens': imagens,
            'gallery_header_image': gallery_header_image,
        },
    )


def contato(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Recebemos sua mensagem com carinho. Retornaremos em breve para seu orçamento.',
            )
            return redirect(f"{reverse('core:contato')}#formulario")
        messages.error(request, 'Revise os campos destacados e tente novamente.')
    else:
        form = LeadForm()

    return render(
        request,
        'core/contato.html',
        {
            'page_title': 'Contato | Rosa Chá',
            'meta_description': 'Solicite orçamento para seu evento com atendimento personalizado.',
            'form': form,
            'contact_header_image': get_contact_header_image(),
        },
    )
