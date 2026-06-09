import re

file_path = 'templates/dashboard.html'
data = open(file_path, encoding='utf-8').read()

# Comprehensive list of translations (English/Portuguese -> Spanish) and Emoji removals
translations = [
    # 1. Emoji Removal in Tabbar and print titles
    ('🟢 CE Desglose', 'CE Desglose'),
    ('🩷 RC Desglose', 'RC Desglose'),
    ('🔵 CO Desglose', 'CO Desglose'),
    ('🟢 CE — Customer Experience Desglose', 'CE — Customer Experience Desglose'),
    ('🩷 RC — Reduce Costs Desglose', 'RC — Reduce Costs Desglose'),
    ('🔵 CO — Conformidad Operacional Desglose', 'CO — Conformidad Operacional Desglose'),
    ('<span>🟢</span>KBP 1', '<span></span>KBP 1'),
    ('<span>🩷</span>KBP 2', '<span></span>KBP 2'),
    ('<span>🔵</span>KBP 3', '<span></span>KBP 3'),
    ('icon: \'🟢\'', 'icon: \'\''),
    ('icon: \'🩷\'', 'icon: \'\''),
    ('icon: \'🔵\'', 'icon: \'\''),

    # 2. English / Portuguese structural names
    ('Top 5 Lojas', 'Top 5 Tiendas'),
    ('Top 10 Lojas', 'Top 10 Tiendas'),
    ('Top 10 Piores Tiendas', 'Top 10 Peores Tiendas'),
    ('Top 10 Melhores Tiendas', 'Top 10 Mejores Tiendas'),
    ('Piores Tiendas (Mais Alertas KBP)', 'Peores Tiendas (Más Alertas KBP)'),
    ('Melhores Tiendas (Menos Alertas KBP)', 'Mejores Tiendas (Menos Alertas KBP)'),
    ('Piores Tiendas (Mais Alertas por Área)', 'Peores Tiendas (Más Alertas por Área)'),
    ('Melhores Tiendas (Menos Alertas por Área)', 'Mejores Tiendas (Menos Alertas por Área)'),
    ('Ranking Lojas - Delivery Time', 'Ranking de Tiendas - Delivery Time'),
    ('Ranking Lojas com Alertas Drive Thru', 'Ranking de Tiendas con Alertas Drive Thru'),
    ('<span>Loja</span>', '<span>Tienda</span>'),
    ('Alertas da Loja', 'Alertas de la Tienda'),
    ('lojas intermediárias', 'tiendas intermedias'),

    # 3. English titles & metric descriptions in Resumen KPIs and Speed Cards
    ('Delivery Wait Avg', 'Promedio de Espera en Delivery'),
    ('Queuing Time', 'Tiempo de Fila'),
    ('Ordering Time', 'Tiempo de Orden'),
    ('Receiving Time', 'Tiempo de Recepción'),
    ('Service Time', 'Tiempo de Servicio'),
    ('Delivery Time', 'Tiempo de Delivery'),
    ('Queue Time', 'Tiempo de Fila'),

    # 4. KBP descriptions in legend & options
    ('Customer Experience', 'Experiencia del Cliente'),
    ('Reduce Costs', 'Reducción de Costos'),
    ('Op. Compliance', 'Conformidad Operacional'),
    ('Operational Compliance', 'Conformidad Operacional'),
    ('Customer Exp.', 'Experiencia del Cliente'),

    # 5. Area names (English -> Spanish)
    ('Cashier', 'Caja'),
    ('All Store', 'Toda la Tienda'),

    # 6. Specific English items in Areas Tables
    ('Receive order >3min', 'Recepción de orden >3min'),
    ('Staff móvil (caja)', 'Personal móvil (caja)'),
    ('Staff fuera caja >1min', 'Personal fuera de caja >1min'),
    ('No atendido >1min', 'Sin atender >1min'),
    ('Cash drawer open', 'Cajón de dinero abierto'),
    ('PIN pad misuse', 'Uso incorrecto de PIN pad'),
    ('Staff sin gorra', 'Personal sin gorra'),
    ('Lost customer', 'Cliente perdido'),
    ('Store open late', 'Apertura tardía de tienda'),
    ('Staff inactivo >5min', 'Personal inactivo >5min'),
    ('Playing/fighting', 'Jugando/peleando'),
    ('Staff sin uniforme', 'Personal sin uniforme'),
    ('Dirty floor', 'Piso sucio'),
    ('Delivery waiting >1min', 'Espera de delivery >1min'),
    ('[D] PIN pad misuse', '[D] Uso incorrecto de PIN pad'),
    ('[D] Staff fuera caja', '[D] Personal fuera de caja'),
    ('[D] Cash drawer open', '[D] Cajón de dinero abierto'),
    ('[D] Staff móvil', '[D] Personal móvil'),
    ('[D] Receipt not given', '[D] Recibo no entregado'),

    # 7. Delivery Alert table rows
    ('Delivery guy waiting &gt;1min', 'Repartidor esperando &gt;1min'),
    ('Check packaging', 'Verificar empaque'),
    ('Delivery man product in clothes', 'Repartidor con producto en ropa'),
    ('Package closed', 'Empaque cerrado')
]

for old, new in translations:
    data = data.replace(old, new)

# Save the translated dashboard.html back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(data)

print("Comprehensive translation to Spanish and emoji cleanup applied successfully!")
